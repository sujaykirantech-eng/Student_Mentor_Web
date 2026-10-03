import os
import json
import sqlite3
from datetime import datetime

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception

SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_mentor.db")

def is_mysql_available():
    """Checks if a reachable MySQL server is configured."""
    if mysql is None:
        return False
    # If on cloud (Render) without external host explicitly set, skip MySQL connect delay
    host = os.getenv("STUDENT_MENTOR_DB_HOST", "")
    if not host or host == "localhost":
        if os.getenv("RENDER"):
            return False
    try:
        conn = mysql.connector.connect(
            host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
            port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
            user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
            password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", ""),
            connection_timeout=2
        )
        conn.close()
        return True
    except Exception:
        return False

def get_sqlite_conn():
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def ensure_sqlite_tables():
    conn = get_sqlite_conn()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS study_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Roll_no TEXT NOT NULL,
        Student_name TEXT,
        student_class TEXT,
        Student_Section TEXT,
        subject TEXT,
        chapter TEXT,
        topic TEXT,
        difficulty TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS general_study_diagnostics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT NOT NULL,
        student_name TEXT,
        student_class TEXT,
        section TEXT,
        topic_key TEXT,
        topic TEXT,
        subtopic_key TEXT,
        subtopic TEXT,
        problem TEXT,
        answers TEXT,
        followup_notes TEXT,
        student_solution TEXT,
        solution_strengths TEXT,
        solution_blind_spots TEXT,
        identified_strengths TEXT,
        identified_growth_areas TEXT,
        comprehensive_advice TEXT,
        named_protocol TEXT,
        mindset_shift TEXT,
        action_step TEXT,
        nlp_detected_topic TEXT,
        nlp_confidence REAL,
        nlp_matched_keywords TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def get_connection():
    if mysql is None:
        raise RuntimeError("mysql-connector-python not available")
    return mysql.connector.connect(
        host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
        port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
        user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
        password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", ""),
        database=os.getenv("STUDENT_MENTOR_DB_NAME", "student_mentor")
    )

def ensure_database():
    if not is_mysql_available():
        ensure_sqlite_tables()
        return
    try:
        init_conn = mysql.connector.connect(
            host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
            port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
            user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
            password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", "")
        )
        cursor = init_conn.cursor()
        db_name = os.getenv("STUDENT_MENTOR_DB_NAME", "student_mentor")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.close()
        init_conn.close()
    except Exception:
        ensure_sqlite_tables()

def save_response(Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty):
    ensure_database()
    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_responses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Roll_no VARCHAR(50) NOT NULL,
                Student_name VARCHAR(150),
                student_class VARCHAR(30),
                Student_Section VARCHAR(20),
                subject VARCHAR(100),
                chapter VARCHAR(200),
                topic VARCHAR(200),
                difficulty TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)
            query = """
            INSERT INTO study_responses 
            (Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(query, (Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception:
            pass

    # SQLite fallback
    try:
        ensure_sqlite_tables()
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
        INSERT INTO study_responses 
        (Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("SQLite save error:", e)
        return False

def check_previous_doubt(Roll_no, subject, topic):
    ensure_database()
    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor()
            query = """
            SELECT chapter, topic, difficulty, created_at
            FROM study_responses
            WHERE Roll_no = %s AND subject = %s AND topic = %s
            ORDER BY created_at DESC;
            """
            cursor.execute(query, (Roll_no, subject, topic))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            if results:
                return results
        except Exception:
            pass

    # SQLite fallback
    try:
        ensure_sqlite_tables()
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
        SELECT chapter, topic, difficulty, created_at
        FROM study_responses
        WHERE Roll_no = ? AND subject = ? AND topic = ?
        ORDER BY created_at DESC;
        """, (str(Roll_no), str(subject), str(topic)))
        rows = c.fetchall()
        results = [(r["chapter"], r["topic"], r["difficulty"], str(r["created_at"])) for r in rows]
        conn.close()
        return results
    except Exception:
        return []

