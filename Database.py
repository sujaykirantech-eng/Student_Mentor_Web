try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    mysql = None
    Error = Exception
import json
import os

def get_connection():
    """Helper to connect to the MySQL database."""
    if mysql is None:
        raise RuntimeError("mysql-connector-python is not installed. Please run: pip install mysql-connector-python")
    return mysql.connector.connect(
        host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
        port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
        user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
        password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", ""),
        database=os.getenv("STUDENT_MENTOR_DB_NAME", "student_mentor")
    )

def ensure_database():
    """Ensure the student_mentor database exists before executing queries."""
    if mysql is None:
        return
    try:
        init_conn = mysql.connector.connect(
            host=os.getenv("STUDENT_MENTOR_DB_HOST", "localhost"),
            port=int(os.getenv("STUDENT_MENTOR_DB_PORT", "3306")),
            user=os.getenv("STUDENT_MENTOR_DB_USER", "root"),
            password=os.getenv("STUDENT_MENTOR_DB_PASSWORD", "")
        )
        cursor = init_conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS student_mentor;")
        init_conn.commit()
        cursor.close()
        init_conn.close()
    except Exception:
        pass

def save_response(Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty):
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_responses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Roll_no VARCHAR(50) NOT NULL,
            Student_name VARCHAR(150),
            student_class VARCHAR(30),
            Student_Section VARCHAR(30),
            subject VARCHAR(100),
            chapter VARCHAR(100),
            topic TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_resp_roll (Roll_no),
            INDEX idx_resp_subject (subject)
        );
        """)

        query = """
        INSERT INTO study_responses
        (Roll_no, Student_name, student_class, Student_Section, subject, chapter, topic, difficulty)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            Roll_no,
            Student_name,
            student_class,
            Student_Section,
            subject,
            chapter,
            topic,
            difficulty
        )
        cursor.execute(query, values)
        db.commit()
        print("\nResponse saved successfully to MySQL! ✅")
        return True
    except Error as e:
        print(f"\n[MySQL Error while saving response]: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

def check_previous_doubt(Roll_no, subject, topic):
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()
        query = """
        SELECT chapter, topic, difficulty, created_at
        FROM study_responses
        WHERE Roll_no = %s
        AND subject = %s
        AND topic = %s
        ORDER BY created_at DESC
        """
        cursor.execute(query, (Roll_no, subject, topic))
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"\n[MySQL Error while checking previous doubt]: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

def check_student_history(Roll_no):
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()
        query = """
        SELECT subject, chapter, topic, difficulty, created_at
        FROM study_responses
        WHERE Roll_no = %s
        ORDER BY created_at DESC
        """
        cursor.execute(query, (Roll_no,))
        results = cursor.fetchall()
        return results
    except Error as e:
        return []
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

def get_last_general_diagnostic(roll_no):
    """Retrieves the student's previous general study diagnostic from MySQL."""
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)
        query = """
        SELECT topic, subtopic, action_step, created_at, student_solution
        FROM general_study_diagnostics
        WHERE roll_no = %s
        ORDER BY id DESC
        LIMIT 1;
        """
        cursor.execute(query, (str(roll_no).strip(),))
        row = cursor.fetchone()
        return row
    except Error:
        return None
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

def save_general_diagnostic(data: dict):
    """Saves a general study diagnostic report into a separate MySQL table."""
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS general_study_diagnostics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll_no VARCHAR(50) NOT NULL,
            student_name VARCHAR(150),
            student_class VARCHAR(30),
            student_section VARCHAR(30),
            topic VARCHAR(100) NOT NULL,
            subtopic VARCHAR(200) NOT NULL,
            raw_input TEXT,
            followup_notes TEXT,
            followup_trajectory VARCHAR(100),
            nlp_category VARCHAR(100),
            nlp_confidence FLOAT,
            nlp_keywords TEXT,
            diagnostic_answers JSON,
            student_solution TEXT,
            strengths TEXT,
            growth_areas TEXT,
            recommended_strategy TEXT,
            action_step TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_gen_roll (roll_no),
            INDEX idx_gen_topic (topic)
        );
        """)

        insert_query = """
        INSERT INTO general_study_diagnostics (
            roll_no, student_name, student_class, student_section,
            topic, subtopic, raw_input, followup_notes, followup_trajectory,
            nlp_category, nlp_confidence, nlp_keywords, diagnostic_answers,
            student_solution, strengths, growth_areas, recommended_strategy, action_step
        ) VALUES (
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        );
        """
        values = (
            data.get("roll_no"),
            data.get("student_name"),
            data.get("student_class"),
            data.get("student_section"),
            data.get("topic"),
            data.get("subtopic"),
            data.get("raw_input"),
            data.get("followup_notes"),
            data.get("followup_trajectory"),
            data.get("nlp_category"),
            data.get("nlp_confidence"),
            data.get("nlp_keywords"),
            json.dumps(data.get("diagnostic_answers", [])),
            data.get("student_solution"),
            data.get("strengths"),
            data.get("growth_areas"),
            data.get("named_protocol") or data.get("recommended_strategy"),
            data.get("action_step")
        )
        cursor.execute(insert_query, values)
        db.commit()
        print("\nGeneral study diagnostic saved to MySQL database successfully! ✅")
        return True
    except Error as err:
        print(f"\n[Database Error] Could not save general diagnostic: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()

def save_teacher_diagnostic(
    Roll_no,
    Student_name,
    student_class,
    Student_Section,
    subject,
    subtopic,
    question_no,
    question,
    student_response,
    detected_signals,
    matched_words,
    student_reasoning,
    student_solution,
    selected_action,
    strengths,
    growth_areas,
    possible_factors,
    advice
):
    ensure_database()
    db = cursor = None
    try:
        db = get_connection()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS general_teacher_diagnostics (
                id INT AUTO_INCREMENT PRIMARY KEY,
                Roll_no VARCHAR(50) NOT NULL,
                Student_name VARCHAR(150),
                student_class VARCHAR(30),
                Student_Section VARCHAR(30),
                subject VARCHAR(100),
                topic VARCHAR(100) NOT NULL,
                subtopic VARCHAR(200) NOT NULL,
                question_no INT,
                question TEXT,
                student_response TEXT,
                detected_signals TEXT,
                matched_words TEXT,
                student_reasoning TEXT,
                student_solution TEXT,
                selected_action TEXT,
                strengths TEXT,
                growth_areas TEXT,
                possible_factors TEXT,
                advice TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_teacher_roll (Roll_no),
                INDEX idx_teacher_subtopic (subtopic),
                INDEX idx_teacher_created (created_at)
            )
        """)

        query = """
            INSERT INTO general_teacher_diagnostics
            (
                Roll_no, Student_name, student_class, Student_Section, subject,
                topic, subtopic, question_no, question, student_response,
                detected_signals, matched_words, student_reasoning, student_solution,
                selected_action, strengths, growth_areas, possible_factors, advice
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            Roll_no,
            Student_name,
            student_class,
            Student_Section,
            subject,
            "Teacher / Teaching Problems",
            subtopic,
            question_no,
            question,
            student_response,
            detected_signals,
            matched_words,
            student_reasoning,
            student_solution,
            selected_action,
            strengths,
            growth_areas,
            possible_factors,
            advice
        )
        cursor.execute(query, values)
        db.commit()
        print("Teacher diagnostic response saved successfully! ✅")
        return True
    except Error as error:
        print("MySQL Error while saving teacher diagnostic:", error)
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None and db.is_connected():
            db.close()
