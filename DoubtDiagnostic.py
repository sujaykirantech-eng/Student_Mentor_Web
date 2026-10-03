"""
DoubtDiagnostic.py

A school-student academic doubt diagnostic system.

Purpose
-------
This module helps a Student Mentor understand WHY a student is struggling
with a topic and then recommends practical study methods.

Important:
- This is an academic support / mentoring system, not a medical or
  psychological diagnosis.
- It should not label students with disorders or make clinical claims.
- The questions are designed to identify learning barriers such as:
  concept gaps, prerequisite gaps, weak recall, poor application,
  question interpretation, insufficient practice, careless errors,
  time pressure, ineffective revision, confidence issues, distractions,
  language difficulty, and study-planning problems.
- The system is deliberately supportive and non-judgmental.

Usage
-----
    from DoubtDiagnostic import DoubtDiagnostic

    diagnostic = DoubtDiagnostic(
        previous_subject,
        previous_chapter,
        previous_topic,
        previous_difficulty
    )

    result = diagnostic.diagnose()

The returned dictionary contains the student's answers, identified
learning patterns, recommendations, action plan, and follow-up questions.
"""


class DoubtDiagnostic:

    VERSION = "2.0"

    # ==============================================================
    # CONSTRUCTOR
    # ==============================================================

    def __init__(
        self,
        subject,
        chapter,
        topic,
        previous_difficulty
    ):
        self.subject = subject
        self.chapter = chapter
        self.topic = topic
        self.previous_difficulty = previous_difficulty

        # Student responses
        self.reason = None
        self.when_stuck = None
        self.after_study = None
        self.prerequisite_choice = None
        self.prerequisite = None
        self.practice = None
        self.learning_condition = None
        self.independent = None
        self.exact_problem = None

        # Additional diagnostic information
        self.understanding_level = None
        self.recall_level = None
        self.application_level = None
        self.question_reading_level = None
        self.error_pattern = None
        self.revision_method = None
        self.time_pressure = None
        self.study_environment = None
        self.resource_problem = None
        self.language_problem = None
        self.confidence = None
        self.help_seeking = None
        self.study_consistency = None
        self.sleep_and_energy = None
        self.distraction_level = None
        self.goal_clarity = None
        self.exam_performance = None

        # Internal analysis
        self.patterns = []
        self.strengths = []
        self.advice = []
        self.priority_actions = []
        self.practice_plan = []
        self.revision_plan = []
        self.follow_up = []
        self.warnings = []

    # ==============================================================
    # BASIC INPUT HELPERS
    # ==============================================================

    def _ask_choice(self, question, options, valid=None):
        """
        Display a numbered question and return a valid answer.

        options:
            Dictionary such as {"1": "Concept", "2": "Practice"}
        """
        print("\n" + question)

        for number, text in options.items():
            print(f"{number}. {text}")

        if valid is None:
            valid = list(options.keys())

        answer = input("\nYour answer: ").strip()

        while answer not in valid:
            print("❌ Please choose one of the available options.")
            answer = input("Your answer: ").strip()

        return answer

    def _ask_text(self, question, allow_empty=False):
        """Ask an open-ended question."""
        print("\n" + question)
        answer = input("> ").strip()

        while not answer and not allow_empty:
            print("Please enter a short answer so I can understand the problem.")
            answer = input("> ").strip()

        return answer

    def _ask_yes_no(self, question):
        """Ask a simple yes/no question."""
        answer = input(f"\n{question} (yes/no): ").strip().lower()

        while answer not in ("yes", "no"):
            print("❌ Please enter yes or no.")
            answer = input("(yes/no): ").strip().lower()

        return answer

    # ==============================================================
    # INTRODUCTION
    # ==============================================================

    def show_previous_doubt(self):
        """Display the student's previous record."""
        print("\n==================================================")
        print("           🧠 PREVIOUS DOUBT REVIEW")
        print("==================================================")

        print(f"\nSubject    : {self.subject}")
        print(f"Chapter    : {self.chapter}")
        print(f"Topic      : {self.topic}")
        print(f"Previous difficulty:")
        print(f"{self.previous_difficulty}")

        print("\nWe're going to find the actual reason behind the difficulty.")
        print(
            "There is no 'good' or 'bad' answer here. "
            "The goal is to find the right study method."
        )

    # ==============================================================
    # CORE DIAGNOSTIC QUESTIONS
    # ==============================================================

    def ask_core_questions(self):
        """Ask the core questions required for every returning doubt."""

        self.reason = self._ask_choice(
            """
Q1. What is the MAIN problem right now?
""",
            {
                "1": "I don't understand the basic concept.",
                "2": "I understand it, but I forget it later.",
                "3": "I understand the concept, but I cannot solve questions.",
                "4": "I can solve basic questions, but difficult questions confuse me.",
                "5": "I struggle to understand what the question is asking.",
                "6": "A prerequisite concept is weak.",
                "7": "The way it was taught was not clear to me.",
                "8": "I know the method but make mistakes while solving.",
                "9": "I need structured revision and practice.",
                "10": "Something else."
            }
        )

        self.when_stuck = self._ask_choice(
            """
Q2. When do you usually get stuck?
""",
            {
                "1": "While learning the concept.",
                "2": "When recalling it without notes.",
                "3": "When starting a question.",
                "4": "Halfway through a question.",
                "5": "Only in difficult or unfamiliar questions.",
                "6": "During tests because of time pressure.",
                "7": "Mainly because of calculation/algebra mistakes."
            }
        )

        self.after_study = self._ask_choice(
            """
Q3. After studying this topic, which situation is closest to you?
""",
            {
                "1": "It makes sense while I read, but I cannot explain it later.",
                "2": "I can explain the idea but cannot apply it.",
                "3": "I can solve it after seeing an example.",
                "4": "I can solve easy questions but not mixed/hard ones.",
                "5": "I forget the steps after a few days.",
                "6": "I still don't understand what is happening."
            }
        )

        self.prerequisite_choice = self._ask_choice(
            """
Q4. Do you think a previous concept is stopping you?
""",
            {
                "1": "Yes, definitely.",
                "2": "Maybe, I'm not sure.",
                "3": "No."
            }
        )

        self.prerequisite = self._ask_text(
            """
If yes/maybe, which previous concept feels weak?
Type 'none' if there isn't one.
""",
            allow_empty=True
        )

        self.practice = self._ask_choice(
            """
Q5. How much have you practised this topic?
""",
            {
                "1": "Almost no questions.",
                "2": "Mostly examples that were already solved.",
                "3": "Basic questions.",
                "4": "Basic + moderate questions.",
                "5": "Difficult and mixed questions too."
            }
        )

        self.learning_condition = self._ask_choice(
            """
Q6. When this topic was taught, what best describes the situation?
""",
            {
                "1": "I was attentive and understood most of it.",
                "2": "I understood some parts but missed others.",
                "3": "It was taught too quickly for me.",
                "4": "I was distracted or unable to concentrate well.",
                "5": "I don't remember the explanation clearly."
            }
        )

        self.independent = self._ask_choice(
            """
Q7. If I give you a fresh question without hints, what happens?
""",
            {
                "1": "I can start and solve it.",
                "2": "I know the concept but don't know how to start.",
                "3": "I start correctly but get stuck.",
                "4": "I immediately look for the solution.",
                "5": "I don't know which concept is relevant."
            }
        )

        self.exact_problem = self._ask_text(
            """
Q8. In your own words, what EXACTLY is confusing you now?
Don't worry about using textbook language.
"""
        )

    # ==============================================================
    # DEEP LEARNING DIAGNOSTICS
    # ==============================================================

    def ask_understanding_questions(self):
        """Separate recognition from genuine understanding."""

        self.understanding_level = self._ask_choice(
            """
Q9. If you had to explain the topic to a friend without notes, what
would happen?
""",
            {
                "1": "I could explain it clearly.",
                "2": "I could explain the main idea but miss details.",
                "3": "I would remember some definitions/formulas only.",
                "4": "I would struggle to explain it.",
                "5": "I would not know where to begin."
            }
        )

        self.recall_level = self._ask_choice(
            """
Q10. How well can you recall the important ideas after a day or two?
""",
            {
                "1": "Almost everything important.",
                "2": "Most of it.",
                "3": "Only the main points.",
                "4": "Very little without notes.",
                "5": "Almost nothing."
            }
        )

        self.application_level = self._ask_choice(
            """
Q11. When the same concept appears in a new-looking question, what
usually happens?
""",
            {
                "1": "I recognise the concept and solve it.",
                "2": "I recognise it after thinking for a while.",
                "3": "I know the concept but cannot connect it to the question.",
                "4": "I usually copy the method from a similar example.",
                "5": "I cannot identify which concept to use."
            }
        )

        self.question_reading_level = self._ask_choice(
            """
Q12. What is your biggest problem with the wording of questions?
""",
            {
                "1": "No major problem.",
                "2": "Long questions confuse me.",
                "3": "I miss conditions or keywords.",
                "4": "I understand the words but not what is required.",
                "5": "I understand only after someone explains the question."
            }
        )

    def ask_error_diagnostics(self):
        """Identify the type of mistake instead of treating every mistake alike."""

        self.error_pattern = self._ask_choice(
            """
Q13. When you get a question wrong, which mistake happens most often?
""",
            {
                "1": "I used the wrong concept.",
                "2": "I remembered the concept/formula incorrectly.",
                "3": "I knew the method but made a calculation error.",
                "4": "I made an algebra/sign/substitution mistake.",
                "5": "I misunderstood the question.",
                "6": "I skipped a condition or important detail.",
                "7": "I ran out of time.",
                "8": "I rarely analyse my mistakes."
            }
        )

        self.revision_method = self._ask_choice(
            """
Q14. How do you usually revise?
""",
            {
                "1": "Mostly rereading notes/textbook.",
                "2": "Reading and highlighting.",
                "3": "Memorising formulas/definitions.",
                "4": "Solving questions from memory.",
                "5": "Active recall + questions + mistake analysis.",
                "6": "I usually revise only before a test.",
                "7": "I don't have a fixed revision method."
            }
        )

    # ==============================================================
    # EXAM + TIME DIAGNOSTICS
    # ==============================================================

    def ask_exam_diagnostics(self):
        """Identify whether the problem changes under test conditions."""

        self.time_pressure = self._ask_choice(
            """
Q15. How does time affect your performance on this topic?
""",
            {
                "1": "Time is not a problem.",
                "2": "I am slightly slow.",
                "3": "I understand the questions but take too long.",
                "4": "I panic/rush when time is running out.",
                "5": "I spend too long on one difficult question.",
                "6": "I don't know how to divide my time."
            }
        )

        self.exam_performance = self._ask_choice(
            """
Q16. Which statement best describes your test performance?
""",
            {
                "1": "I perform about as well as I do while practising.",
                "2": "I know the material but make more mistakes in tests.",
                "3": "I understand after the test, but couldn't solve during it.",
                "4": "I leave questions because I get stuck too long.",
                "5": "I perform well in familiar questions but struggle with new ones.",
                "6": "I need much more preparation before tests."
            }
        )

    # ==============================================================
    # STUDY ENVIRONMENT + HABITS
    # ==============================================================

    def ask_study_diagnostics(self):
        """Explore practical study barriers."""

        self.study_environment = self._ask_choice(
            """
Q17. What is the biggest problem with your study environment?
""",
            {
                "1": "No major problem.",
                "2": "Phone/social-media distractions.",
                "3": "Noise or interruptions.",
                "4": "I keep switching between subjects/resources.",
                "5": "I start studying but lose focus quickly.",
                "6": "I don't have a clear study plan."
            }
        )

        self.distraction_level = self._ask_choice(
            """
Q18. During a normal study session, how often do you lose focus?
""",
            {
                "1": "Rarely.",
                "2": "Sometimes.",
                "3": "Several times.",
                "4": "Very frequently.",
                "5": "I struggle to maintain a session at all."
            }
        )

        self.study_consistency = self._ask_choice(
            """
Q19. How consistently do you study this subject?
""",
            {
                "1": "Almost every planned day.",
                "2": "Most days.",
                "3": "Only when there is homework/test pressure.",
                "4": "Irregularly.",
                "5": "I keep postponing it."
            }
        )

        self.goal_clarity = self._ask_choice(
            """
Q20. Do you have a clear target for what you want to achieve in this topic?
""",
            {
                "1": "Yes, very clear.",
                "2": "Somewhat clear.",
                "3": "Not really.",
                "4": "I mainly want to finish it.",
                "5": "I don't know what level I should reach."
            }
        )

    # ==============================================================
    # RESOURCES + COMMUNICATION
    # ==============================================================

    def ask_resource_diagnostics(self):
        """Find whether the problem is caused by explanation/resources."""

        self.resource_problem = self._ask_choice(
            """
Q21. How do you currently learn this topic?
""",
            {
                "1": "School explanation + textbook.",
                "2": "Textbook + my own notes.",
                "3": "Video/online explanation.",
                "4": "Multiple resources.",
                "5": "Mostly from solved answers.",
                "6": "I don't have a reliable explanation yet."
            }
        )

        self.language_problem = self._ask_choice(
            """
Q22. Does language or terminology make this topic harder?
""",
            {
                "1": "No.",
                "2": "Sometimes unfamiliar words slow me down.",
                "3": "Some textbook language is difficult.",
                "4": "I understand the idea better when it is explained simply.",
                "5": "Language is a major barrier for this topic."
            }
        )

        self.help_seeking = self._ask_choice(
            """
Q23. When you are stuck, what do you normally do?
""",
            {
                "1": "Try independently and then ask for help.",
                "2": "Ask a teacher/friend quickly.",
                "3": "Search for a solution immediately.",
                "4": "Keep trying without changing strategy.",
                "5": "Skip the question/topic.",
                "6": "I don't usually ask anyone."
            }
        )

    # ==============================================================
    # CONFIDENCE + LEARNING ATTITUDE
    # ==============================================================

    def ask_confidence_diagnostics(self):
        """
        Ask about academic confidence without diagnosing mental-health
        conditions.
        """

        self.confidence = self._ask_choice(
            """
Q24. When you see a difficult question from this topic, what is your
usual reaction?
""",
            {
                "1": "I am curious and try to break it down.",
                "2": "I feel challenged but keep trying.",
                "3": "I become unsure about where to start.",
                "4": "I quickly assume I probably cannot solve it.",
                "5": "I avoid it until I absolutely have to do it."
            }
        )

        self.sleep_and_energy = self._ask_choice(
            """
Q25. When do you usually study this topic?
""",
            {
                "1": "When I am generally alert.",
                "2": "At different times depending on the day.",
                "3": "Mostly when I am already tired.",
                "4": "Late at night because I postpone it.",
                "5": "I don't have a regular time."
            }
        )

    # ==============================================================
    # SUBJECT-SPECIFIC DIAGNOSTICS
    # ==============================================================

    def ask_subject_specific(self):
        """
        Ask one subject-tailored question.

        This is academic rather than clinical. It helps the mentor choose
        a useful method for the subject.
        """

        subject = str(self.subject).strip().lower()

        if "math" in subject:
            answer = self._ask_choice(
                """
Q26. For this Maths topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding the theorem/formula/concept.",
                    "2": "Knowing which method to choose.",
                    "3": "Setting up the problem correctly.",
                    "4": "Algebra/calculation.",
                    "5": "Multi-step or unfamiliar problems.",
                    "6": "Proof/derivation/reasoning."
                }
            )

        elif "physics" in subject:
            answer = self._ask_choice(
                """
Q26. For this Physics topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding the physical concept.",
                    "2": "Identifying the correct law/principle.",
                    "3": "Drawing/visualising the situation.",
                    "4": "Setting up equations.",
                    "5": "Mathematical calculation.",
                    "6": "Multi-concept numerical problems."
                }
            )

        elif "chem" in subject:
            answer = self._ask_choice(
                """
Q26. For this Chemistry topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding the concept.",
                    "2": "Remembering reactions/facts.",
                    "3": "Applying concepts to problems.",
                    "4": "Organic reaction mechanism/reasoning.",
                    "5": "Physical chemistry calculations.",
                    "6": "Inorganic trends/facts."
                }
            )

        elif "bio" in subject:
            answer = self._ask_choice(
                """
Q26. For this Biology topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding the process.",
                    "2": "Remembering terminology.",
                    "3": "Connecting different concepts.",
                    "4": "Diagrams/labelled structures.",
                    "5": "Application-based questions.",
                    "6": "Long-answer organisation."
                }
            )

        elif "computer" in subject or "cs" in subject:
            answer = self._ask_choice(
                """
Q26. For this Computer Science topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding programming logic.",
                    "2": "Syntax.",
                    "3": "Tracing/debugging code.",
                    "4": "Writing code independently.",
                    "5": "Algorithms/problem decomposition.",
                    "6": "Theory/database/network concepts."
                }
            )

        elif "english" in subject:
            answer = self._ask_choice(
                """
Q26. For this English topic, where does the difficulty usually occur?
""",
                {
                    "1": "Grammar rules.",
                    "2": "Applying grammar in questions.",
                    "3": "Vocabulary/meaning.",
                    "4": "Reading comprehension.",
                    "5": "Writing structure/content.",
                    "6": "Time management in English exams."
                }
            )

        elif "social" in subject:
            answer = self._ask_choice(
                """
Q26. For this Social Science topic, where does the difficulty usually occur?
""",
                {
                    "1": "Understanding the chapter.",
                    "2": "Remembering facts/dates/terms.",
                    "3": "Connecting causes and effects.",
                    "4": "Map/data/source-based questions.",
                    "5": "Writing long answers.",
                    "6": "Distinguishing similar concepts."
                }
            )

        else:
            answer = self._ask_choice(
                """
Q26. Which part of this subject is most difficult?
""",
                {
                    "1": "Understanding.",
                    "2": "Remembering.",
                    "3": "Applying.",
                    "4": "Question interpretation.",
                    "5": "Practice.",
                    "6": "Exam performance."
                }
            )

        self.subject_specific = answer

    # ==============================================================
    # OPEN REFLECTION
    # ==============================================================

    def ask_final_reflection(self):
        """Give the student space to identify the real issue themselves."""

        self.final_reflection = self._ask_text(
            """
Q27. If you could change ONE thing about the way you currently study
this topic, what would you change?
"""
        )

        self.support_needed = self._ask_text(
            """
Q28. What kind of help would be most useful right now?
For example: simpler explanation, worked example, practice questions,
revision plan, error analysis, or exam strategy.
"""
        )

    # ==============================================================
    # ANALYSIS ENGINE
    # ==============================================================

    def _add_pattern(self, pattern):
        if pattern not in self.patterns:
            self.patterns.append(pattern)

    def _add_advice(self, advice):
        if advice not in self.advice:
            self.advice.append(advice)

    def _add_action(self, action):
        if action not in self.priority_actions:
            self.priority_actions.append(action)

    def analyse(self):
        """
        Convert responses into learning patterns and practical
        recommendations.

        This does NOT diagnose a mental-health condition.
        """

        self.patterns = []
        self.strengths = []
        self.advice = []
        self.priority_actions = []
        self.practice_plan = []
        self.revision_plan = []
        self.follow_up = []
        self.warnings = []

        # ----------------------------------------------------------
        # MAIN REASON
        # ----------------------------------------------------------

        if self.reason == "1":
            self._add_pattern("Foundational concept gap")

            self._add_advice(
                "Rebuild the topic from the simplest meaningful idea "
                "before attempting difficult questions."
            )

            self._add_action(
                "Write the core definition/principle in your own words."
            )

            self._add_action(
                "Solve 3 very basic questions before moving upward."
            )

        elif self.reason == "2":
            self._add_pattern("Recall/retention gap")

            self._add_advice(
                "Replace repeated rereading with active recall."
            )

            self._add_advice(
                "Use spaced revision: recall the topic after a gap instead "
                "of revising everything in one sitting."
            )

            self._add_action(
                "Close the book and reproduce the key ideas from memory."
            )

        elif self.reason == "3":
            self._add_pattern("Application gap")

            self._add_advice(
                "Use the progression: worked example → guided problem → "
                "independent problem."
            )

            self._add_advice(
                "When stuck, identify the given information, required "
                "quantity, and relevant principle before looking at a solution."
            )

            self._add_action(
                "Solve one fresh question without looking at an example."
            )

        elif self.reason == "4":
            self._add_pattern("Difficulty-transfer gap")

            self._add_advice(
                "Gradually increase difficulty instead of jumping from easy "
                "questions directly to the hardest ones."
            )

            self._add_advice(
                "Practise mixed questions so you must recognise the method "
                "yourself."
            )

            self._add_action(
                "Choose one moderate and one difficult question and analyse "
                "where the reasoning changes."
            )

        elif self.reason == "5":
            self._add_pattern("Question interpretation gap")

            self._add_advice(
                "Before solving, write: GIVEN → REQUIRED → RELEVANT CONCEPT."
            )

            self._add_advice(
                "Underline conditions, units, keywords, and restrictions."
            )

            self._add_action(
                "Practise translating five questions into your own words "
                "without solving them immediately."
            )

        elif self.reason == "6":
            self._add_pattern("Prerequisite gap")

            self._add_advice(
                "Repair the prerequisite first rather than repeatedly "
                "attacking the current topic."
            )

            self._add_action(
                f"Spend one short session revising: {self.prerequisite}."
            )

        elif self.reason == "7":
            self._add_pattern("Explanation mismatch")

            self._add_advice(
                "Try a second explanation using a different representation "
                "or example."
            )

            self._add_advice(
                "Immediately test the new explanation with a fresh question."
            )

            self._add_action(
                "Write down the exact sentence/step that became unclear."
            )

        elif self.reason == "8":
            self._add_pattern("Execution/error-control gap")

            self._add_advice(
                "Keep an error log instead of simply marking answers wrong."
            )

            self._add_advice(
                "Classify each mistake before correcting it."
            )

            self._add_action(
                "Reattempt one previously wrong question without seeing "
                "the solution."
            )

        elif self.reason == "9":
            self._add_pattern("Study-structure gap")

            self._add_advice(
                "Use the cycle: learn → recall → practise → analyse → reattempt."
            )

            self._add_action(
                "Divide the topic into small subtopics and assign a clear "
                "target to each session."
            )

        else:
            self._add_pattern("Unclassified learning barrier")

            self._add_advice(
                "Use the student's own description to locate the exact "
                "point where understanding breaks."
            )

        # ----------------------------------------------------------
        # AFTER-STUDY ANALYSIS
        # ----------------------------------------------------------

        if self.after_study == "1":
            self._add_pattern("Recognition without reliable recall")

            self._add_advice(
                "Use the closed-book teach-back method: explain the topic "
                "aloud without looking at notes."
            )

        elif self.after_study == "2":
            self._add_pattern("Concept-to-application gap")

            self._add_advice(
                "After learning each concept, immediately solve one fresh "
                "application question."
            )

        elif self.after_study == "3":
            self._add_pattern("Example dependence")

            self._add_advice(
                "Hide the worked example before attempting the next question."
            )

        elif self.after_study == "4":
            self._add_pattern("Difficulty progression gap")

            self._add_advice(
                "Introduce mixed practice and progressively harder questions."
            )

        elif self.after_study == "5":
            self._add_pattern("Retention gap")

            self._add_advice(
                "Use spaced retrieval rather than a single long revision."
            )

        elif self.after_study == "6":
            self._add_pattern("Foundational understanding gap")

            self._add_advice(
                "Return to the simplest representation of the concept and "
                "rebuild step by step."
            )

        # ----------------------------------------------------------
        # UNDERSTANDING
        # ----------------------------------------------------------

        if self.understanding_level in ["4", "5"]:
            self._add_pattern("Low explainability")

            self._add_advice(
                "Use teach-back: if you cannot explain a concept simply, "
                "identify the exact part you cannot explain."
            )

        elif self.understanding_level == "1":
            self.strengths.append("Can explain the topic independently.")

        # ----------------------------------------------------------
        # RECALL
        # ----------------------------------------------------------

        if self.recall_level in ["4", "5"]:
            self._add_pattern("Weak retrieval")

            self._add_advice(
                "Use short closed-book recall sessions instead of repeatedly "
                "reading the same page."
            )

            self._add_action(
                "Create 5-10 recall prompts for this topic."
            )

        elif self.recall_level in ["1", "2"]:
            self.strengths.append("Reasonably strong recall.")

        # ----------------------------------------------------------
        # APPLICATION
        # ----------------------------------------------------------

        if self.application_level in ["3", "4", "5"]:
            self._add_pattern("Transfer/application difficulty")

            self._add_advice(
                "Practise recognising which principle applies before doing "
                "the calculations or writing the final answer."
            )

        elif self.application_level == "1":
            self.strengths.append("Can transfer the concept to new questions.")

        # ----------------------------------------------------------
        # QUESTION READING
        # ----------------------------------------------------------

        if self.question_reading_level in ["3", "4", "5"]:
            self._add_pattern("Question decoding difficulty")

            self._add_advice(
                "Separate reading from solving: first identify given data, "
                "required result, conditions, and likely concept."
            )

            self._add_action(
                "Do a short set of question-interpretation-only exercises."
            )

        # ----------------------------------------------------------
        # ERROR ANALYSIS
        # ----------------------------------------------------------

        if self.error_pattern == "1":
            self._add_pattern("Concept selection error")

            self._add_advice(
                "Before solving, name the principle you intend to use and "
                "briefly explain why it applies."
            )

        elif self.error_pattern == "2":
            self._add_pattern("Formula/fact recall error")

            self._add_advice(
                "Use active recall and spaced review for formulas, "
                "definitions, reactions, terms, or rules."
            )

        elif self.error_pattern in ["3", "4"]:
            self._add_pattern("Execution error")

            self._add_advice(
                "Maintain a mistake log and identify the exact operation "
                "where the error entered."
            )

        elif self.error_pattern == "5":
            self._add_pattern("Question interpretation error")

            self._add_advice(
                "Rewrite the question in your own words before calculating."
            )

        elif self.error_pattern == "6":
            self._add_pattern("Condition/detail omission")

            self._add_advice(
                "Create a final checklist for conditions, units, signs, "
                "labels, and requested quantities."
            )

        elif self.error_pattern == "7":
            self._add_pattern("Time-management issue")

            self._add_advice(
                "Practise with controlled time limits only after the underlying "
                "method is reasonably secure."
            )

        elif self.error_pattern == "8":
            self._add_pattern("Insufficient mistake analysis")

            self._add_advice(
                "For every wrong answer, record the cause and reattempt the "
                "question later."
            )

        # ----------------------------------------------------------
        # PREREQUISITE
        # ----------------------------------------------------------

        if (
            self.prerequisite_choice in ["1", "2"]
            and self.prerequisite
            and self.prerequisite.lower() != "none"
        ):
            self._add_pattern("Possible prerequisite weakness")

            self._add_action(
                f"Review the prerequisite '{self.prerequisite}' before "
                f"restarting '{self.topic}'."
            )

        # ----------------------------------------------------------
        # PRACTICE
        # ----------------------------------------------------------

        if self.practice in ["1", "2"]:
            self._add_pattern("Insufficient active practice")

            self._add_advice(
                "Increase question practice gradually rather than attempting "
                "the hardest problems immediately."
            )

        elif self.practice == "5":
            self.strengths.append("Has substantial practice exposure.")

            self._add_advice(
                "Because practice volume is already high, focus on quality: "
                "mistake analysis, mixed practice, and reattempts."
            )

        # ----------------------------------------------------------
        # LEARNING CONDITION
        # ----------------------------------------------------------

        if self.learning_condition in ["3", "4", "5"]:
            self._add_pattern("Learning-condition/explanation issue")

            self._add_advice(
                "Relearn the topic in a focused session using a clear "
                "explanation and active recall."
            )

        # ----------------------------------------------------------
        # INDEPENDENT SOLVING
        # ----------------------------------------------------------

        if self.independent == "2":
            self._add_pattern("Starting-point difficulty")

            self._add_advice(
                "Use a three-question start routine: What is given? What is "
                "required? What concept could connect them?"
            )

        elif self.independent == "3":
            self._add_pattern("Mid-solution reasoning gap")

            self._add_advice(
                "When stuck, identify the last correct step and determine "
                "what information is missing for the next step."
            )

        elif self.independent == "4":
            self._add_pattern("Solution dependence")

            self._add_advice(
                "Delay solution checking. Give yourself a fixed attempt "
                "period, then check only the next step rather than the whole answer."
            )

        elif self.independent == "5":
            self._add_pattern("Concept-recognition difficulty")

            self._add_advice(
                "Practise mixed questions where the topic or method is not "
                "announced beforehand."
            )

        # ----------------------------------------------------------
        # REVISION
        # ----------------------------------------------------------

        if self.revision_method in ["1", "2", "3", "6", "7"]:
            self._add_pattern("Passive or irregular revision")

            self._add_advice(
                "Upgrade revision to active recall + practice + mistake analysis."
            )

            self.revision_plan.extend([
                "Recall key ideas without notes.",
                "Solve a few questions.",
                "Analyse mistakes.",
                "Reattempt wrong questions after a gap."
            ])

        else:
            self.revision_plan.extend([
                "Recall the key ideas.",
                "Use mixed practice.",
                "Analyse mistakes.",
                "Reattempt difficult questions later."
            ])

        # ----------------------------------------------------------
        # TIME
        # ----------------------------------------------------------

        if self.time_pressure in ["3", "4", "5", "6"]:
            self._add_pattern("Time-management pressure")

            self._add_advice(
                "Do not use speed practice as a replacement for understanding. "
                "First become accurate, then gradually introduce time limits."
            )

            self.practice_plan.append(
                "Use a short timed set after accuracy improves."
            )

        # ----------------------------------------------------------
        # EXAM PERFORMANCE
        # ----------------------------------------------------------

        if self.exam_performance in ["2", "3", "4"]:
            self._add_pattern("Exam-transfer issue")

            self._add_advice(
                "Include timed mixed practice so you practise choosing and "
                "applying methods under realistic conditions."
            )

        elif self.exam_performance == "5":
            self._add_pattern("Unfamiliar-question transfer issue")

            self._add_advice(
                "Practise mixed and unfamiliar questions instead of only "
                "repeating predictable examples."
            )

        # ----------------------------------------------------------
        # ENVIRONMENT
        # ----------------------------------------------------------

        if self.study_environment == "2":
            self._add_pattern("Digital distraction")

            self._add_advice(
                "During a study block, keep unnecessary notifications and "
                "distractions away from the immediate workspace."
            )

        elif self.study_environment == "3":
            self._add_pattern("Environmental interruption")

            self._add_advice(
                "Use the quietest practical study location and shorter "
                "focused sessions when interruptions cannot be avoided."
            )

        elif self.study_environment == "4":
            self._add_pattern("Resource switching")

            self._add_advice(
                "Choose one primary explanation/resource for the session and "
                "use additional resources only when a specific gap remains."
            )

        elif self.study_environment == "5":
            self._add_pattern("Focus-session difficulty")

            self._add_advice(
                "Start with a short, clearly defined study block and one "
                "specific target rather than trying to study indefinitely."
            )

        elif self.study_environment == "6":
            self._add_pattern("Planning gap")

            self._add_advice(
                "Set a concrete target for every session: one concept, "
                "a number of questions, or one error category."
            )

        # ----------------------------------------------------------
        # CONSISTENCY
        # ----------------------------------------------------------

        if self.study_consistency in ["4", "5"]:
            self._add_pattern("Inconsistent study routine")

            self._add_advice(
                "Use smaller, repeatable study sessions rather than waiting "
                "for a large amount of free time."
            )

        # ----------------------------------------------------------
        # RESOURCE
        # ----------------------------------------------------------

        if self.resource_problem == "4":
            self._add_pattern("Too many resources")

            self._add_advice(
                "Avoid resource overload. Master one clear explanation first, "
                "then use another source only for unresolved points."
            )

        elif self.resource_problem == "5":
            self._add_pattern("Over-reliance on solutions")

            self._add_advice(
                "Attempt questions before viewing solutions and reproduce "
                "the reasoning after checking."
            )

        elif self.resource_problem == "6":
            self._add_pattern("Lack of reliable explanation")

            self._add_advice(
                "Find one clear explanation and verify it through active "
                "recall and fresh questions."
            )

        # ----------------------------------------------------------
        # LANGUAGE
        # ----------------------------------------------------------

        if self.language_problem in ["3", "4", "5"]:
            self._add_pattern("Terminology/language barrier")

            self._add_advice(
                "Create a small glossary in your own words. Do not memorise "
                "a difficult sentence when you can first understand its meaning."
            )

        # ----------------------------------------------------------
        # HELP SEEKING
        # ----------------------------------------------------------

        if self.help_seeking == "3":
            self._add_pattern("Premature solution checking")

            self._add_advice(
                "Try independently first. If stuck, inspect only the next "
                "useful hint rather than the complete solution."
            )

        elif self.help_seeking == "5":
            self._add_pattern("Avoidance of difficult questions")

            self._add_advice(
                "Break difficult questions into smaller steps and treat "
                "mistakes as information about what to practise next."
            )

        elif self.help_seeking == "6":
            self._add_pattern("Low help-seeking")

            self._add_advice(
                "When a doubt remains after a genuine attempt, asking a "
                "teacher, mentor, or trusted classmate is a productive study skill."
            )

        # ----------------------------------------------------------
        # CONFIDENCE
        # ----------------------------------------------------------

        if self.confidence in ["4", "5"]:
            self._add_pattern("Avoidance response to difficulty")

            self._add_advice(
                "Start with a manageable question, then increase difficulty "
                "gradually. Confidence should come from repeated successful "
                "attempts, not from avoiding hard questions."
            )

        elif self.confidence in ["1", "2"]:
            self.strengths.append(
                "Shows willingness to engage with difficult questions."
            )

        # ----------------------------------------------------------
        # SLEEP / ENERGY
        # ----------------------------------------------------------

        if self.sleep_and_energy in ["3", "4"]:
            self._add_pattern("Study timing may be reducing efficiency")

            self._add_advice(
                "Where possible, schedule demanding learning when you are "
                "more alert instead of relying on exhausted last-minute study."
            )

        # ----------------------------------------------------------
        # SUBJECT-SPECIFIC METHOD
        # ----------------------------------------------------------

        self._generate_subject_strategy()

        # ----------------------------------------------------------
        # PRACTICE PLAN
        # ----------------------------------------------------------

        self._generate_practice_plan()

        # ----------------------------------------------------------
        # FOLLOW-UP
        # ----------------------------------------------------------

        self._generate_follow_up()

    # ==============================================================
    # SUBJECT STRATEGY
    # ==============================================================

    def _generate_subject_strategy(self):
        """Add subject-specific methods."""

        subject = str(self.subject).lower()

        if "math" in subject:
            self._add_advice(
                "Maths method: understand the principle, identify the "
                "question type, solve without looking, then analyse the error."
            )

            self.practice_plan.extend([
                "1 easy question to verify the concept.",
                "2 moderate questions with different wording.",
                "1 challenging/mixed question.",
                "Reattempt the hardest question later without notes."
            ])

        elif "physics" in subject:
            self._add_advice(
                "Physics method: visualise the situation, list given data, "
                "identify the law/principle, build equations, then calculate."
            )

            self.practice_plan.extend([
                "Draw a diagram or mental model where appropriate.",
                "Write given and required quantities.",
                "State the physical principle before substituting values.",
                "Check units and physical reasonableness."
            ])

        elif "chem" in subject:
            self._add_advice(
                "Chemistry method: separate understanding from memorisation "
                "and use the correct practice style for the topic."
            )

            self.practice_plan.extend([
                "Conceptual topic: explain the mechanism/trend in your own words.",
                "Reaction-based topic: recall the transformation before checking.",
                "Numerical topic: practise setup before speed.",
                "Fact-heavy topic: use spaced active recall."
            ])

        elif "bio" in subject:
            self._add_advice(
                "Biology method: understand the process first, then use "
                "active recall, diagrams, comparison tables, and application questions."
            )

            self.practice_plan.extend([
                "Explain the process without notes.",
                "Draw the relevant diagram from memory where appropriate.",
                "Recall key terminology.",
                "Answer one application-based question."
            ])

        elif "computer" in subject or "cs" in subject:
            self._add_advice(
                "Computer Science method: don't only read code. Predict the "
                "output, trace variables, write small programs, debug, and "
                "then solve a fresh problem independently."
            )

            self.practice_plan.extend([
                "Trace a short program manually.",
                "Change one part and predict the new output.",
                "Write a small program without copying.",
                "Debug one deliberately imperfect program.",
                "Solve one fresh problem from a blank editor."
            ])

        elif "english" in subject:
            self._add_advice(
                "English method: practise the skill, not just the rule. "
                "For grammar, learn the rule briefly and apply it immediately; "
                "for writing, practise structure, clarity, and time control."
            )

            self.practice_plan.extend([
                "Review the grammar rule briefly.",
                "Solve application questions without looking at the rule.",
                "Analyse every wrong answer and identify the rule involved.",
                "Practise one timed writing task when appropriate."
            ])

        elif "social" in subject:
            self._add_advice(
                "Social Science method: organise information by cause, "
                "effect, sequence, comparison, significance, and evidence "
                "rather than memorising disconnected sentences."
            )

            self.practice_plan.extend([
                "Build a chapter concept map.",
                "Recall major facts without notes.",
                "Practise cause/effect and comparison questions.",
                "Write one structured long answer."
            ])

        else:
            self._add_advice(
                "Use a subject-neutral cycle: understand → recall → "
                "apply → analyse mistakes → reattempt."
            )

    # ==============================================================
    # PRACTICE PLAN
    # ==============================================================

    def _generate_practice_plan(self):
        """Create a flexible practice sequence."""

        if not self.practice_plan:
            self.practice_plan = [
                "Review the core idea briefly.",
                "Recall it without notes.",
                "Solve a basic question.",
                "Solve a moderate question.",
                "Analyse mistakes.",
                "Reattempt one wrong question later."
            ]

        # Remove duplicate entries while keeping order.
        self.practice_plan = list(dict.fromkeys(self.practice_plan))

    # ==============================================================
    # FOLLOW-UP
    # ==============================================================

    def _generate_follow_up(self):
        """Generate questions for the next mentor interaction."""

        self.follow_up = [
            "Can you explain the concept now without looking at your notes?",
            "Can you solve one fresh basic question independently?",
            "What was the exact step that previously caused the problem?",
            "Which mistake should you watch for next time?",
            "Has the difficulty changed from understanding to application?"
        ]

    # ==============================================================
    # ACTION PLAN
    # ==============================================================

    def build_action_plan(self):
        """
        Convert diagnosis into a practical immediate plan.

        The plan deliberately avoids unrealistic promises and focuses on
        observable study actions.
        """

        if not self.priority_actions:
            self.priority_actions = [
                "Identify the exact weak point.",
                "Review it briefly.",
                "Recall it without notes.",
                "Solve a fresh question.",
                "Analyse the result."
            ]

        return self.priority_actions[:]

    # ==============================================================
    # STUDENT-FRIENDLY SUMMARY
    # ==============================================================

    def display_diagnosis(self):
        """Print a complete student-friendly report."""

        print("\n")
        print("==================================================")
        print("             🔍 YOUR STUDY DIAGNOSIS")
        print("==================================================")

        print(f"\nSubject : {self.subject}")
        print(f"Chapter : {self.chapter}")
        print(f"Topic   : {self.topic}")

        print("\nWhat seems to be happening:")

        if self.patterns:
            for number, pattern in enumerate(self.patterns, start=1):
                print(f"{number}. {pattern}")
        else:
            print("No single dominant pattern was identified.")

        if self.strengths:
            print("\n💪 Strengths identified:")

            for strength in self.strengths:
                print(f"• {strength}")

        print("\n🧠 Recommended methods:")

        for number, advice in enumerate(self.advice, start=1):
            print(f"\n{number}. {advice}")

        print("\n==================================================")
        print("               🎯 ACTION PLAN")
        print("==================================================")

        for number, action in enumerate(self.build_action_plan(), start=1):
            print(f"{number}. {action}")

        print("\n==================================================")
        print("              📚 PRACTICE METHOD")
        print("==================================================")

        for number, item in enumerate(self.practice_plan, start=1):
            print(f"{number}. {item}")

        print("\n==================================================")
        print("              🔄 NEXT CHECK-IN")
        print("==================================================")

        for number, question in enumerate(self.follow_up, start=1):
            print(f"{number}. {question}")

        print("\n==================================================")
        print("     Remember: difficulty is information, not a label.")
        print("==================================================")

    # ==============================================================
    # RESULT OBJECT
    # ==============================================================

    def get_result(self):
        """Return all useful diagnostic data as a dictionary."""

        return {
            "diagnostic_version": self.VERSION,

            "previous_doubt": {
                "subject": self.subject,
                "chapter": self.chapter,
                "topic": self.topic,
                "difficulty": self.previous_difficulty
            },

            "responses": {
                "main_reason": self.reason,
                "when_stuck": self.when_stuck,
                "after_study": self.after_study,
                "prerequisite_choice": self.prerequisite_choice,
                "prerequisite": self.prerequisite,
                "practice": self.practice,
                "learning_condition": self.learning_condition,
                "independent_solving": self.independent,
                "exact_problem": self.exact_problem,
                "understanding": self.understanding_level,
                "recall": self.recall_level,
                "application": self.application_level,
                "question_reading": self.question_reading_level,
                "error_pattern": self.error_pattern,
                "revision_method": self.revision_method,
                "time_pressure": self.time_pressure,
                "exam_performance": self.exam_performance,
                "study_environment": self.study_environment,
                "distraction_level": self.distraction_level,
                "study_consistency": self.study_consistency,
                "goal_clarity": self.goal_clarity,
                "resource_problem": self.resource_problem,
                "language_problem": self.language_problem,
                "help_seeking": self.help_seeking,
                "confidence": self.confidence,
                "study_timing": self.sleep_and_energy,
                "subject_specific": getattr(self, "subject_specific", None),
                "final_reflection": getattr(self, "final_reflection", None),
                "support_needed": getattr(self, "support_needed", None)
            },

            "analysis": {
                "patterns": self.patterns,
                "strengths": self.strengths
            },

            "recommendations": self.advice,

            "action_plan": self.priority_actions,

            "practice_plan": self.practice_plan,

            "revision_plan": self.revision_plan,

            "follow_up_questions": self.follow_up,

            "warnings": self.warnings
        }

    # ==============================================================
    # MAIN DIAGNOSTIC FLOW
    # ==============================================================

    def diagnose(self):
        """
        Run the complete adaptive academic diagnostic.

        Returns:
            dict containing responses, analysis, advice, plans and
            follow-up questions.
        """

        self.show_previous_doubt()

        print("\nThis will take a little longer than a normal doubt check.")
        print(
            "That's intentional: the goal is to find the cause instead "
            "of giving random advice."
        )

        self.ask_core_questions()
        self.ask_understanding_questions()
        self.ask_error_diagnostics()
        self.ask_exam_diagnostics()
        self.ask_study_diagnostics()
        self.ask_resource_diagnostics()
        self.ask_confidence_diagnostics()
        self.ask_subject_specific()
        self.ask_final_reflection()

        self.analyse()
        self.display_diagnosis()

        return self.get_result()


# ==============================================================
# OPTIONAL QUICK TEST
# ==============================================================

if __name__ == "__main__":

    print("==================================================")
    print("          DOUBT DIAGNOSTIC TEST MODE")
    print("==================================================")

    print("\nThis test runs the class independently.")
    print("It does not connect to MySQL.")

    test_subject = input("\nSubject: ").strip()
    test_chapter = input("Chapter: ").strip()
    test_topic = input("Topic: ").strip()
    test_difficulty = input("Previous difficulty: ").strip()

    diagnostic = DoubtDiagnostic(
        test_subject,
        test_chapter,
        test_topic,
        test_difficulty
    )

    diagnostic.diagnose()
