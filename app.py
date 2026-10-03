from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
import secrets

from DoubtDiagnostic_General import (
    DoubtDiagnostic_General,
    TOPIC_CATALOG,
    classify_natural_language_problem,
    evaluate_student_solution,
    check_safety_concerns,
)
try:
    import Database
except Exception:
    Database = None

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, 'static'),
    template_folder=os.path.join(BASE_DIR, 'templates')
)
app.secret_key = os.environ.get("STUDENT_MENTOR_SECRET", secrets.token_hex(32))
SITE_DOMAIN = os.environ.get("STUDENT_MENTOR_DOMAIN", "studentmentorproject.example").strip().rstrip("/")
SITE_URL = SITE_DOMAIN if SITE_DOMAIN.startswith(("http://", "https://")) else f"https://{SITE_DOMAIN}"

@app.context_processor
def inject_site_config():
    return {"site_domain": SITE_DOMAIN, "site_url": SITE_URL}


SUBJECTS_BY_CLASS = {
    "10": ["Maths", "Science", "Social Science", "English"],
    "11": ["Maths", "Physics", "Chemistry", "Biology", "Computer Science", "English"],
    "12": ["Maths", "Physics", "Chemistry", "Biology", "Computer Science", "English"],
}

def profile():
    return {
        "name": session.get("student_name", "Student"),
        "roll": session.get("roll", ""),
        "section": session.get("section", ""),
        "student_class": session.get("student_class", ""),
    }

def build_result(topic_key, subtopic_key, problem, answers, why, solution):
    d = DoubtDiagnostic_General(
        Roll_no=session.get("roll", ""),
        Student_name=session.get("student_name", "Student"),
        student_class=session.get("student_class", ""),
        Student_Section=session.get("section", ""),
        problem=problem,
        previous_record=None,
    )
    d.selected_topic_key = topic_key
    d.selected_subtopic_key = subtopic_key
    d.diagnostic_answers = answers
    d.followup_notes = why
    d.followup_trajectory = "web_session"
    d.student_proposed_solution = solution
    d.solution_evaluation = evaluate_student_solution(solution)
    d.identified_strengths = [
        "Self-observation: You described the study difficulty in your own words."
    ] + d.solution_evaluation["strengths"]
    sub_name = TOPIC_CATALOG[topic_key]["subtopics"][subtopic_key]["name"]
    d.identified_growth_areas = [
        f"Friction point: {sub_name}",
        "Follow-through: turning the suggested adjustment into a repeatable study habit.",
    ]
    topic_data = TOPIC_CATALOG[topic_key]
    d.comprehensive_advice = topic_data.get("comprehensive_advice", [])
    d.named_protocol = topic_data.get("named_protocol", "Action Plan")
    d.mindset_shift = topic_data.get(
        "mindset_shift",
        "Focus on consistent, manageable improvements rather than trying to fix everything at once.",
    )
    d.actionable_step = topic_data.get(
        "action", "Complete one focused study task today and review what helped."
    )
    key, confidence, matches = classify_natural_language_problem(problem)
    d.nlp_detected_topic = key
    d.nlp_confidence = confidence
    d.nlp_matched_keywords = matches
    result = d.get_structured_result()

    # Use the project's existing database layer when available.
    saved = False
    if Database is not None and hasattr(Database, "save_general_diagnostic"):
        try:
            saved = bool(Database.save_general_diagnostic(result))
        except Exception:
            saved = False
    return result, saved

@app.route("/")
def home():
    return render_template("home.html", profile=profile())