def check_student_history(Roll_no):
    ensure_database()
    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor()
            query = """
            SELECT subject, chapter, topic, difficulty, created_at
            FROM study_responses
            WHERE Roll_no = %s
            ORDER BY created_at DESC;
            """
            cursor.execute(query, (Roll_no,))
            results = cursor.fetchall()
            cursor.close()
            db.close()
            if results:
                return results
        except Exception:
            pass

    # SQLite fallback
    try:
        ensure_sqlite_tables()
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
        SELECT subject, chapter, topic, difficulty, created_at
        FROM study_responses
        WHERE Roll_no = ?
        ORDER BY created_at DESC;
        """, (str(Roll_no),))
        rows = c.fetchall()
        results = [(r["subject"], r["chapter"], r["topic"], r["difficulty"], str(r["created_at"])) for r in rows]
        conn.close()
        return results
    except Exception:
        return []

def get_last_general_diagnostic(roll_no):
    ensure_database()
    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor(dictionary=True)
            query = """
            SELECT topic, subtopic, action_step, created_at, student_solution
            FROM general_study_diagnostics
            WHERE roll_no = %s
            ORDER BY id DESC LIMIT 1;
            """
            cursor.execute(query, (str(roll_no),))
            res = cursor.fetchone()
            cursor.close()
            db.close()
            if res:
                return res
        except Exception:
            pass

    # SQLite fallback
    try:
        ensure_sqlite_tables()
        conn = get_sqlite_conn()
        c = conn.cursor()
        c.execute("""
        SELECT topic, subtopic, action_step, created_at, student_solution
        FROM general_study_diagnostics
        WHERE roll_no = ?
        ORDER BY id DESC LIMIT 1;
        """, (str(roll_no),))
        row = c.fetchone()
        res = dict(row) if row else None
        conn.close()
        return res
    except Exception:
        return None

def save_general_diagnostic(data: dict):
    ensure_database()
    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor()
            # standard MySQL insert
            query = """
            INSERT INTO general_study_diagnostics (
                roll_no, student_name, student_class, section,
                topic_key, topic, subtopic_key, subtopic, problem, answers,
                followup_notes, student_solution, solution_strengths,
                solution_blind_spots, identified_strengths, identified_growth_areas,
                comprehensive_advice, named_protocol, mindset_shift, action_step,
                nlp_detected_topic, nlp_confidence, nlp_matched_keywords
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s
            );
            """
            sol = data.get("solution_evaluation", {})
            cursor.execute(query, (
                data.get("Roll_no"), data.get("Student_name"), data.get("student_class"), data.get("Student_Section"),
                data.get("selected_topic_key"), data.get("topic"), data.get("selected_subtopic_key"), data.get("subtopic"),
                data.get("problem"), json.dumps(data.get("diagnostic_answers", [])), data.get("followup_notes"),
                data.get("student_proposed_solution"), json.dumps(sol.get("strengths", [])), json.dumps(sol.get("blind_spots", [])),
                json.dumps(data.get("identified_strengths", [])), json.dumps(data.get("identified_growth_areas", [])),
                json.dumps(data.get("comprehensive_advice", [])), data.get("named_protocol"), data.get("mindset_shift"),
                data.get("action_step"), data.get("nlp_detected_topic"), data.get("nlp_confidence"),
                json.dumps(data.get("nlp_matched_keywords", []))
            ))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception:
            pass

    # SQLite fallback
    try:
        ensure_sqlite_tables()
        conn = get_sqlite_conn()
        c = conn.cursor()
        query = """
        INSERT INTO general_study_diagnostics (
            roll_no, student_name, student_class, section,
            topic_key, topic, subtopic_key, subtopic, problem, answers,
            followup_notes, student_solution, solution_strengths,
            solution_blind_spots, identified_strengths, identified_growth_areas,
            comprehensive_advice, named_protocol, mindset_shift, action_step,
            nlp_detected_topic, nlp_confidence, nlp_matched_keywords
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?
        );
        """
        sol = data.get("solution_evaluation", {})
        c.execute(query, (
            data.get("Roll_no"), data.get("Student_name"), data.get("student_class"), data.get("Student_Section"),
            data.get("selected_topic_key"), data.get("topic"), data.get("selected_subtopic_key"), data.get("subtopic"),
            data.get("problem"), json.dumps(data.get("diagnostic_answers", [])), data.get("followup_notes"),
            data.get("student_proposed_solution"), json.dumps(sol.get("strengths", [])), json.dumps(sol.get("blind_spots", [])),
            json.dumps(data.get("identified_strengths", [])), json.dumps(data.get("identified_growth_areas", [])),
            json.dumps(data.get("comprehensive_advice", [])), data.get("named_protocol"), data.get("mindset_shift"),
            data.get("action_step"), data.get("nlp_detected_topic"), data.get("nlp_confidence"),
            json.dumps(data.get("nlp_matched_keywords", []))
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("SQLite save general error:", e)
        return False
