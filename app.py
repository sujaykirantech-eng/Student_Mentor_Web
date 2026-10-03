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

def _session_profile_complete():
    required = {"student_name": "Sujay Kiran", "roll": "101", "section": "A", "student_class": "12"}
    for k, v in required.items():
        if not str(session.get(k, "")).strip():
            session[k] = v
    return True

def _diagnostic_severity(answers):
    """Return a simple 0-100 web-flow friction indicator from selected option positions."""
    if not answers:
        return 0
    values = []
    for item in answers:
        try:
            values.append(int(str(item.get("selected_option", "1"))))
        except (TypeError, ValueError):
            values.append(1)
    max_value = max(values) if values else 1
    return int(round(sum(values) / len(values) / max(max_value, 1) * 100))

def _report_from_session():
    state = session.get("general_diagnostic")
    if not isinstance(state, dict):
        return None, "Your diagnostic session has expired. Please start the General Study pathway again."
    topic_key = state.get("topic_key")
    subtopic_key = state.get("subtopic_key")
    if topic_key not in TOPIC_CATALOG or subtopic_key not in TOPIC_CATALOG[topic_key].get("subtopics", {}):
        return None, "The selected study topic is no longer available in this session. Please choose it again."
    if not _session_profile_complete():
        return None, "Your student profile is missing. Please start the mentoring flow again."
    try:
        answers = state.get("answers", [])
        why = str(state.get("why", "")).strip()
        solution = str(state.get("solution", "")).strip()
        problem = str(state.get("problem", "")).strip()
        if not answers or not why or not solution or not problem:
            return None, "Some diagnostic responses are missing. Please complete the assessment again."
        result, _ = build_result(topic_key, subtopic_key, problem, answers, why, solution, save=False)
        result["severity_score"] = state.get("severity_score", _diagnostic_severity(answers))
        return result, None
    except (KeyError, TypeError, ValueError):
        return None, "The mentor report could not be reconstructed safely. Please start the assessment again."

def build_result(topic_key, subtopic_key, problem, answers, why, solution, save=True):
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
    if save and Database is not None and hasattr(Database, "save_general_diagnostic"):
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


