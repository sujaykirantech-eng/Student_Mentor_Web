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
    r_no = str(data.get("roll_no") or data.get("Roll_no") or "101")
    s_name = str(data.get("student_name") or data.get("Student_name") or "Student")
    s_class = str(data.get("student_class") or "12")
    s_sec = str(data.get("student_section") or data.get("Student_Section") or data.get("section") or "A")
    t_key = str(data.get("selected_topic_key") or data.get("topic_key") or "")
    t_name = str(data.get("topic") or "")
    st_key = str(data.get("selected_subtopic_key") or data.get("subtopic_key") or "")
    st_name = str(data.get("subtopic") or "")
    prob = str(data.get("problem") or data.get("raw_input") or "")
    ans = json.dumps(data.get("diagnostic_answers", []))
    notes = str(data.get("followup_notes") or "")
    sol = str(data.get("student_proposed_solution") or data.get("student_solution") or "")
    sol_eval = data.get("solution_evaluation", {})
    sol_str = json.dumps(sol_eval.get("strengths", [])) if isinstance(sol_eval, dict) else json.dumps([])
    sol_blind = json.dumps(sol_eval.get("blind_spots", [])) if isinstance(sol_eval, dict) else json.dumps([])
    strengths = data.get("strengths")
    strengths_str = strengths if isinstance(strengths, str) else json.dumps(strengths or [])
    growth = data.get("growth_areas")
    growth_str = growth if isinstance(growth, str) else json.dumps(growth or [])
    advice = data.get("comprehensive_advice")
    advice_str = json.dumps(advice) if isinstance(advice, list) else str(advice or "")
    protocol = str(data.get("named_protocol") or "Action Plan")
    mindset = str(data.get("mindset_shift") or "")
    action = str(data.get("action_step") or "")
    nlp_cat = str(data.get("nlp_detected_topic") or data.get("nlp_category") or "")
    nlp_conf = float(data.get("nlp_confidence") or 0.0)
    nlp_kw = json.dumps(data.get("nlp_matched_keywords", []))

    if is_mysql_available():
        try:
            db = get_connection()
            cursor = db.cursor()
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
            cursor.execute(query, (
                r_no, s_name, s_class, s_sec,
                t_key, t_name, st_key, st_name, prob, ans,
                notes, sol, sol_str, sol_blind, strengths_str, growth_str,
                advice_str, protocol, mindset, action,
                nlp_cat, nlp_conf, nlp_kw
            ))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print("MySQL save general diagnostic exception:", e)

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
        c.execute(query, (
            r_no, s_name, s_class, s_sec,
            t_key, t_name, st_key, st_name, prob, ans,
            notes, sol, sol_str, sol_blind, strengths_str, growth_str,
            advice_str, protocol, mindset, action,
            nlp_cat, nlp_conf, nlp_kw
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("SQLite save general error:", e)
        return False