INFO_PAGES = {
    "about": {
        "title": "About Student Mentor & Creator",
        "eyebrow": "RESEARCH & DEVELOPMENT",
        "heading": "Empowering Students Through Intelligent Guidance & Applied Psychology.",
        "text": "Student Mentor Project was designed and developed by Sujay Kiran A, a Class 12 Computer Science student, cybersecurity enthusiast, and researcher. Built at the intersection of computational logic, human psychology, and cognitive diagnostics, this platform transforms vague academic struggle into structured, actionable progress.",
        "cards": [
            ("👨‍💻", "Architect & Researcher", "Designed by Sujay Kiran A with a vision to build technology-driven, psychological support systems that help fellow high schoolers identify academic bottlenecks."),
            ("🧠", "Diagnostic & Cognitive Logic", "The engine bridges student self-reflection with applied cognitive frameworks, turning frustration into structured root-cause analysis."),
            ("🎯", "Action Over Labels", "Rather than standard academic profiling, the platform crafts concrete, individualized micro-actions to rebuild study momentum and mental clarity."),
            ("🛡️", "Data & Security Architecture", "Built with clean software engineering principles, secure input sanitization, and structured database memory layers."),
        ],
    },
    "study": {
        "title": "The Study Flow",
        "eyebrow": "HOW IT WORKS",
        "heading": "From first check-in to a practical next action.",
        "text": "The web flow keeps the original Student Mentor sequence while presenting it in a cleaner student-facing interface.",
        "cards": [
            ("01", "Profile", "Enter class, section and roll details."),
            ("02", "Mood & wellness", "Check in before the academic pathway."),
            ("03", "Academic Q1/Q2", "Choose between subject-specific and general study difficulties."),
            ("04", "Diagnosis", "Move through topic, subtopic and diagnostic questions."),
            ("05", "Mentor report", "Receive strengths, growth areas and an actionable plan."),
        ],
    },
    "scenarios": {
        "title": "Diagnostic Scenarios",
        "eyebrow": "SCENARIOS",
        "heading": "Real study friction, explored step by step.",
        "text": "General-study topics cover concentration, distractions, procrastination, family and home environment, peer influence, exam pressure and more.",
        "cards": [
            ("01", "Concentration & mental stamina", "Explore difficulty starting, sustaining or recovering focus."),
            ("02", "Digital & environmental distractions", "Look at devices, noise, interruptions and study surroundings."),
            ("03", "Procrastination & delaying tasks", "Understand task avoidance and starting friction."),
            ("04", "Family expectations & home environment", "Explore pressure, routines and the effect of the home setting."),
            ("05", "Friends & peer influence", "Consider social pressure and study habits around peers."),
            ("06", "Exam pressure & performance anxiety", "Explore pressure around tests and performance."),
        ],
    },
    "psychology": {
        "title": "Psychology in the Project",
        "eyebrow": "PSYCHOLOGY",
        "heading": "Reflection is part of the diagnostic process.",
        "text": "The system uses student self-observation, reflection questions and solution evaluation to make the final mentor report more specific.",
        "cards": [
            ("🔎", "Self-observation", "Students describe what is actually happening in their own words."),
            ("💬", "Reflection", "Follow-up questions connect the difficulty to the student's perspective."),
            ("🧩", "Strengths & growth", "The report separates existing strengths from areas that need follow-through."),
        ],
    },
    "resources": {
        "title": "Resources",
        "eyebrow": "STUDENT TOOLKIT",
        "heading": "Useful pathways inside Student Mentor.",
        "text": "Use the diagnostic flow, subject pathways and progress history as the main project resources.",
        "cards": [
            ("📚", "Academic diagnosis", "Start the mentoring flow and identify where the difficulty sits."),
            ("🗂️", "General-study topics", "Browse the full general-study topic catalogue when the issue is not tied to one subject."),
            ("📊", "My progress", "Review records saved through the existing database layer."),
        ],
    },
    "participate": {
        "title": "Participate",
        "eyebrow": "START HERE",
        "heading": "Your next step starts with an honest description.",
        "text": "Begin with your student details and follow the diagnostic pathway. The system is designed around your own responses rather than a generic one-size-fits-all answer.",
        "cards": [
            ("→", "Start mentoring", "Enter the full Student Mentor flow."),
            ("✎", "Describe the problem", "Use your own words when the general-study pathway asks what is difficult."),
            ("✓", "Take the next action", "Use the final report as a practical starting point."),
        ],
    },
}

@app.route("/info/<page>")
def info_page(page):
    data = INFO_PAGES.get(page)
    if not data:
        return redirect(url_for("home"))
    return render_template("info.html", profile=profile(), **data)