# Comprehensive subject syllabi & diagnostic data
SUBJECT_DIAGNOSTIC_DATA = {
    "12": {
        "Chemistry": {
            "chapters": {
                "1": "Solutions", "2": "Electrochemistry", "3": "Chemical Kinetics",
                "4": "d and f Block Elements", "5": "Coordination Compounds",
                "6": "Haloalkanes and Haloarenes", "7": "Alcohols Phenols and Ethers",
                "8": "Aldehydes Ketones and Carboxylic Acids", "9": "Amines",
                "10": "Biomolecules", "11": "Principles of Practical Chemistry"
            },
            "topics": {
                "1": {"1": "Types of Solutions", "2": "Concentration Terms", "3": "Solubility & Henry's Law", "4": "Colligative Properties & Raoult's Law", "5": "Abnormal Molar Mass & Van 't Hoff Factor"},
                "2": {"1": "Galvanic & Electrolytic Cells", "2": "Nernst Equation & Gibbs Energy", "3": "Conductance & Kohlrausch's Law", "4": "Faraday's Laws", "5": "Batteries & Corrosion"},
                "3": {"1": "Rate of Reaction", "2": "Order and Molecularity", "3": "Integrated Rate Law & Half-Life", "4": "Pseudo First Order", "5": "Arrhenius Equation"},
                "4": {"1": "Electronic Configuration & General Properties", "2": "Oxidation States & Magnetic Properties", "3": "Potassium Dichromate & Permanganate", "4": "Lanthanoid Contraction", "5": "Actinoids"},
                "5": {"1": "Werner's Theory", "2": "IUPAC Nomenclature", "3": "Isomerism", "4": "Valence Bond Theory (VBT)", "5": "Crystal Field Theory (CFT)"},
                "6": {"1": "Nomenclature & Nature of C-X", "2": "Preparation Methods", "3": "SN1 and SN2 Reaction Mechanisms", "4": "Polyhalogen Compounds"},
                "7": {"1": "Classification & Nomenclature", "2": "Preparation of Alcohols & Phenols", "3": "Reactions of Phenols", "4": "Williamson Ether Synthesis"},
                "8": {"1": "Carbonyl Structure & Nomenclature", "2": "Preparation Methods", "3": "Nucleophilic Addition", "4": "Aldol & Cannizzaro Reactions", "5": "Carboxylic Acids"},
                "9": {"1": "Classification of Amines", "2": "Preparation Methods", "3": "Basic Character & Reactions", "4": "Diazonium Salts"},
                "10": {"1": "Monosaccharides (Glucose/Fructose)", "2": "Proteins & Peptide Bonds", "3": "Denaturation & Enzymes", "4": "Nucleic Acids & Vitamins"}
            },
            "difficulties": {
                "1": "I do not understand the core chemical concept or physical theory.",
                "2": "I understand the theory but forget formulas, reaction conditions or trends.",
                "3": "I understand the concept but struggle to solve numericals and word problems.",
                "4": "I make calculation, sign, formula or nomenclature mistakes.",
                "5": "I get confused between similar organic reaction mechanisms and reagents.",
                "6": "I struggle with time management or getting stuck midway in exams."
            },
            "advice": {
                "1": [
                    "Start from the core physical or chemical definition rather than jumping directly into complex questions.",
                    "Break the theory into three pillars: What happens, Why it happens (molecular reasons), and Key NCERT exceptions.",
                    "Write down a 3-sentence summary in your own words using standard terminology."
                ],
                "2": [
                    "Use active recall and spaced repetition instead of repeatedly rereading pages.",
                    "Maintain a dedicated 2-page formula & reagent cheat sheet with conditions and units.",
                    "Close your notebook every evening and reproduce 5 reactions/formulas purely from memory."
                ],
                "3": [
                    "Follow the 3-step structured numerical pipeline: Write 'Given Data' with standard units, specify 'Target Variable', and write the governing equation first.",
                    "Standardize units immediately before calculating (e.g., Temperature to Kelvin, Volume to L, Pressure to atm).",
                    "Solve 4 worked NCERT examples step-by-step before attempting unassisted exercises."
                ],
                "4": [
                    "Maintain an active 'Mistake Log' book categorizing errors into Calculation, Sign, Unit, or Nomenclature slips.",
                    "Check the dimensional units of your final answer before declaring it finished.",
                    "Slow down your pen speed by 10% during multi-step arithmetic expansions to eliminate careless slips."
                ],
                "5": [
                    "Create comparative side-by-side summary tables contrasting reagents and mechanisms.",
                    "Identify the nucleophile (electron-rich) and electrophile (electron-poor) centers rather than memorizing entire equations.",
                    "Map reactions as functional group conversion roadmaps (e.g., Alkyl Halide -> Alcohol -> Aldehyde -> Acid)."
                ],
                "6": [
                    "Adopt the 2-minute test rule: If no clear solution path emerges after 2 minutes, mark for review and move on.",
                    "Practice 45-minute timed sprint blocks using previous years' questions.",
                    "Analyze every practice exam to separate knowledge deficits from pacing/calculation fatigue."
                ]
            }
        },
        "Maths": {
            "chapters": {
                "1": "Relations and Functions", "2": "Inverse Trigonometric Functions", "3": "Matrices",
                "4": "Determinants", "5": "Continuity and Differentiability", "6": "Application of Derivatives",
                "7": "Integrals", "8": "Application of Integrals", "9": "Differential Equations",
                "10": "Vector Algebra", "11": "Three Dimensional Geometry", "12": "Linear Programming", "13": "Probability"
            },
            "topics": {
                "1": {"1": "Types of Relations (Equivalence)", "2": "Types of Functions (One-One, Onto)", "3": "Composition & Invertible Functions"},
                "3": {"1": "Matrix Operations & Types", "2": "Matrix Multiplication", "3": "Transpose & Symmetric Matrices", "4": "Inverse of Matrix"},
                "4": {"1": "Properties of Determinants", "2": "Minors & Cofactors", "3": "Adjoint & Inverse", "4": "Solving Systems via Matrix Method"},
                "5": {"1": "Continuity at a Point", "2": "Differentiability & Chain Rule", "3": "Logarithmic Differentiation", "4": "Parametric Forms & Second Order Derivatives"},
                "6": {"1": "Rate of Change", "2": "Increasing and Decreasing Functions", "3": "Maxima and Minima"},
                "7": {"1": "Integration by Substitution", "2": "Integration by Partial Fractions", "3": "Integration by Parts", "4": "Definite Integrals & Properties"},
                "9": {"1": "Order and Degree", "2": "Variable Separable", "3": "Homogeneous Differential Equations", "4": "Linear Differential Equations"},
                "10": {"1": "Direction Cosines", "2": "Scalar (Dot) Product", "3": "Vector (Cross) Product"},
                "11": {"1": "Direction Cosines & Ratios", "2": "Equation of Line in Space", "3": "Shortest Distance between Skew Lines"},
                "13": {"1": "Conditional Probability", "2": "Independent Events", "3": "Bayes' Theorem", "4": "Probability Distribution"}
            },
            "difficulties": {
                "1": "I do not understand the underlying concept or theorem proof.",
                "2": "I know formulas but cannot identify which method/substitution to apply.",
                "3": "I understand the method but get stuck midway during algebraic simplification.",
                "4": "I make frequent sign, algebra, or calculation mistakes.",
                "5": "I struggle with speed and managing time during exam conditions."
            },
            "advice": {
                "1": ["Study the geometric interpretation and standard definitions before attempting questions.", "Work through 2 standard textbook examples while writing out the justification for each step."],
                "2": ["Train method recognition: categorize problems by visual structure rather than formula names.", "Ask three questions before writing: What is given? What is required? Which standard form does this match?"],
                "3": ["Break long multi-step solutions into clear milestone stages.", "Pause midway to verify your intermediate expressions against the problem constraints."],
                "4": ["Write each step on a fresh line with aligned equals signs.", "Explicitly verify signs whenever multiplying across brackets or moving terms across equality."],
                "5": ["Practice timed 30-minute sets of 5-mark and 3-mark questions.", "Avoid spending more than 4 minutes on any step without tangible progress during exam mocks."]
            }
        },
        "Physics": {
            "chapters": {
                "1": "Electric Charges and Fields", "2": "Electrostatic Potential and Capacitance",
                "3": "Current Electricity", "4": "Moving Charges and Magnetism",
                "5": "Magnetism and Matter", "6": "Electromagnetic Induction",
                "7": "Alternating Current", "8": "Electromagnetic Waves",
                "9": "Ray Optics", "10": "Wave Optics",
                "11": "Dual Nature of Radiation", "12": "Atoms", "13": "Nuclei", "14": "Semiconductor Electronics"
            },
            "topics": {
                "1": {"1": "Coulomb's Law & Superposition", "2": "Electric Field & Dipole", "3": "Gauss's Law & Applications"},
                "2": {"1": "Electric Potential & Equipotential", "2": "Capacitors & Dielectrics", "3": "Energy Stored in Capacitor"},
                "3": {"1": "Ohm's Law & Drift Velocity", "2": "Cells in Series & Parallel", "3": "Kirchhoff's Rules & Wheatstone Bridge"},
                "4": {"1": "Biot-Savart Law", "2": "Ampere's Circuital Law", "3": "Force on Moving Charge", "4": "Galvanometer"},
                "6": {"1": "Faraday's & Lenz's Law", "2": "Motional EMF", "3": "Self & Mutual Inductance"},
                "7": {"1": "Series LCR Circuit", "2": "Phasor Diagrams & Resonance", "3": "Transformers"},
                "9": {"1": "Refraction at Spherical Surfaces & Lenses", "2": "Lens Maker's Formula", "3": "Prism & Optical Instruments"},
                "10": {"1": "Huygens' Principle", "2": "Young's Double Slit Interference", "3": "Single Slit Diffraction"},
                "14": {"1": "p-n Junction Diode", "2": "Diode as Rectifier", "3": "Semiconductor Logic"}
            },
            "difficulties": {
                "1": "I struggle to visualize the physical concepts and field diagrams.",
                "2": "I know the theory but cannot derive standard formulas smoothly.",
                "3": "I cannot apply formulas correctly to multi-step numericals.",
                "4": "I get confused by sign conventions, directions (vectors), and units."
            },
            "advice": {
                "1": ["Always draw a clear, large diagram before starting any derivation or problem.", "Map out field lines, force vectors, and coordinate axes explicitly on paper."],
                "2": ["Learn the 3 core logical steps: Setup assumptions, Apply fundamental theorem, Integrate/Simplify.", "Practice writing key derivations with neat labeled sketches from memory."],
                "3": ["Extract all given physical values and convert immediately to SI units (m, kg, s, A, V, T).", "Identify the central governing law before choosing secondary formulas."],
                "4": ["Use right-hand rules consistently for cross products and magnetic field orientations.", "Define a single positive direction convention at the very beginning of the problem."]
            }
        },
        "Computer Science": {
            "chapters": {
                "1": "Python Revision Tour & Functions", "2": "File Handling (Text, Binary, CSV)",
                "3": "Data Structures (Stack)", "4": "Computer Networks",
                "5": "Database Management & SQL", "6": "Interface Python with MySQL"
            },
            "topics": {
                "1": {"1": "Scope of Variables & Functions", "2": "Default & Keyword Arguments", "3": "Recursion"},
                "2": {"1": "Text Files: read/write", "2": "Binary Files: pickle dump/load", "3": "CSV Files: reader/writer"},
                "3": {"1": "Stack Operations: Push/Pop using List", "2": "Underflow & Overflow Handling"},
                "4": {"1": "Transmission Media & Topologies", "2": "Network Devices & Protocols", "3": "Cyber Security & Case Studies"},
                "5": {"1": "DDL vs DML & Constraints", "2": "Aggregate Functions", "3": "GROUP BY, HAVING & ORDER BY", "4": "Table Joins"},
                "6": {"1": "Connecting Python with MySQL", "2": "Cursor & execute()", "3": "fetchall/fetchone", "4": "Commit & Transaction Handling"}
            },
            "difficulties": {
                "1": "I struggle with coding syntax, indentation, and logic building.",
                "2": "I find file handling (pickle/csv) or SQL cursor operations confusing.",
                "3": "I make silly errors in SQL queries (GROUP BY, HAVING, single vs double quotes).",
                "4": "I write code that errors out or cannot trace execution flow properly."
            },
            "advice": {
                "1": ["Trace your program manually on paper with a dry-run variable table before typing in an editor.", "Write code in modular chunks of 4-5 lines and test immediately."],
                "2": ["Remember the file handling lifecycle: Open -> Process -> Close.", "For binary files, always handle EOFError inside a try-except block when reading with pickle.load()."],
                "3": ["Memorize the exact clause order: SELECT -> FROM -> WHERE -> GROUP BY -> HAVING -> ORDER BY.", "Remember: WHERE filters records before grouping; HAVING filters aggregate groups."],
                "4": ["Read Python error messages carefully: IndexError and KeyError tell you the exact failing line and reason.", "Use deliberate print() statements to inspect variable values at intermediate points."]
            }
        }
    }
}
SUBJECT_DIAGNOSTIC_DATA["11"] = SUBJECT_DIAGNOSTIC_DATA["12"]
SUBJECT_DIAGNOSTIC_DATA["10"] = {
    "Maths": {
        "chapters": {
            "1": "Real Numbers", "2": "Polynomials", "3": "Pair of Linear Equations",
            "4": "Quadratic Equations", "5": "Arithmetic Progressions", "6": "Triangles",
            "7": "Coordinate Geometry", "8": "Introduction to Trigonometry", "9": "Circles",
            "10": "Surface Areas and Volumes", "11": "Statistics & Probability"
        },
        "topics": {
            "1": {"1": "Fundamental Theorem of Arithmetic", "2": "Irrational Numbers Proof"},
            "2": {"1": "Zeroes of Polynomials", "2": "Relationship between Zeroes and Coefficients"},
            "3": {"1": "Graphical Method", "2": "Substitution & Elimination Methods"},
            "4": {"1": "Standard Form", "2": "Quadratic Formula & Nature of Roots"},
            "6": {"1": "Basic Proportionality Theorem (BPT)", "2": "Criteria for Similarity (AAA, SSS, SAS)"},
            "8": {"1": "Trigonometric Ratios", "2": "Specific Angles (0, 30, 45, 60, 90)", "3": "Trigonometric Identities"}
        },
        "difficulties": {
            "1": "I do not understand the concept or proof.",
            "2": "I forget formulas and identities during tests.",
            "3": "I make calculation or sign mistakes.",
            "4": "I struggle to solve word problems or formulate equations."
        },
        "advice": {
            "1": ["Review the core definitions and work through 2 basic NCERT examples step by step."],
            "2": ["Maintain a dedicated formula notebook and write formulas daily from memory."],
            "3": ["Slow down your arithmetic steps and re-check signs carefully before writing answers."],
            "4": ["Identify the unknown, assign variable x, and translate statements into equations line by line."]
        }
    },
    "Science": {
        "chapters": {
            "1": "Chemical Reactions & Equations", "2": "Acids, Bases and Salts", "3": "Metals and Non-metals",
            "4": "Carbon and its Compounds", "5": "Life Processes", "6": "Control and Coordination",
            "7": "Reproduction", "8": "Heredity", "9": "Light - Reflection & Refraction",
            "10": "Electricity", "11": "Magnetic Effects of Electric Current"
        },
        "topics": {
            "1": {"1": "Balancing Chemical Equations", "2": "Types of Chemical Reactions"},
            "5": {"1": "Nutrition & Digestion", "2": "Respiration", "3": "Transportation & Blood Circulation", "4": "Excretion & Nephron Structure"},
            "9": {"1": "Spherical Mirrors & Mirror Formula", "2": "Refraction of Light & Snell's Law", "3": "Lenses & Lens Formula"}
        },
        "difficulties": {
            "1": "I do not understand the underlying concept or process.",
            "2": "I forget chemical equations, balances, or biological terms.",
            "3": "I get confused with ray diagrams, sign conventions, and numericals."
        },
        "advice": {
            "1": ["Study the process through neat diagrams and state reasons for each step."],
            "2": ["Practice writing balanced chemical equations daily; verify atom counts on LHS and RHS."],
            "3": ["Follow strict Cartesian sign conventions: distances measured against incident ray are always negative."]
        }
    }
}

@app.route("/subject/<subject_name>", methods=["GET", "POST"])
def subject_bridge(subject_name):
    cls = str(session.get("student_class", "12"))
    display_name = subject_name.replace("-", " ").title()
    
    class_data = SUBJECT_DIAGNOSTIC_DATA.get(cls, SUBJECT_DIAGNOSTIC_DATA.get("12", {}))
    subj_data = class_data.get(display_name, class_data.get("Chemistry", {}))
    
    chapters = subj_data.get("chapters", {})
    selected_chapter = request.form.get("chapter", "1")
    if selected_chapter not in chapters and chapters:
        selected_chapter = next(iter(chapters))
        
    topics = subj_data.get("topics", {}).get(selected_chapter, {})
    if not topics:
        topics = {"1": "Core Concepts & Fundamentals", "2": "Formulas, Definitions & Equations", "3": "Numerical Problems & Applications", "4": "Exam Board Practice & Trends"}
        
    selected_topic = request.form.get("topic", "1")
    if selected_topic not in topics and topics:
        selected_topic = next(iter(topics))
        
    difficulties = subj_data.get("difficulties", {
        "1": "I do not understand the core concept or theory.",
        "2": "I understand the concept but forget formulas/details.",
        "3": "I cannot solve numericals or apply formulas independently.",
        "4": "I make careless calculation, sign, or syntax mistakes."
    })
    
    if request.method == "POST" and request.form.get("submit_diagnostic"):
        selected_diff = request.form.get("difficulty", "1")
        advice_list = subj_data.get("advice", {}).get(selected_diff, [
            "Review the fundamental NCERT chapter summary thoroughly.",
            "Write down all key formulas and definitions on a one-page summary sheet.",
            "Solve 5 worked textbook examples before attempting unassisted exercises."
        ])
        
        # Save to database if available
        try:
            if Database is not None and hasattr(Database, "save_response"):
                Database.save_response(
                    Roll_no=session.get("roll", "101"),
                    Student_name=session.get("student_name", "Student"),
                    student_class=cls,
                    Student_Section=session.get("section", "A"),
                    subject=display_name,
                    chapter=chapters.get(selected_chapter, f"Chapter {selected_chapter}"),
                    topic=topics.get(selected_topic, f"Topic {selected_topic}"),
                    difficulty=selected_diff
                )
        except Exception:
            pass

        return render_template(
            "subject_result.html",
            profile=profile(),
            subject=display_name,
            chapter_name=chapters.get(selected_chapter, f"Chapter {selected_chapter}"),
            topic_name=topics.get(selected_topic, f"Topic {selected_topic}"),
            difficulty_name=difficulties.get(selected_diff, "General Friction"),
            advice_lines=advice_list
        )

    return render_template(
        "subject_diagnostic.html",
        profile=profile(),
        subject=display_name,
        chapters=chapters,
        selected_chapter=selected_chapter,
        topics=topics,
        selected_topic=selected_topic,
        difficulties=difficulties
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
        problem = str(session.get("general_problem", "")).strip()
        if not _session_profile_complete() or not problem:
            session.pop("general_diagnostic", None)
            flash("Your mentoring session is incomplete. Please start again from the student profile.", "error")
            return redirect(url_for("start"))

        severity = _diagnostic_severity(answers)
        # Store only compact diagnostic state in Flask's signed cookie session.
        # The full report is rebuilt on /report, avoiding oversized session cookies.
        session["general_diagnostic"] = {
            "topic_key": topic_key,
            "subtopic_key": subtopic_key,
            "problem": problem,
            "answers": [{"question": a["question"], "selected_option": a["selected_option"], "answer_text": a["answer_text"]} for a in answers],
            "why": why,
            "solution": solution,
            "severity_score": severity,
        }
        try:
            _, saved = build_result(topic_key, subtopic_key, problem, answers, why, solution, save=True)
        except (KeyError, TypeError, ValueError):
            session.pop("general_diagnostic", None)
            flash("I could not generate the mentor report safely. Please try the assessment again.", "error")
            return redirect(url_for("general_topics"))
        session["last_saved"] = bool(saved)
        return redirect(url_for("report"))
    return render_template("questions.html", profile=profile(), topic=data, questions=questions, topic_key=topic_key, subtopic_key=subtopic_key)

@app.route("/report")
def report():
    result, error = _report_from_session()
    if error:
        session.pop("general_diagnostic", None)
        flash(error, "error")
        return redirect(url_for("general_problem"))
    return render_template(
        "report.html", profile=profile(), result=result,
        saved=session.get("last_saved", False),
        severity_score=result.get("severity_score", 0),
    )

@app.route("/breathe")
@app.route("/breathing-exercise")
def breathing_exercise():
    return render_template("breathing.html", profile=profile())

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

@app.errorhandler(500)
def internal_error(error):
    flash("Something interrupted the mentoring flow. Please restart this pathway.", "error")
    return redirect(url_for("general_problem"))

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