@app.route("/start", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        roll = request.form.get("roll", "").strip()
        section = request.form.get("section", "").strip()
        student_class = request.form.get("student_class", "").strip()
        if not name or not roll or not section or student_class not in {"10", "11", "12"}:
            flash("Please complete all student details.", "error")
            return render_template("start.html", values=request.form)
        session["student_name"] = name
        session["roll"] = roll
        session["section"] = section
        session["student_class"] = student_class
        session["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return redirect(url_for("mood"))
    return render_template("start.html", values={})

@app.route("/mood", methods=["GET", "POST"])
def mood():
    if request.method == "POST":
        mood_value = request.form.get("mood", "fine")
        session["mood"] = mood_value
        if mood_value in {"anxious", "stressed", "angry"}:
            return redirect(url_for("wellness"))
        return redirect(url_for("academic"))
    return render_template("mood.html", profile=profile())

@app.route("/wellness", methods=["GET", "POST"])
def wellness():
    if request.method == "POST":
        activity = request.form.get("activity", "continue")
        session["wellness_activity"] = activity
        return redirect(url_for("academic"))
    return render_template("wellness.html", profile=profile())

@app.route("/academic", methods=["GET", "POST"])
def academic():
    if request.method == "POST":
        q1 = request.form.get("q1")
        if q1 == "no":
            return render_template("clear.html", profile=profile())
        if q1 != "yes":
            flash("Please choose an option.", "error")
            return render_template("academic.html", profile=profile())
        q2 = request.form.get("q2")
        if q2 == "yes":
            return redirect(url_for("subject"))
        if q2 == "no":
            return redirect(url_for("general_problem"))
        flash("Please choose an option.", "error")
    return render_template("academic.html", profile=profile())

@app.route("/subject")
def subject():
    cls = session.get("student_class", "")
    return render_template(
        "subject.html",
        profile=profile(),
        subjects=SUBJECTS_BY_CLASS.get(cls, []),
    )

@app.route("/subject/<subject_name>")
def subject_bridge(subject_name):
    # The original Class10/Class11/Class12 modules are kept at the project root.
    # This page provides a polished web bridge while keeping the existing
    # subject diagnostic implementation untouched.
    return render_template(
        "subject_bridge.html",
        profile=profile(),
        subject=subject_name.replace("-", " ").title(),
    )

@app.route("/general", methods=["GET", "POST"])
def general_problem():
    if request.method == "POST":
        problem = request.form.get("problem", "").strip()
        if not problem:
            flash("Tell me a little about the difficulty in your own words.", "error")
            return render_template("general_problem.html", profile=profile())
        session["general_problem"] = problem
        if check_safety_concerns(problem):
            return render_template("support.html", profile=profile())
        key, confidence, matches = classify_natural_language_problem(problem)
        session["nlp_key"] = key
        session["nlp_confidence"] = confidence
        session["nlp_matches"] = matches
        if key and key in TOPIC_CATALOG:
            return redirect(url_for("general_topic", topic_key=key))
        return redirect(url_for("general_topics"))
    return render_template("general_problem.html", profile=profile())

@app.route("/general/topics", methods=["GET", "POST"])
def general_topics():
    if request.method == "POST":
        key = request.form.get("topic_key")
        if key in TOPIC_CATALOG:
            return redirect(url_for("general_topic", topic_key=key))
        flash("Please select a topic.", "error")
    cards = [(k, v["title"]) for k, v in TOPIC_CATALOG.items()]
    return render_template(
        "general_topics.html", profile=profile(), topics=cards,
        detected=session.get("nlp_key"), confidence=session.get("nlp_confidence", 0)
    )

@app.route("/general/topic/<topic_key>", methods=["GET", "POST"])
def general_topic(topic_key):
    if topic_key not in TOPIC_CATALOG:
        return redirect(url_for("general_topics"))
    data = TOPIC_CATALOG[topic_key]
    subtopics = data["subtopics"]
    if request.method == "POST":
        subkey = request.form.get("subtopic_key")
        if subkey not in subtopics:
            flash("Please select a scenario.", "error")
            return render_template("subtopic.html", profile=profile(), topic=data, topic_key=topic_key)
        session["topic_key"] = topic_key
        session["subtopic_key"] = subkey
        return redirect(url_for("general_questions", topic_key=topic_key, subtopic_key=subkey))
    return render_template("subtopic.html", profile=profile(), topic=data, topic_key=topic_key)

@app.route("/general/questions/<topic_key>/<subtopic_key>", methods=["GET", "POST"])
def general_questions(topic_key, subtopic_key):
    if topic_key not in TOPIC_CATALOG or subtopic_key not in TOPIC_CATALOG[topic_key]["subtopics"]:
        return redirect(url_for("general_topics"))
    data = TOPIC_CATALOG[topic_key]
    questions = data.get("questions", [])
    if request.method == "POST":
        answers = []
        for idx, (q, opts) in enumerate(questions):
            val = request.form.get(f"q{idx}")
            if val not in opts:
                flash("Please answer every diagnostic question.", "error")
                return render_template("questions.html", profile=profile(), topic=data, questions=questions, topic_key=topic_key, subtopic_key=subtopic_key)
            answers.append({"question": q, "selected_option": val, "answer_text": opts[val]})
        why = request.form.get("why", "").strip()
        solution = request.form.get("solution", "").strip()
        if not why or not solution:
            flash("Please complete both reflection boxes.", "error")
            return render_template("questions.html", profile=profile(), topic=data, questions=questions, topic_key=topic_key, subtopic_key=subtopic_key)
        result, saved = build_result(
            topic_key, subtopic_key, session.get("general_problem", ""),
            answers, why, solution
        )
        session["last_result"] = result
        session["last_saved"] = saved
        return redirect(url_for("report"))
    return render_template("questions.html", profile=profile(), topic=data, questions=questions, topic_key=topic_key, subtopic_key=subtopic_key)

@app.route("/report")
def report():
    result = session.get("last_result")
    if not result:
        return redirect(url_for("home"))
    return render_template("report.html", profile=profile(), result=result, saved=session.get("last_saved", False))

@app.route("/history")
def history():
    rows = []
    general = None
    if Database is not None:
        try:
            if hasattr(Database, "check_student_history"):
                rows = Database.check_student_history(session.get("roll", ""))
            if hasattr(Database, "get_last_general_diagnostic"):
                general = Database.get_last_general_diagnostic(session.get("roll", ""))
        except Exception:
            pass
    return render_template("history.html", profile=profile(), rows=rows, general=general)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
