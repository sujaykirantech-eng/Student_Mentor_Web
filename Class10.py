import Database

class Class10:

    def maths(self, Roll, Q_name, Q4_1):

        print("\n========================================")
        print("          CLASS 10 MATHS ASSESSMENT")
        print("========================================\n")

        print("I want to understand which areas of Maths")
        print("you are finding difficult.")
        print("You can select more than one chapter.\n")

        chapters = {
            "1": "Real Numbers",
            "2": "Polynomials",
            "3": "Pair of Linear Equations in Two Variables",
            "4": "Quadratic Equations",
            "5": "Arithmetic Progressions",
            "6": "Triangles",
            "7": "Coordinate Geometry",
            "8": "Introduction to Trigonometry",
            "9": "Applications of Trigonometry",
            "10": "Circles",
            "11": "Areas Related to Circles",
            "12": "Surface Areas and Volumes",
            "13": "Statistics",
            "14": "Probability"
        }

        while True:

            print("\n----------------------------------------")
            print("           CHAPTER SELECTION")
            print("----------------------------------------\n")

            for number, chapter in chapters.items():
                print(f"{number}. {chapter}")

            print("\n15. I am not having difficulty in any chapter")

            chapter_choice = input(
                "\nWhich chapter are you not clear about? "
                "(enter the number): "
            ).strip()

            # ----------------------------------------------------
            # NO DIFFICULTY
            # ----------------------------------------------------

            if chapter_choice == "15":

                print("\nThat's great! 😎")
                print("You don't currently have a specific Maths chapter")
                print("that you feel unclear about.")

                more = input(
                    "\nDo you still want to assess another Maths difficulty? "
                    "(yes/no): "
                ).lower()

                if more == "no":
                    break
                else:
                    continue

            # ----------------------------------------------------
            # INVALID CHAPTER
            # ----------------------------------------------------

            if chapter_choice not in chapters:

                print("\nInvalid choice.")
                print("Please choose a chapter number from 1 to 14.")
                continue

            chapter = chapters[chapter_choice]

            print("\n========================================")
            print(f"        {chapter.upper()}")
            print("========================================")

            print(
                f"\nYou selected: {chapter}"
            )

            # ====================================================
            # Q5 - WHAT PART IS DIFFICULT?
            # ====================================================

            if chapter_choice == "1":

                Q_5 = input(
                    "\nWhat part of Real Numbers is difficult for you?\n"
                    "1. Euclid's Division Algorithm\n"
                    "2. Fundamental Theorem of Arithmetic\n"
                    "3. HCF and LCM\n"
                    "4. Irrational Numbers\n"
                    "5. Applications and Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "2":

                Q_5 = input(
                    "\nWhat part of Polynomials is difficult for you?\n"
                    "1. Zeroes of Polynomials\n"
                    "2. Relationship between Zeroes and Coefficients\n"
                    "3. Finding Zeroes\n"
                    "4. Graphical Understanding\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "3":

                Q_5 = input(
                    "\nWhat part of Pair of Linear Equations is difficult?\n"
                    "1. Graphical Method\n"
                    "2. Substitution Method\n"
                    "3. Elimination Method\n"
                    "4. Cross-Multiplication Method\n"
                    "5. Word Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "4":

                Q_5 = input(
                    "\nWhat part of Quadratic Equations is difficult?\n"
                    "1. Factorisation\n"
                    "2. Quadratic Formula\n"
                    "3. Completing the Square\n"
                    "4. Nature of Roots\n"
                    "5. Word Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "5":

                Q_5 = input(
                    "\nWhat part of Arithmetic Progressions is difficult?\n"
                    "1. Identifying an AP\n"
                    "2. nth Term\n"
                    "3. Sum of n Terms\n"
                    "4. Word Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "6":

                Q_5 = input(
                    "\nWhat part of Triangles is difficult?\n"
                    "1. Similarity\n"
                    "2. Theorems\n"
                    "3. Proofs\n"
                    "4. Applications\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "7":

                Q_5 = input(
                    "\nWhat part of Coordinate Geometry is difficult?\n"
                    "1. Distance Formula\n"
                    "2. Section Formula\n"
                    "3. Midpoint\n"
                    "4. Area of Triangle\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "8":

                Q_5 = input(
                    "\nWhat part of Trigonometry is difficult?\n"
                    "1. Trigonometric Ratios\n"
                    "2. Standard Values\n"
                    "3. Trigonometric Identities\n"
                    "4. Trigonometric Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "9":

                Q_5 = input(
                    "\nWhat part of Applications of Trigonometry is difficult?\n"
                    "1. Drawing the Diagram\n"
                    "2. Identifying Angles\n"
                    "3. Choosing the Ratio\n"
                    "4. Word Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "10":

                Q_5 = input(
                    "\nWhat part of Circles is difficult?\n"
                    "1. Tangent Theorems\n"
                    "2. Proofs\n"
                    "3. Applying Theorems\n"
                    "4. Diagrams\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "11":

                Q_5 = input(
                    "\nWhat part of Areas Related to Circles is difficult?\n"
                    "1. Area of Sector\n"
                    "2. Length of Arc\n"
                    "3. Area of Segment\n"
                    "4. Composite Figures\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "12":

                Q_5 = input(
                    "\nWhat part of Surface Areas and Volumes is difficult?\n"
                    "1. Formula Selection\n"
                    "2. Surface Area\n"
                    "3. Volume\n"
                    "4. Composite Solids\n"
                    "5. Unit Conversion\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "13":

                Q_5 = input(
                    "\nWhat part of Statistics is difficult?\n"
                    "1. Mean\n"
                    "2. Median\n"
                    "3. Mode\n"
                    "4. Cumulative Frequency\n"
                    "5. Graphs\n"
                    "Enter your choice: "
                )

            elif chapter_choice == "14":

                Q_5 = input(
                    "\nWhat part of Probability is difficult?\n"
                    "1. Sample Space\n"
                    "2. Basic Probability\n"
                    "3. Events\n"
                    "4. Word Problems\n"
                    "5. Problems\n"
                    "Enter your choice: "
                )

            # ====================================================
            # Q6 - TOPIC-SPECIFIC LEARNING DIFFICULTY
            # ====================================================

            topic_questions = {
                ('1', '1'): (
                    "When using Euclid's Division Algorithm, what troubles you most?",
                    [
                        'Choosing the dividend and divisor',
                        'Following the repeated-division steps',
                        'Finding the HCF from the final remainder',
                        'Arithmetic errors during division',
                        'Applying it to unfamiliar numbers',
                    ]
                ),
                ('1', '2'): (
                    'What is hardest about the Fundamental Theorem of Arithmetic?',
                    [
                        'Breaking a number into prime factors',
                        'Keeping track of repeated prime factors',
                        'Using prime factors for HCF/LCM',
                        'Handling powers of prime factors',
                        'Applying it to a new problem',
                    ]
                ),
                ('1', '3'): (
                    'What causes difficulty in HCF and LCM questions?',
                    [
                        'Knowing whether HCF or LCM is needed',
                        'Choosing the correct method',
                        'Handling prime factors',
                        'Applying HCF/LCM in word problems',
                        'Checking whether the answer makes sense',
                    ]
                ),
                ('1', '4'): (
                    'What is hardest about irrational numbers?',
                    [
                        'Recognising an irrational number',
                        'Setting up an irrationality proof',
                        'Using contradiction correctly',
                        'Remembering the proof steps',
                        'Handling unfamiliar examples',
                    ]
                ),
                ('1', '5'): (
                    'What usually stops you in Real Numbers application problems?',
                    [
                        'Understanding what the question asks',
                        'Choosing the relevant concept',
                        'Turning words into mathematics',
                        'Carrying out the calculation',
                        'Knowing how to start',
                    ]
                ),
                ('2', '1'): (
                    'What is hardest when finding zeroes of a polynomial?',
                    [
                        'Understanding what a zero represents',
                        'Factorising the polynomial',
                        'Finding all the zeroes',
                        'Checking the answer',
                        'Handling unfamiliar polynomials',
                    ]
                ),
                ('2', '2'): (
                    'What troubles you in the relationship between zeroes and coefficients?',
                    [
                        'Remembering the relationships',
                        'Keeping the signs correct',
                        'Identifying which relationship to use',
                        'Substituting values',
                        'Finding a missing coefficient or zero',
                    ]
                ),
                ('2', '3'): (
                    'What makes finding zeroes difficult for you?',
                    [
                        'Choosing a suitable method',
                        'Factorising correctly',
                        'Handling signs',
                        'Checking the obtained zeroes',
                        'Working without a worked example',
                    ]
                ),
                ('2', '4'): (
                    'What is difficult about the graphical understanding of polynomials?',
                    [
                        'Connecting zeroes with x-intercepts',
                        'Reading the graph',
                        'Identifying the correct scale',
                        'Connecting graph and algebra',
                        'Interpreting an unfamiliar graph',
                    ]
                ),
                ('2', '5'): (
                    'What is hardest in polynomial application problems?',
                    [
                        'Identifying the required information',
                        'Forming the polynomial',
                        'Choosing the correct relationship',
                        'Doing the algebra accurately',
                        'Starting an unfamiliar question',
                    ]
                ),
                ('3', '1'): (
                    'What troubles you in the graphical method?',
                    [
                        'Plotting the two equations',
                        'Finding suitable points',
                        'Understanding the intersection',
                        'Identifying the type of solution',
                        'Interpreting an unfamiliar graph',
                    ]
                ),
                ('3', '2'): (
                    'What is hardest in the substitution method?',
                    [
                        'Choosing which variable to isolate',
                        'Substituting without changing signs',
                        'Handling brackets',
                        'Solving the resulting equation',
                        'Using it independently',
                    ]
                ),
                ('3', '3'): (
                    'What causes difficulty in the elimination method?',
                    [
                        'Choosing what to multiply',
                        'Making coefficients equal',
                        'Adding/subtracting correctly',
                        'Keeping signs correct',
                        'Finishing the second variable',
                    ]
                ),
                ('3', '4'): (
                    'What is hardest about cross-multiplication?',
                    [
                        'Remembering the formula arrangement',
                        'Keeping signs correct',
                        'Matching coefficients to the formula',
                        'Knowing when to use it',
                        'Applying it to unfamiliar equations',
                    ]
                ),
                ('3', '5'): (
                    'What troubles you in linear-equation word problems?',
                    [
                        'Identifying the unknowns',
                        'Converting words into equations',
                        'Choosing a solving method',
                        'Interpreting the final values',
                        'Knowing how to begin',
                    ]
                ),
                ('4', '1'): (
                    'What is hardest about factorising quadratic equations?',
                    [
                        'Finding suitable factors',
                        'Splitting the middle term',
                        'Handling signs',
                        'Finding the roots after factorisation',
                        'Factorising unfamiliar quadratics',
                    ]
                ),
                ('4', '2'): (
                    'What troubles you when using the quadratic formula?',
                    [
                        'Remembering the formula',
                        'Identifying a, b and c',
                        'Substituting signs correctly',
                        'Simplifying the discriminant',
                        'Applying it under exam pressure',
                    ]
                ),
                ('4', '3'): (
                    'What is difficult about completing the square?',
                    [
                        'Understanding the required adjustment',
                        'Finding the number to add/subtract',
                        'Rearranging the equation',
                        'Keeping the algebra accurate',
                        'Connecting the method to the roots',
                    ]
                ),
                ('4', '4'): (
                    'What is hardest about the nature of roots?',
                    [
                        'Understanding the discriminant',
                        'Remembering the three conditions',
                        'Calculating b²−4ac',
                        'Interpreting the result',
                        'Finding an unknown coefficient',
                    ]
                ),
                ('4', '5'): (
                    'What troubles you in quadratic word problems?',
                    [
                        'Identifying the unknown',
                        'Forming the quadratic equation',
                        'Solving the equation',
                        'Rejecting an unsuitable root',
                        'Interpreting the final answer',
                    ]
                ),
                ('5', '1'): (
                    'What is hardest about identifying an Arithmetic Progression?',
                    [
                        'Recognising the sequence as an AP',
                        'Finding the common difference',
                        'Checking every consecutive difference',
                        'Distinguishing AP from other sequences',
                        'Handling unfamiliar sequences',
                    ]
                ),
                ('5', '2'): (
                    'What troubles you in nth-term questions?',
                    [
                        'Remembering the formula',
                        'Identifying a and d',
                        'Substituting n correctly',
                        'Finding a missing term',
                        'Applying the formula in word problems',
                    ]
                ),
                ('5', '3'): (
                    'What is difficult about the sum of n terms?',
                    [
                        'Choosing the correct sum formula',
                        'Identifying a, d and n',
                        'Substituting accurately',
                        'Finding a missing quantity first',
                        'Combining sum with nth-term ideas',
                    ]
                ),
                ('5', '4'): (
                    'What troubles you in AP word problems?',
                    [
                        'Recognising the AP structure',
                        'Finding the first term',
                        'Finding the common difference',
                        'Choosing nth term or sum',
                        'Interpreting the final answer',
                    ]
                ),
                ('6', '1'): (
                    'What is hardest about similarity of triangles?',
                    [
                        'Recognising corresponding angles',
                        'Matching corresponding sides',
                        'Choosing the correct similarity criterion',
                        'Setting up proportions',
                        'Handling differently drawn triangles',
                    ]
                ),
                ('6', '2'): (
                    'What troubles you with triangle theorems?',
                    [
                        'Remembering theorem statements',
                        'Recognising which theorem applies',
                        'Connecting the theorem to the diagram',
                        'Using the resulting ratio',
                        'Applying a theorem in a new diagram',
                    ]
                ),
                ('6', '3'): (
                    'What is hardest about triangle proofs?',
                    [
                        'Knowing how to start',
                        'Choosing the required theorem',
                        'Ordering the logical steps',
                        'Using the given information',
                        'Knowing exactly what must be proved',
                    ]
                ),
                ('6', '4'): (
                    'What troubles you when applying triangle concepts?',
                    [
                        'Identifying the relevant concept',
                        'Reading the diagram',
                        'Choosing the theorem',
                        'Connecting several steps',
                        'Starting without a worked example',
                    ]
                ),
                ('6', '5'): (
                    'What is difficult in triangle problems?',
                    [
                        'Extracting information from the diagram',
                        'Choosing a theorem',
                        'Setting up the calculation',
                        'Avoiding calculation mistakes',
                        'Combining more than one concept',
                    ]
                ),
                ('7', '1'): (
                    'What troubles you in the distance formula?',
                    [
                        'Remembering the formula',
                        'Substituting coordinates',
                        'Handling negative coordinates',
                        'Simplifying the square root',
                        'Identifying the correct two points',
                    ]
                ),
                ('7', '2'): (
                    'What is hardest about the section formula?',
                    [
                        'Remembering the formula',
                        'Using the ratio correctly',
                        'Keeping coordinate signs correct',
                        'Substituting values',
                        'Finding an unknown coordinate',
                    ]
                ),
                ('7', '3'): (
                    'What troubles you with the midpoint formula?',
                    [
                        'Remembering the formula',
                        'Adding coordinates correctly',
                        'Handling negative values',
                        'Distinguishing it from section formula',
                        'Applying it in a word problem',
                    ]
                ),
                ('7', '4'): (
                    'What is hardest about area of a triangle using coordinates?',
                    [
                        'Remembering the formula',
                        'Substituting coordinates',
                        'Handling signs',
                        'Taking the absolute value',
                        'Interpreting a zero-area result',
                    ]
                ),
                ('7', '5'): (
                    'What troubles you in Coordinate Geometry problems?',
                    [
                        'Choosing the formula',
                        'Identifying the useful points',
                        'Handling signs',
                        'Setting up the calculation',
                        'Combining multiple formulas',
                    ]
                ),
                ('8', '1'): (
                    'What is hardest about trigonometric ratios?',
                    [
                        'Identifying opposite/adjacent/hypotenuse',
                        'Choosing sin, cos or tan',
                        'Reading a rotated triangle',
                        'Substituting values',
                        'Applying ratios in an unfamiliar diagram',
                    ]
                ),
                ('8', '2'): (
                    'What troubles you with standard trigonometric values?',
                    [
                        'Remembering the values',
                        'Matching the angle to the ratio',
                        'Avoiding sin/cos confusion',
                        'Handling reciprocal values',
                        'Applying values in a longer calculation',
                    ]
                ),
                ('8', '3'): (
                    'What is hardest about trigonometric identities?',
                    [
                        'Remembering basic identities',
                        'Choosing which identity to use',
                        'Transforming one side',
                        'Handling algebraic manipulation',
                        'Starting an unfamiliar proof',
                    ]
                ),
                ('8', '4'): (
                    'What troubles you in trigonometric problems?',
                    [
                        'Choosing the correct ratio',
                        'Selecting the needed identity',
                        'Substituting standard values',
                        'Managing multiple steps',
                        'Knowing how to begin',
                    ]
                ),
                ('9', '1'): (
                    'What is hardest about drawing diagrams for Applications of Trigonometry?',
                    [
                        'Identifying the objects and distances',
                        'Placing the right angle',
                        'Representing height correctly',
                        'Labelling the diagram',
                        'Visualising the situation',
                    ]
                ),
                ('9', '2'): (
                    'What troubles you when identifying angles of elevation/depression?',
                    [
                        'Recognising the reference line',
                        'Distinguishing elevation from depression',
                        'Locating the correct angle',
                        'Reading an unscaled diagram',
                        'Connecting the angle to the triangle',
                    ]
                ),
                ('9', '3'): (
                    'What is hardest about choosing a ratio in Applications of Trigonometry?',
                    [
                        'Identifying the known sides',
                        'Matching sides to sin/cos/tan',
                        'Choosing a ratio with useful information',
                        'Setting up the equation',
                        'Handling a multi-step situation',
                    ]
                ),
                ('9', '4'): (
                    'What troubles you in Applications of Trigonometry word problems?',
                    [
                        'Understanding the situation',
                        'Drawing the diagram',
                        'Identifying the angle',
                        'Choosing the ratio',
                        'Connecting multiple steps',
                    ]
                ),
                ('10', '1'): (
                    'What is hardest about tangent theorems?',
                    [
                        'Remembering tangent properties',
                        'Recognising when a tangent theorem applies',
                        'Connecting tangent and radius',
                        'Using the theorem in calculations',
                        'Handling an unfamiliar diagram',
                    ]
                ),
                ('10', '2'): (
                    'What troubles you in circle proofs?',
                    [
                        'Knowing how to start',
                        'Choosing the required theorem',
                        'Reading the diagram',
                        'Ordering the proof',
                        'Connecting given facts to the conclusion',
                    ]
                ),
                ('10', '3'): (
                    'What is difficult when applying circle theorems?',
                    [
                        'Identifying the theorem',
                        'Extracting information from the diagram',
                        'Applying the theorem correctly',
                        'Handling angles/lengths',
                        'Combining circle properties',
                    ]
                ),
                ('10', '4'): (
                    'What troubles you with circle diagrams?',
                    [
                        'Identifying important points',
                        'Distinguishing radius/chord/tangent',
                        'Marking equal angles or lengths',
                        'Reading a complex diagram',
                        'Visualising an unfamiliar figure',
                    ]
                ),
                ('10', '5'): (
                    'What is hardest in Circle problems?',
                    [
                        'Choosing the theorem',
                        'Understanding the diagram',
                        'Setting up the relation',
                        'Doing the calculation',
                        'Combining multiple theorems',
                    ]
                ),
                ('11', '1'): (
                    'What troubles you in area-of-sector questions?',
                    [
                        'Remembering the sector formula',
                        'Using the central angle',
                        'Handling fractions of a circle',
                        'Using π accurately',
                        'Applying it to a composite figure',
                    ]
                ),
                ('11', '2'): (
                    'What is hardest about arc length?',
                    [
                        'Remembering the formula',
                        'Using the central angle',
                        'Converting the angle correctly',
                        'Distinguishing arc length from area',
                        'Handling multi-step questions',
                    ]
                ),
                ('11', '3'): (
                    'What troubles you with area of a segment?',
                    [
                        'Identifying the required region',
                        'Finding the sector area',
                        'Finding the triangle area',
                        'Knowing what to subtract',
                        'Visualising the segment',
                    ]
                ),
                ('11', '4'): (
                    'What is hardest about composite circular figures?',
                    [
                        'Splitting the figure into parts',
                        'Deciding what to add/subtract',
                        'Finding missing dimensions',
                        'Handling several formulas',
                        'Reading the diagram',
                    ]
                ),
                ('11', '5'): (
                    'What troubles you in Areas Related to Circles problems?',
                    [
                        'Choosing the formula',
                        'Identifying the required region',
                        'Combining areas',
                        'Handling units/calculation',
                        'Starting an unfamiliar diagram',
                    ]
                ),
                ('12', '1'): (
                    'What is hardest about formula selection in Surface Areas and Volumes?',
                    [
                        'Identifying the solid',
                        'Choosing surface area or volume',
                        'Choosing the correct formula',
                        'Recognising exposed surfaces',
                        'Handling combined solids',
                    ]
                ),
                ('12', '2'): (
                    'What troubles you with surface area?',
                    [
                        'Distinguishing curved/total/lateral area',
                        'Identifying exposed surfaces',
                        'Choosing the formula',
                        'Handling dimensions',
                        'Solving composite solids',
                    ]
                ),
                ('12', '3'): (
                    'What is hardest about volume?',
                    [
                        'Remembering the formula',
                        'Identifying dimensions',
                        'Choosing the correct solid',
                        'Handling units',
                        'Combining volumes',
                    ]
                ),
                ('12', '4'): (
                    'What troubles you with composite solids?',
                    [
                        'Splitting the solid',
                        'Finding shared dimensions',
                        'Deciding what to add/subtract',
                        'Choosing formulas',
                        'Keeping the 3D structure clear',
                    ]
                ),
                ('12', '5'): (
                    'What is hardest about unit conversion?',
                    [
                        'Remembering length conversions',
                        'Handling square units',
                        'Handling cubic units',
                        'Converting before calculation',
                        'Avoiding powers-of-10 mistakes',
                    ]
                ),
                ('13', '1'): (
                    'What troubles you when finding the mean?',
                    [
                        'Identifying the correct values',
                        'Using frequency correctly',
                        'Adding accurately',
                        'Dividing by the correct total',
                        'Handling grouped data',
                    ]
                ),
                ('13', '2'): (
                    'What is hardest about finding the median?',
                    [
                        'Finding the correct position',
                        'Identifying the median class',
                        'Using cumulative frequency',
                        'Substituting into the formula',
                        'Handling grouped data',
                    ]
                ),
                ('13', '3'): (
                    'What troubles you with mode?',
                    [
                        'Identifying the modal class',
                        'Finding the relevant frequencies',
                        'Remembering the formula',
                        'Substituting correctly',
                        'Handling missing-frequency questions',
                    ]
                ),
                ('13', '4'): (
                    'What is hardest about cumulative frequency?',
                    [
                        'Constructing the table',
                        'Adding frequencies correctly',
                        'Finding the required cumulative frequency',
                        'Using it for median',
                        'Reading the table quickly',
                    ]
                ),
                ('13', '5'): (
                    'What troubles you with Statistics graphs?',
                    [
                        'Choosing the correct graph',
                        'Choosing a suitable scale',
                        'Labelling axes',
                        'Plotting accurately',
                        'Interpreting the graph',
                    ]
                ),
                ('14', '1'): (
                    'What is hardest about identifying the sample space?',
                    [
                        'Listing every outcome',
                        'Avoiding duplicate outcomes',
                        'Counting outcomes correctly',
                        'Handling multi-step experiments',
                        'Representing outcomes systematically',
                    ]
                ),
                ('14', '2'): (
                    'What troubles you in basic probability?',
                    [
                        'Remembering the formula',
                        'Finding favourable outcomes',
                        'Finding total outcomes',
                        'Simplifying the probability',
                        'Translating a word problem',
                    ]
                ),
                ('14', '3'): (
                    'What is hardest about probability events?',
                    [
                        'Understanding what the event means',
                        'Identifying favourable outcomes',
                        'Handling multiple events',
                        'Interpreting the wording',
                        'Connecting events to the sample space',
                    ]
                ),
                ('14', '4'): (
                    'What troubles you in Probability word problems?',
                    [
                        'Understanding the situation',
                        'Building the sample space',
                        'Identifying favourable outcomes',
                        'Choosing the probability method',
                        'Turning words into mathematics',
                    ]
                ),
                ('14', '5'): (
                    'What is hardest in Probability problem-solving?',
                    [
                        'Knowing how to start',
                        'Listing possible outcomes',
                        'Choosing a counting approach',
                        'Calculating accurately',
                        'Handling unfamiliar problem types',
                    ]
                ),
            }

            key = (chapter_choice, Q_5)

            if key in topic_questions:

                question, choices = topic_questions[key]

                print("\n----------------------------------------")
                print("       LET'S UNDERSTAND THE PROBLEM")
                print("----------------------------------------\n")
                print(question)

                for index, choice in enumerate(choices, start=1):
                    print(f"{index}. {choice}")

                print("6. Something else.")

                Q_6 = input("\nEnter your choice: ").strip()

                while Q_6 not in ["1", "2", "3", "4", "5", "6"]:
                    print("Please enter a number from 1 to 6.")
                    Q_6 = input("Enter your choice: ").strip()

                if Q_6 == "6":
                    other_problem = input(
                        "\nTell me what usually happens when you struggle "
                        "with this topic: "
                    )
                    difficulty = "Other: " + other_problem
                else:
                    difficulty = choices[int(Q_6) - 1]

            else:
                Q_6 = input(
                    "\nTell me what usually makes this topic difficult for you: "
                ).strip()
                difficulty = Q_6

            # ====================================================
            # PERSONALIZED GUIDANCE
            # ====================================================

            selected_problem = ""

            if Q_6 in ["1", "2", "3", "4", "5"]:
                selected_problem = choices[int(Q_6) - 1]

            def give_guidance(problem, chapter_name):

                p = problem.lower()

                print("\n========================================")
                print("          WHAT YOU CAN DO")
                print("========================================\n")

                if "remember" in p or "formula" in p or "values" in p:
                    print(
                        f"For {chapter_name}, don't try to memorise everything "
                        "by repeatedly reading it."
                    )
                    print(
                        "\nMake a small formula sheet and practise recalling it "
                        "without looking at the book."
                    )
                    print(
                        "Then solve 3 easy questions using the formula from memory."
                    )
                    print(
                        "After that, close the formula sheet and solve one mixed "
                        "question."
                    )

                elif "choos" in p or "identif" in p or "select" in p:
                    print(
                        f"Your main issue in {chapter_name} seems to be recognising "
                        "which method to use."
                    )
                    print(
                        "\nBefore solving, underline the information given in the "
                        "question."
                    )
                    print(
                        "Then ask: 'What is the question asking me to find?'"
                    )
                    print(
                        "Finally, write down two possible formulas/theorems and "
                        "decide which one actually uses the given information."
                    )

                elif "diagram" in p or "visualis" in p or "draw" in p or "reading" in p:
                    print(
                        f"For {chapter_name}, practise understanding the diagram "
                        "before doing calculations."
                    )
                    print(
                        "\nFirst redraw the diagram neatly."
                    )
                    print(
                        "Label every known length, angle, point or relevant part."
                    )
                    print(
                        "Then mark exactly what the question asks you to find."
                    )
                    print(
                        "Only after that choose the theorem or formula."
                    )

                elif "sign" in p or "substitut" in p or "negative" in p:
                    print(
                        f"In {chapter_name}, your concept may be okay but the "
                        "substitution stage needs more control."
                    )
                    print(
                        "\nWrite every substitution on a separate line instead "
                        "of doing it mentally."
                    )
                    print(
                        "Put brackets around negative numbers."
                    )
                    print(
                        "At the end, check the signs once before simplifying."
                    )

                elif (
                    "calculat" in p
                    or "accuracy" in p
                    or "mistake" in p
                    or "adding" in p
                    or "simplif" in p
                ):
                    print(
                        f"For {chapter_name}, focus on accuracy rather than simply "
                        "solving more questions."
                    )
                    print(
                        "\nKeep a small mistake log."
                    )
                    print(
                        "For every wrong answer, write whether it was a sign, "
                        "calculation, formula, copying or reasoning mistake."
                    )
                    print(
                        "Redo the same question correctly after identifying the error."
                    )

                elif "proof" in p or "theorem" in p or "ordering" in p:
                    print(
                        f"For {chapter_name}, practise the LOGIC of the proof, "
                        "not just memorising the final answer."
                    )
                    print(
                        "\nWrite down: Given → To Prove → Theorem/Property → Steps → Result."
                    )
                    print(
                        "After studying one proof, close the book and reproduce "
                        "the reasoning in your own words."
                    )

                elif "word problem" in p or "situation" in p or "words" in p or "application" in p:
                    print(
                        f"For {chapter_name}, the main goal is converting words "
                        "into mathematics."
                    )
                    print(
                        "\nFirst write down the known information."
                    )
                    print(
                        "Next define the unknown quantity."
                    )
                    print(
                        "Then draw a diagram or write an equation if appropriate."
                    )
                    print(
                        "Only after that choose the formula or method."
                    )

                elif "graph" in p or "plot" in p or "scale" in p or "axis" in p:
                    print(
                        f"For {chapter_name}, practise reading the graph before "
                        "trying to calculate from it."
                    )
                    print(
                        "\nAlways check the x-axis, y-axis and scale first."
                    )
                    print(
                        "Mark the important points clearly."
                    )
                    print(
                        "Then explain in words what the graph is showing."
                    )

                elif "ratio" in p or "outcome" in p or "sample space" in p or "count" in p:
                    print(
                        f"For {chapter_name}, slow down at the setup stage."
                    )
                    print(
                        "\nList the information systematically before calculating."
                    )
                    print(
                        "For probability, write the complete sample space first."
                    )
                    print(
                        "For ratios, clearly label the quantities being compared."
                    )
                    print(
                        "Then calculate and check whether the answer makes sense."
                    )

                elif "unit" in p or "conversion" in p or "powers-of-10" in p:
                    print(
                        f"For {chapter_name}, make units part of every calculation."
                    )
                    print(
                        "\nConvert all measurements to the same unit before "
                        "substituting into the formula."
                    )
                    print(
                        "Remember: area uses square units and volume uses cubic units."
                    )
                    print(
                        "Write the unit beside the final answer."
                    )

                elif "start" in p or "begin" in p or "unfamiliar" in p or "complex" in p:
                    print(
                        f"For {chapter_name}, the first step is what we need to train."
                    )
                    print(
                        "\nUse this routine:"
                    )
                    print(
                        "1. Write what is given."
                    )
                    print(
                        "2. Write what must be found."
                    )
                    print(
                        "3. Draw a diagram or write the relevant equation."
                    )
                    print(
                        "4. Choose the formula/theorem."
                    )
                    print(
                        "5. Solve one step at a time."
                    )

                else:
                    print(
                        f"For {chapter_name}, break the problem into smaller steps "
                        "instead of trying to solve the whole question immediately."
                    )
                    print(
                        "\nStudy one solved example, close the solution, and solve "
                        "a similar question independently."
                    )
                    print(
                        "Then practise two slightly different questions to make "
                        "sure you can apply the idea."
                    )

                print(
                    "\nTip: Don't measure improvement by how many pages you read. "
                    "Measure it by how many questions you can solve independently."
                )


            if Q_6 in ["1", "2", "3", "4", "5"]:

                give_guidance(selected_problem, chapter)

            elif Q_6 == "6":

                print("\n========================================")
                print("          LET'S UNDERSTAND IT")
                print("========================================\n")
                print(
                    "Your own explanation is important because it can reveal a "
                    "difficulty that the options did not cover."
                )
                print(
                    "\nTry describing the exact step where you usually get stuck."
                )
                print(
                    "For now, start with one worked example, identify the first "
                    "step where you get stuck, and practise that step separately."
                )


            # ====================================================
            # MYSQL SAVE
            # ====================================================
            Database.save_response(
                Roll_no=Roll,
                Student_name=Q_name,
                student_class="10",
                Student_Section=Q4_1,
                subject="Maths",
                chapter=chapter,
                topic=Q_5,
                difficulty=difficulty
            )

            # ====================================================
            # LOOP
            # ====================================================

            print("\n----------------------------------------")

            another = input(
                "Are there any other Maths chapters you are not clear about? "
                "(yes/no): "
            ).strip().lower()

            if another == "yes":

                print(
                    "\nOkay! Let's identify the next chapter. 🔄"
                )

                continue

            else:

                print("\n========================================")
                print("       MATHS ASSESSMENT COMPLETED")
                print("========================================")

                print(
                    "\nWe've identified the Maths difficulties you wanted "
                    "to discuss."
                )

                print(
                    "Remember: struggling with a chapter does not mean "
                    "you're bad at Maths."
                )

                break
    
    def science(self, Roll, Q_name, Q4_1):

        print("\n========================================")
        print("          CLASS 10 SCIENCE ASSESSMENT")
        print("========================================\n")

        print("I want to understand which areas of Science")
        print("you are finding difficult.")
        print("You can select more than one chapter.\n")

        chapters = {
            "1": "Chemical Reactions and Equations",
            "2": "Acids, Bases and Salts",
            "3": "Metals and Non-metals",
            "4": "Carbon and its Compounds",
            "5": "Life Processes",
            "6": "Control and Coordination",
            "7": "How do Organisms Reproduce?",
            "8": "Heredity",
            "9": "Light – Reflection and Refraction",
            "10": "The Human Eye and the Colourful World",
            "11": "Electricity",
            "12": "Magnetic Effects of Electric Current",
            "13": "Our Environment",
            "14": "Sustainable Management of Natural Resources"
        }

        topic_questions = {

            ("1", "1"): (
                "What is hardest about writing and balancing chemical equations?",
                [
                    "Writing the correct chemical formulae",
                    "Knowing which element to balance first",
                    "Keeping the number of atoms equal",
                    "Handling complex equations",
                    "Checking whether the final equation is balanced"
                ]
            ),
            ("1", "2"): (
                "What is hardest about types of chemical reactions?",
                [
                    "Remembering the different reaction types",
                    "Recognising the type from an equation",
                    "Distinguishing similar reaction types",
                    "Writing the correct products",
                    "Applying the classification to unfamiliar reactions"
                ]
            ),
            ("1", "3"): (
                "What is hardest about oxidation and reduction?",
                [
                    "Remembering what oxidation means",
                    "Remembering what reduction means",
                    "Identifying oxidised and reduced substances",
                    "Understanding oxidising and reducing agents",
                    "Applying the concepts to new reactions"
                ]
            ),
            ("1", "4"): (
                "What is hardest about the effects of oxidation (corrosion and rancidity)?",
                [
                    "Understanding corrosion",
                    "Understanding rancidity",
                    "Remembering prevention methods",
                    "Connecting the concept with real examples",
                    "Answering application-based questions"
                ]
            ),

            ("2", "1"): (
                "What is hardest about acids, bases and their properties?",
                [
                    "Understanding their properties",
                    "Using indicators correctly",
                    "Interpreting colour changes",
                    "Distinguishing strong and weak substances",
                    "Applying properties to unfamiliar examples"
                ]
            ),
            ("2", "2"): (
                "What is hardest about chemical reactions of acids and bases?",
                [
                    "Remembering the reactions",
                    "Predicting the products",
                    "Writing balanced equations",
                    "Understanding neutralisation",
                    "Applying reactions to word problems"
                ]
            ),
            ("2", "3"): (
                "What is hardest about the pH scale?",
                [
                    "Understanding what pH represents",
                    "Remembering the pH range",
                    "Comparing acidic and basic strength",
                    "Interpreting pH in everyday situations",
                    "Solving application questions"
                ]
            ),
            ("2", "4"): (
                "What is hardest about salts?",
                [
                    "Remembering common salts",
                    "Understanding how salts are prepared",
                    "Writing the reactions",
                    "Connecting salts with their uses",
                    "Distinguishing similar compounds"
                ]
            ),

            ("3", "1"): (
                "What is hardest about physical properties of metals and non-metals?",
                [
                    "Remembering the properties",
                    "Comparing metals and non-metals",
                    "Understanding exceptions",
                    "Connecting properties with uses",
                    "Answering comparison questions"
                ]
            ),
            ("3", "2"): (
                "What is hardest about chemical properties of metals?",
                [
                    "Remembering reactions with oxygen",
                    "Understanding reactions with water",
                    "Understanding reactions with acids",
                    "Writing the correct equations",
                    "Predicting whether a reaction occurs"
                ]
            ),
            ("3", "3"): (
                "What is hardest about the reactivity series?",
                [
                    "Remembering the order",
                    "Comparing reactivities",
                    "Predicting displacement reactions",
                    "Understanding extraction implications",
                    "Applying the series to unfamiliar questions"
                ]
            ),
            ("3", "4"): (
                "What is hardest about ionic compounds?",
                [
                    "Understanding ion formation",
                    "Understanding electron transfer",
                    "Writing ionic formulae",
                    "Understanding their physical properties",
                    "Connecting structure with properties"
                ]
            ),
            ("3", "5"): (
                "What is hardest about extraction of metals?",
                [
                    "Understanding the extraction steps",
                    "Connecting reactivity with extraction method",
                    "Understanding roasting and calcination",
                    "Remembering reduction methods",
                    "Applying the process to different metals"
                ]
            ),

            ("4", "1"): (
                "What is hardest about covalent bonding?",
                [
                    "Understanding sharing of electrons",
                    "Drawing electron-dot structures",
                    "Identifying covalent bonds",
                    "Understanding properties of covalent compounds",
                    "Applying bonding ideas to unfamiliar compounds"
                ]
            ),
            ("4", "2"): (
                "What is hardest about carbon's bonding and versatility?",
                [
                    "Understanding tetravalency",
                    "Understanding catenation",
                    "Drawing carbon structures",
                    "Connecting structure with properties",
                    "Handling unfamiliar carbon compounds"
                ]
            ),
            ("4", "3"): (
                "What is hardest about homologous series and nomenclature?",
                [
                    "Recognising functional groups",
                    "Understanding patterns in a homologous series",
                    "Naming compounds",
                    "Writing structural formulae",
                    "Distinguishing similar compounds"
                ]
            ),
            ("4", "4"): (
                "What is hardest about chemical properties of carbon compounds?",
                [
                    "Remembering combustion",
                    "Understanding oxidation",
                    "Understanding addition reactions",
                    "Understanding substitution reactions",
                    "Writing or predicting products"
                ]
            ),
            ("4", "5"): (
                "What is hardest about ethanol and ethanoic acid?",
                [
                    "Remembering their properties",
                    "Understanding their reactions",
                    "Writing equations",
                    "Understanding esterification",
                    "Connecting chemistry with everyday uses"
                ]
            ),

            ("5", "1"): (
                "What is hardest about nutrition?",
                [
                    "Understanding different modes of nutrition",
                    "Remembering the steps of digestion",
                    "Understanding enzymes",
                    "Connecting organs with their functions",
                    "Answering application questions"
                ]
            ),
            ("5", "2"): (
                "What is hardest about respiration?",
                [
                    "Distinguishing aerobic and anaerobic respiration",
                    "Understanding the steps of respiration",
                    "Remembering where processes occur",
                    "Understanding energy release",
                    "Applying the concept to situations"
                ]
            ),
            ("5", "3"): (
                "What is hardest about transportation in humans?",
                [
                    "Understanding blood components",
                    "Understanding the heart and circulation",
                    "Remembering the path of blood",
                    "Understanding double circulation",
                    "Interpreting heart or circulation diagrams"
                ]
            ),
            ("5", "4"): (
                "What is hardest about transportation in plants?",
                [
                    "Understanding xylem",
                    "Understanding phloem",
                    "Understanding transpiration",
                    "Understanding transport mechanisms",
                    "Connecting structure with function"
                ]
            ),
            ("5", "5"): (
                "What is hardest about excretion?",
                [
                    "Understanding the human excretory system",
                    "Remembering nephron structure",
                    "Understanding urine formation",
                    "Understanding excretion in plants",
                    "Interpreting diagrams"
                ]
            ),

            ("6", "1"): (
                "What is hardest about the nervous system?",
                [
                    "Understanding the parts of a neuron",
                    "Understanding nerve impulses",
                    "Following the pathway of a response",
                    "Distinguishing brain regions and functions",
                    "Interpreting nervous-system diagrams"
                ]
            ),
            ("6", "2"): (
                "What is hardest about reflex actions?",
                [
                    "Understanding the reflex arc",
                    "Remembering the pathway",
                    "Identifying the role of each neuron",
                    "Distinguishing reflex and voluntary actions",
                    "Applying the concept to examples"
                ]
            ),
            ("6", "3"): (
                "What is hardest about hormones?",
                [
                    "Remembering different hormones",
                    "Connecting hormones with functions",
                    "Understanding plant hormones",
                    "Distinguishing nervous and hormonal control",
                    "Applying the concepts to examples"
                ]
            ),
            ("6", "4"): (
                "What is hardest about plant movements?",
                [
                    "Understanding tropisms",
                    "Distinguishing different tropisms",
                    "Understanding the role of hormones",
                    "Connecting stimulus with response",
                    "Applying the concept to examples"
                ]
            ),

            ("7", "1"): (
                "What is hardest about asexual reproduction?",
                [
                    "Remembering different methods",
                    "Distinguishing the methods",
                    "Understanding the biological process",
                    "Connecting examples with methods",
                    "Answering comparison questions"
                ]
            ),
            ("7", "2"): (
                "What is hardest about sexual reproduction in plants?",
                [
                    "Understanding flower structure",
                    "Understanding pollination",
                    "Understanding fertilisation",
                    "Following the reproductive process",
                    "Interpreting flower diagrams"
                ]
            ),
            ("7", "3"): (
                "What is hardest about human reproduction?",
                [
                    "Remembering reproductive organs",
                    "Understanding their functions",
                    "Following the reproductive process",
                    "Understanding hormonal changes",
                    "Interpreting reproductive-system diagrams"
                ]
            ),
            ("7", "4"): (
                "What is hardest about reproductive health?",
                [
                    "Understanding contraceptive methods",
                    "Understanding their purposes",
                    "Understanding sexually transmitted infections",
                    "Distinguishing facts from misconceptions",
                    "Answering application questions"
                ]
            ),

            ("8", "1"): (
                "What is hardest about Mendel's experiments?",
                [
                    "Understanding the experimental setup",
                    "Understanding dominant and recessive traits",
                    "Following the crosses",
                    "Interpreting ratios",
                    "Applying Mendel's ideas to new crosses"
                ]
            ),
            ("8", "2"): (
                "What is hardest about inheritance?",
                [
                    "Understanding genes and alleles",
                    "Distinguishing genotype and phenotype",
                    "Setting up genetic crosses",
                    "Calculating expected ratios",
                    "Interpreting inheritance questions"
                ]
            ),
            ("8", "3"): (
                "What is hardest about sex determination?",
                [
                    "Understanding sex chromosomes",
                    "Following the inheritance pattern",
                    "Drawing the cross",
                    "Interpreting probability",
                    "Avoiding misconceptions"
                ]
            ),
            ("8", "4"): (
                "What is hardest about evolution?",
                [
                    "Understanding variation",
                    "Understanding natural selection",
                    "Connecting inheritance with evolution",
                    "Understanding evidence for evolution",
                    "Applying evolutionary ideas to examples"
                ]
            ),

            ("9", "1"): (
                "What is hardest about reflection of light?",
                [
                    "Understanding the laws of reflection",
                    "Drawing ray diagrams",
                    "Using sign conventions",
                    "Finding image characteristics",
                    "Solving numerical questions"
                ]
            ),
            ("9", "2"): (
                "What is hardest about spherical mirrors?",
                [
                    "Understanding mirror terminology",
                    "Drawing ray diagrams",
                    "Using the mirror formula",
                    "Using magnification",
                    "Applying sign conventions"
                ]
            ),
            ("9", "3"): (
                "What is hardest about refraction?",
                [
                    "Understanding why light bends",
                    "Using refractive index",
                    "Understanding Snell's law",
                    "Drawing refraction diagrams",
                    "Solving numerical questions"
                ]
            ),
            ("9", "4"): (
                "What is hardest about lenses?",
                [
                    "Understanding lens terminology",
                    "Drawing ray diagrams",
                    "Using the lens formula",
                    "Using magnification",
                    "Applying sign conventions"
                ]
            ),
            ("9", "5"): (
                "What is hardest about ray diagrams and numericals?",
                [
                    "Choosing the correct formula",
                    "Drawing the correct ray diagram",
                    "Applying sign conventions",
                    "Substituting values",
                    "Interpreting the final answer"
                ]
            ),

            ("10", "1"): (
                "What is hardest about the human eye?",
                [
                    "Remembering the parts",
                    "Connecting each part with its function",
                    "Understanding accommodation",
                    "Interpreting eye diagrams",
                    "Answering application questions"
                ]
            ),
            ("10", "2"): (
                "What is hardest about defects of vision?",
                [
                    "Distinguishing myopia and hypermetropia",
                    "Understanding their causes",
                    "Remembering corrective lenses",
                    "Drawing correction diagrams",
                    "Solving numerical questions"
                ]
            ),
            ("10", "3"): (
                "What is hardest about atmospheric refraction?",
                [
                    "Understanding why refraction occurs",
                    "Understanding twinkling of stars",
                    "Understanding apparent position",
                    "Connecting examples with the concept",
                    "Answering reasoning questions"
                ]
            ),
            ("10", "4"): (
                "What is hardest about dispersion and scattering?",
                [
                    "Understanding dispersion",
                    "Understanding rainbow formation",
                    "Understanding scattering",
                    "Connecting colours with wavelength",
                    "Explaining everyday observations"
                ]
            ),

            ("11", "1"): (
                "What is hardest about electric current and potential difference?",
                [
                    "Understanding the concepts",
                    "Distinguishing current and potential difference",
                    "Reading circuit diagrams",
                    "Using correct units",
                    "Applying concepts to numerical questions"
                ]
            ),
            ("11", "2"): (
                "What is hardest about Ohm's law?",
                [
                    "Understanding the relationship",
                    "Using the formula correctly",
                    "Reading V-I graphs",
                    "Rearranging the formula",
                    "Solving unfamiliar numerical questions"
                ]
            ),
            ("11", "3"): (
                "What is hardest about resistance and resistivity?",
                [
                    "Understanding what resistance depends on",
                    "Using the resistance formula",
                    "Understanding resistivity",
                    "Handling unit conversions",
                    "Solving numerical questions"
                ]
            ),
            ("11", "4"): (
                "What is hardest about series and parallel circuits?",
                [
                    "Understanding current distribution",
                    "Understanding potential difference distribution",
                    "Finding equivalent resistance",
                    "Drawing or interpreting circuits",
                    "Solving mixed numerical questions"
                ]
            ),
            ("11", "5"): (
                "What is hardest about electric power and energy?",
                [
                    "Remembering power formulas",
                    "Choosing the correct formula",
                    "Handling units",
                    "Calculating electrical energy",
                    "Applying the concepts to household situations"
                ]
            ),

            ("12", "1"): (
                "What is hardest about magnetic fields?",
                [
                    "Understanding magnetic field lines",
                    "Drawing field-line patterns",
                    "Understanding direction",
                    "Comparing field strength",
                    "Interpreting magnetic-field diagrams"
                ]
            ),
            ("12", "2"): (
                "What is hardest about the magnetic field due to current?",
                [
                    "Understanding the field around a straight conductor",
                    "Using the right-hand thumb rule",
                    "Understanding circular field lines",
                    "Understanding the field around a coil",
                    "Applying the idea to diagrams"
                ]
            ),
            ("12", "3"): (
                "What is hardest about electromagnetic induction?",
                [
                    "Understanding induced current",
                    "Understanding changing magnetic fields",
                    "Using Fleming's right-hand rule",
                    "Understanding generator action",
                    "Interpreting diagrams"
                ]
            ),
            ("12", "4"): (
                "What is hardest about electric motors?",
                [
                    "Understanding the principle",
                    "Understanding the role of the magnetic field",
                    "Using Fleming's left-hand rule",
                    "Understanding the split ring",
                    "Interpreting motor diagrams"
                ]
            ),
            ("12", "5"): (
                "What is hardest about domestic electric circuits?",
                [
                    "Understanding live, neutral and earth wires",
                    "Understanding fuse and safety devices",
                    "Understanding parallel connections",
                    "Reading domestic-circuit diagrams",
                    "Applying electrical safety concepts"
                ]
            ),

            ("13", "1"): (
                "What is hardest about ecosystems?",
                [
                    "Understanding components of an ecosystem",
                    "Distinguishing biotic and abiotic factors",
                    "Understanding food chains",
                    "Understanding food webs",
                    "Applying ecosystem concepts"
                ]
            ),
            ("13", "2"): (
                "What is hardest about food chains and energy flow?",
                [
                    "Identifying trophic levels",
                    "Understanding energy transfer",
                    "Understanding the 10 percent law",
                    "Constructing food chains",
                    "Answering application questions"
                ]
            ),
            ("13", "3"): (
                "What is hardest about ozone and environmental problems?",
                [
                    "Understanding ozone formation",
                    "Understanding ozone depletion",
                    "Connecting causes with effects",
                    "Remembering prevention measures",
                    "Answering reasoning questions"
                ]
            ),
            ("13", "4"): (
                "What is hardest about biodegradable and non-biodegradable waste?",
                [
                    "Distinguishing the two categories",
                    "Understanding decomposition",
                    "Understanding environmental effects",
                    "Identifying examples",
                    "Applying waste-management concepts"
                ]
            ),

            ("14", "1"): (
                "What is hardest about sustainable development?",
                [
                    "Understanding sustainability",
                    "Balancing human needs and conservation",
                    "Understanding resource management",
                    "Applying the concept to real situations",
                    "Answering reasoning questions"
                ]
            ),
            ("14", "2"): (
                "What is hardest about forest and wildlife conservation?",
                [
                    "Understanding conservation methods",
                    "Understanding stakeholder roles",
                    "Connecting human activity with environmental effects",
                    "Remembering examples",
                    "Answering application questions"
                ]
            ),
            ("14", "3"): (
                "What is hardest about water management?",
                [
                    "Understanding water conservation",
                    "Understanding rainwater harvesting",
                    "Evaluating large projects",
                    "Connecting resource use with sustainability",
                    "Answering case-based questions"
                ]
            ),
            ("14", "4"): (
                "What is hardest about coal and petroleum management?",
                [
                    "Understanding why these resources are limited",
                    "Understanding conservation",
                    "Understanding environmental effects",
                    "Remembering alternatives",
                    "Applying sustainable-use ideas"
                ]
            )
        }

        while True:

            print("\n----------------------------------------")
            print("           CHAPTER SELECTION")
            print("----------------------------------------\n")

            for number, chapter_name in chapters.items():
                print(f"{number}. {chapter_name}")

            print("\n15. I am not having difficulty in any chapter")

            chapter_choice = input(
                "\nWhich Science chapter are you not clear about? "
                "(enter the number): "
            ).strip()

            if chapter_choice == "15":
                print("\nThat's great! 😎")
                print("You don't currently have a specific Science chapter")
                print("that you feel unclear about.")
                break

            if chapter_choice not in chapters:
                print("\nInvalid choice.")
                print("Please choose a chapter number from 1 to 14.")
                continue

            chapter = chapters[chapter_choice]

            print("\n========================================")
            print(f"        {chapter.upper()}")
            print("========================================\n")

            # Q5
            # Show the ACTUAL topic names.
            # Q5 stores the selected topic name for MySQL.
            topic_options = sorted(
                [
                    key[1]
                    for key in topic_questions
                    if key[0] == chapter_choice
                ],
                key=int
            )

            topic_names = {
                "1": {
                    "1": "Writing and balancing chemical equations",
                    "2": "Types of chemical reactions",
                    "3": "Oxidation and reduction",
                    "4": "Effects of oxidation (corrosion and rancidity)"
                },
                "2": {
                    "1": "Properties of acids and bases",
                    "2": "Reactions of acids and bases",
                    "3": "pH scale",
                    "4": "Salts"
                },
                "3": {
                    "1": "Physical properties of metals and non-metals",
                    "2": "Chemical properties of metals",
                    "3": "Reactivity series",
                    "4": "Ionic compounds",
                    "5": "Extraction of metals"
                },
                "4": {
                    "1": "Covalent bonding",
                    "2": "Carbon's bonding and versatility",
                    "3": "Homologous series and nomenclature",
                    "4": "Chemical properties of carbon compounds",
                    "5": "Ethanol and ethanoic acid"
                },
                "5": {
                    "1": "Nutrition",
                    "2": "Respiration",
                    "3": "Transportation in humans",
                    "4": "Transportation in plants",
                    "5": "Excretion"
                },
                "6": {
                    "1": "Nervous system",
                    "2": "Reflex actions",
                    "3": "Hormones",
                    "4": "Plant movements"
                },
                "7": {
                    "1": "Asexual reproduction",
                    "2": "Sexual reproduction in plants",
                    "3": "Human reproduction",
                    "4": "Reproductive health"
                },
                "8": {
                    "1": "Mendel's experiments",
                    "2": "Inheritance",
                    "3": "Sex determination",
                    "4": "Evolution"
                },
                "9": {
                    "1": "Reflection of light",
                    "2": "Spherical mirrors",
                    "3": "Refraction",
                    "4": "Lenses",
                    "5": "Ray diagrams and numericals"
                },
                "10": {
                    "1": "Human eye",
                    "2": "Defects of vision",
                    "3": "Atmospheric refraction",
                    "4": "Dispersion and scattering"
                },
                "11": {
                    "1": "Electric current and potential difference",
                    "2": "Ohm's law",
                    "3": "Resistance and resistivity",
                    "4": "Series and parallel circuits",
                    "5": "Electric power and energy"
                },
                "12": {
                    "1": "Magnetic fields",
                    "2": "Magnetic field due to current",
                    "3": "Electromagnetic induction",
                    "4": "Electric motors",
                    "5": "Domestic electric circuits"
                },
                "13": {
                    "1": "Ecosystems",
                    "2": "Food chains and energy flow",
                    "3": "Ozone and environmental problems",
                    "4": "Biodegradable and non-biodegradable waste"
                },
                "14": {
                    "1": "Sustainable development",
                    "2": "Forest and wildlife conservation",
                    "3": "Water management",
                    "4": "Coal and petroleum management"
                }
            }

            print("Which specific topic are you finding difficult?\n")

            for topic_number in topic_options:
                print(
                    f"{topic_number}. "
                    f"{topic_names[chapter_choice][topic_number]}"
                )

            Q5_choice = input(
                "\nEnter the topic number: "
            ).strip()

            while (chapter_choice, Q5_choice) not in topic_questions:
                print("Please enter a valid topic number.")
                Q5_choice = input("Enter the topic number: ").strip()

            # Q5 is now the ACTUAL topic name.
            Q5 = topic_names[chapter_choice][Q5_choice]

            question, choices = topic_questions[
                (chapter_choice, Q5_choice)
            ]

            # ====================================================
            # Q_6 - SPECIFIC DIFFICULTY
            # ====================================================

            print("\n----------------------------------------")
            print("       LET'S UNDERSTAND THE PROBLEM")
            print("----------------------------------------\n")

            print(question)

            for index, choice in enumerate(choices, start=1):
                print(f"{index}. {choice}")

            print("6. Something else.")

            Q_6 = input(
                "\nEnter your choice: "
            ).strip()

            while Q_6 not in ["1", "2", "3", "4", "5", "6"]:
                print("Please enter a number from 1 to 6.")
                Q_6 = input("Enter your choice: ").strip()

            if Q_6 == "6":

                other_problem = input(
                    "\nTell me what usually makes this topic difficult for you: "
                ).strip()

                difficulty = "Other: " + other_problem

            else:

                difficulty = choices[int(Q_6) - 1]

            # ====================================================
            # PERSONALIZED GUIDANCE
            # ====================================================

            print("\n========================================")
            print("          WHAT YOU CAN DO")
            print("========================================\n")

            if Q_6 != "6":

                problem = choices[int(Q_6) - 1]
                p = problem.lower()

                if (
                    "remember" in p
                    or "formula" in p
                    or "values" in p
                ):
                    print(
                        "Use active recall instead of repeatedly reading."
                    )
                    print(
                        "Close the book and reproduce the important "
                        "formulae, reactions, definitions or values."
                    )
                    print(
                        "Then solve a few direct questions without looking "
                        "at your notes."
                    )

                elif (
                    "choos" in p
                    or "identif" in p
                    or "select" in p
                ):
                    print(
                        "Before solving, identify what the question gives "
                        "you and what it asks you to find."
                    )
                    print(
                        "Then choose the law, formula, reaction, diagram "
                        "or concept that connects those two."
                    )

                elif (
                    "diagram" in p
                    or "draw" in p
                    or "reading" in p
                ):
                    print(
                        "Redraw the diagram without looking at the textbook."
                    )
                    print(
                        "Label the important parts and write the function "
                        "or principle beside each one."
                    )
                    print(
                        "Then solve a question using your own diagram."
                    )

                elif (
                    "equation" in p
                    or "reaction" in p
                    or "product" in p
                ):
                    print(
                        "Practise reactions as:"
                    )
                    print(
                        "Reactants → Conditions → Products → Observation/Reason"
                    )
                    print(
                        "Cover the products and try to predict them yourself."
                    )

                elif (
                    "sign" in p
                    or "substitut" in p
                    or "unit" in p
                ):
                    print(
                        "Write the formula first, substitute second, "
                        "calculate third and write the unit last."
                    )
                    print(
                        "Check signs, substitutions and units before moving on."
                    )

                elif (
                    "calculat" in p
                    or "mistake" in p
                ):
                    print(
                        "Keep a mistake log."
                    )
                    print(
                        "For every wrong answer, identify whether the error "
                        "was conceptual, formula-based, calculation-based "
                        "or due to units."
                    )
                    print(
                        "Redo the same question correctly."
                    )

                elif (
                    "understand" in p
                    or "concept" in p
                    or "distinguish" in p
                ):
                    print(
                        "Explain the concept in your own words as if you "
                        "were teaching someone else."
                    )
                    print(
                        "Then create one example and explain why it fits."
                    )

                elif (
                    "application" in p
                    or "unfamiliar" in p
                    or "situation" in p
                ):
                    print(
                        "Start with a familiar example and then practise "
                        "the same concept with different wording or data."
                    )
                    print(
                        "Before answering, write down what the question "
                        "is actually asking."
                    )

                elif (
                    "process" in p
                    or "pathway" in p
                ):
                    print(
                        "Write the process as a sequence:"
                    )
                    print(
                        "START → STEP 1 → STEP 2 → STEP 3 → RESULT"
                    )
                    print(
                        "Close the book and reproduce the sequence from memory."
                    )

                else:
                    print(
                        "Break the problem into smaller steps."
                    )
                    print(
                        "Study one worked example, close the solution, "
                        "and solve a similar question independently."
                    )

            else:

                print(
                    "Your own explanation is useful because it can reveal "
                    "a difficulty that the options did not cover."
                )
                print(
                    "Try identifying the exact step where you get stuck."
                )

            # ====================================================
            # MYSQL SAVE
            # ====================================================

            Database.save_response(
                Roll_no=Roll,
                Student_name=Q_name,
                student_class="10",
                Student_Section=Q4_1,
                subject="Science",
                chapter=chapter,
                topic=Q5,
                difficulty=difficulty
            )

            # ====================================================
            # LOOP
            # ====================================================

            print("\n----------------------------------------")

            another = input(
                "Are there any other Science chapters you are not clear about? "
                "(yes/no): "
            ).strip().lower()

            if another == "yes":
                print("\nOkay! Let's identify the next chapter. 🔄")
                continue

            print("\n========================================")
            print("       SCIENCE ASSESSMENT COMPLETED")
            print("========================================\n")
            break
        
    def social_science(self, Roll, Q_name, Q4_1):

        print("\n========================================")
        print("      CLASS 10 SOCIAL SCIENCE")
        print("========================================\n")

        # ====================================================
        # SOCIAL SCIENCE SUBPARTS
        # ====================================================

        subparts = {
            "1": "Geography",
            "2": "History",
            "3": "Political Science",
            "4": "Economics"
        }

        chapters = {

            "1": {
                "1": "Resources and Development",
                "2": "Forest and Wildlife Resources",
                "3": "Water Resources",
                "4": "Agriculture",
                "5": "Minerals and Energy Resources",
                "6": "Manufacturing Industries",
                "7": "Lifelines of National Economy"
            },

            "2": {
                "1": "The Rise of Nationalism in Europe",
                "2": "Nationalism in India",
                "3": "The Making of a Global World",
                "4": "The Age of Industrialisation",
                "5": "Print Culture and the Modern World"
            },

            "3": {
                "1": "Power Sharing",
                "2": "Federalism",
                "3": "Gender, Religion and Caste",
                "4": "Political Parties",
                "5": "Outcomes of Democracy"
            },

            "4": {
                "1": "Development",
                "2": "Sectors of the Indian Economy",
                "3": "Money and Credit",
                "4": "Globalisation and the Indian Economy",
                "5": "Consumer Rights"
            }
        }

        # ====================================================
        # TOPIC-SPECIFIC DIAGNOSTIC QUESTIONS
        # ====================================================

        topic_questions = {

            # ---------------- GEOGRAPHY ----------------

            ("1", "1"): (
                "What is hardest for you in Resources and Development?",
                [
                    "Understanding the classification of resources",
                    "Understanding resource planning",
                    "Understanding land resources and land degradation",
                    "Understanding soil types and soil conservation",
                    "Applying the concepts to map or case-based questions"
                ],
                [
                    "Make a classification table of resources based on origin, exhaustibility, ownership and status of development.",
                    "Study resource planning as a sequence: identification → planning structure → matching resources with technology and institutions.",
                    "Create a cause → effect → solution table for land degradation.",
                    "Make a soil table containing type, characteristics, crops and conservation methods.",
                    "Practise one map/case question after every revision session."
                ]
            ),

            ("1", "2"): (
                "What is hardest for you in Forest and Wildlife Resources?",
                [
                    "Understanding biodiversity and its importance",
                    "Distinguishing different categories of species",
                    "Understanding causes of depletion",
                    "Understanding conservation methods",
                    "Remembering examples and case studies"
                ],
                [
                    "Create a small table for biodiversity, flora and fauna with examples.",
                    "Use a comparison table for normal, endangered, vulnerable, rare and endemic species.",
                    "Learn depletion as cause → impact → consequence.",
                    "Separate conservation methods into protected areas, species protection and community participation.",
                    "Revise examples through short case cards instead of memorising paragraphs."
                ]
            ),

            ("1", "3"): (
                "What is hardest for you in Water Resources?",
                [
                    "Understanding water scarcity",
                    "Understanding multipurpose river projects",
                    "Understanding advantages and disadvantages of dams",
                    "Understanding rainwater harvesting",
                    "Answering case-based questions"
                ],
                [
                    "Make a cause-and-effect chain for water scarcity.",
                    "Create a two-column table of benefits and problems of multipurpose projects.",
                    "Practise explaining dams from economic, social and environmental viewpoints.",
                    "Draw and label one rainwater-harvesting system.",
                    "Practise case questions by first identifying the water-management concept being tested."
                ]
            ),

            ("1", "4"): (
                "What is hardest for you in Agriculture?",
                [
                    "Understanding types of farming",
                    "Remembering cropping patterns",
                    "Understanding major crops and their conditions",
                    "Understanding technological and institutional reforms",
                    "Answering map or application questions"
                ],
                [
                    "Make a table comparing primitive subsistence, intensive subsistence and commercial farming.",
                    "Create a crop calendar for major cropping patterns.",
                    "For each major crop, learn temperature, rainfall, soil and major producing areas.",
                    "Separate technological reforms from institutional reforms.",
                    "Practise agriculture map work regularly instead of only before exams."
                ]
            ),

            ("1", "5"): (
                "What is hardest for you in Minerals and Energy Resources?",
                [
                    "Classifying minerals",
                    "Understanding occurrence and distribution",
                    "Remembering major mineral-producing areas",
                    "Understanding conventional and non-conventional energy",
                    "Map-based questions"
                ],
                [
                    "Use a table for metallic/non-metallic minerals and their examples.",
                    "Learn mineral occurrence through simple diagrams and region associations.",
                    "Make a state/region revision map for important minerals.",
                    "Compare conventional and non-conventional energy sources.",
                    "Practise blank-map identification repeatedly."
                ]
            ),

            ("1", "6"): (
                "What is hardest for you in Manufacturing Industries?",
                [
                    "Understanding factors affecting industrial location",
                    "Classifying industries",
                    "Understanding major industries",
                    "Understanding industrial pollution",
                    "Map and case-based questions"
                ],
                [
                    "Make a checklist of raw material, labour, power, capital, market and transport.",
                    "Create an industry classification table.",
                    "For each major industry learn location factors, importance and major centres.",
                    "Study pollution as source → pollutant → effect → control.",
                    "Practise industry locations on a blank map."
                ]
            ),

            ("1", "7"): (
                "What is hardest for you in Lifelines of National Economy?",
                [
                    "Understanding different modes of transport",
                    "Remembering important transport networks",
                    "Understanding international trade",
                    "Understanding tourism as a trade",
                    "Map-based questions"
                ],
                [
                    "Make a comparison table for roadways, railways, pipelines, waterways and airways.",
                    "Use maps to connect important transport routes and locations.",
                    "Learn international trade through exports, imports and balance of trade.",
                    "Connect tourism with employment, foreign exchange and cultural exchange.",
                    "Practise map locations regularly."
                ]
            ),

            # ---------------- HISTORY ----------------

            ("2", "1"): (
                "What is hardest for you in The Rise of Nationalism in Europe?",
                [
                    "Understanding the French Revolution and nationalism",
                    "Remembering the sequence of European events",
                    "Understanding liberalism and nationalism",
                    "Understanding unification of Germany and Italy",
                    "Interpreting historical sources or questions"
                ],
                [
                    "Build a timeline from the French Revolution to German and Italian unification.",
                    "Make a cause → event → consequence chain for major developments.",
                    "Compare political, economic and social meanings of liberalism.",
                    "Use separate short timelines for German and Italian unification.",
                    "Practise source questions by identifying the historical context first."
                ]
            ),

            ("2", "2"): (
                "What is hardest for you in Nationalism in India?",
                [
                    "Understanding the effects of the First World War",
                    "Understanding Non-Cooperation and Civil Disobedience",
                    "Remembering important events and dates",
                    "Understanding participation of different social groups",
                    "Interpreting sources and analysing questions"
                ],
                [
                    "Create a chronological timeline of the major national movements.",
                    "For each movement learn cause → programme → participation → withdrawal/result.",
                    "Use event cards for important dates instead of rereading the chapter.",
                    "Make a table comparing how different social groups participated.",
                    "For source questions, identify who, when, why and what the source is describing."
                ]
            ),

            ("2", "3"): (
                "What is hardest for you in The Making of a Global World?",
                [
                    "Understanding the pre-modern global world",
                    "Understanding the nineteenth-century world economy",
                    "Understanding colonialism",
                    "Understanding migration and trade",
                    "Connecting historical events with globalisation"
                ],
                [
                    "Create a timeline showing major phases of global connections.",
                    "Separate trade, migration, technology and capital as four recurring themes.",
                    "Study colonialism through causes, economic effects and human consequences.",
                    "Make a flowchart showing how migration and trade connected regions.",
                    "After each section explain how it contributed to a more connected world."
                ]
            ),

            ("2", "4"): (
                "What is hardest for you in The Age of Industrialisation?",
                [
                    "Understanding proto-industrialisation",
                    "Understanding the growth of factories",
                    "Understanding the role of workers",
                    "Understanding industrialisation in India",
                    "Remembering examples and interpreting sources"
                ],
                [
                    "Compare production before factories and factory production.",
                    "Make a sequence: proto-industrialisation → factories → industrial society.",
                    "Create a worker-focused table covering wages, conditions and employment.",
                    "Study Indian industrialisation through major industries and entrepreneurs.",
                    "Use source questions to practise extracting evidence."
                ]
            ),

            ("2", "5"): (
                "What is hardest for you in Print Culture and the Modern World?",
                [
                    "Understanding the invention and spread of print",
                    "Understanding print and religious debates",
                    "Understanding print and social reform",
                    "Understanding print and nationalism",
                    "Remembering examples and analysing sources"
                ],
                [
                    "Build a timeline of print technology and its spread.",
                    "Make a cause-and-effect chart for print and religious debate.",
                    "Connect print with education, reform and public discussion.",
                    "Study how print contributed to nationalist ideas.",
                    "Practise source questions by identifying the message and historical context."
                ]
            ),

            # ---------------- POLITICAL SCIENCE ----------------

            ("3", "1"): (
                "What is hardest for you in Power Sharing?",
                [
                    "Understanding why power sharing is desirable",
                    "Understanding forms of power sharing",
                    "Understanding the Belgian example",
                    "Understanding the Sri Lankan example",
                    "Comparing different power-sharing arrangements"
                ],
                [
                    "Learn the prudential and moral reasons separately.",
                    "Create a four-part diagram for the major forms of power sharing.",
                    "Compare Belgium and Sri Lanka using a two-column table.",
                    "Focus on how accommodation can prevent conflict.",
                    "Practise identifying the form of power sharing in examples."
                ]
            ),

            ("3", "2"): (
                "What is hardest for you in Federalism?",
                [
                    "Understanding the key features of federalism",
                    "Distinguishing federal and unitary systems",
                    "Understanding the three lists",
                    "Understanding language policy and decentralisation",
                    "Applying federalism to Indian examples"
                ],
                [
                    "Make a checklist of the key features of federalism.",
                    "Create a comparison table between federal and unitary systems.",
                    "Memorise the Union, State and Concurrent Lists through examples.",
                    "Connect language policy and decentralisation with federal practice.",
                    "Practise identifying which level of government handles a given issue."
                ]
            ),

            ("3", "3"): (
                "What is hardest for you in Gender, Religion and Caste?",
                [
                    "Understanding gender division",
                    "Understanding communalism",
                    "Understanding caste inequalities",
                    "Understanding how social divisions affect politics",
                    "Writing balanced analytical answers"
                ],
                [
                    "Separate gender, religion and caste into three concept maps.",
                    "For communalism, learn the different forms rather than memorising one definition.",
                    "Connect caste with social and economic inequalities.",
                    "Practise identifying when social differences become political divisions.",
                    "Use point → explanation → example structure for long answers."
                ]
            ),

            ("3", "4"): (
                "What is hardest for you in Political Parties?",
                [
                    "Understanding the functions of political parties",
                    "Understanding challenges faced by parties",
                    "Understanding reforms",
                    "Remembering examples",
                    "Writing analytical answers"
                ],
                [
                    "Make a mind map of the major functions of political parties.",
                    "Create a challenge → consequence → reform table.",
                    "Learn reforms through the problem they are intended to address.",
                    "Use examples only after understanding the underlying concept.",
                    "Practise five-mark answers using clear headings and explanations."
                ]
            ),

            ("3", "5"): (
                "What is hardest for you in Outcomes of Democracy?",
                [
                    "Understanding accountable and responsive government",
                    "Understanding economic outcomes",
                    "Understanding reduction of inequality",
                    "Understanding accommodation of social diversity",
                    "Evaluating democracy through arguments"
                ],
                [
                    "Create a checklist of the major expected outcomes of democracy.",
                    "For each outcome write one explanation and one example.",
                    "Distinguish political equality from economic equality.",
                    "Practise questions where you must evaluate both strengths and limitations.",
                    "Use balanced answers rather than treating democracy as automatically perfect."
                ]
            ),

            # ---------------- ECONOMICS ----------------

            ("4", "1"): (
                "What is hardest for you in Development?",
                [
                    "Understanding different development goals",
                    "Understanding income and other criteria",
                    "Understanding national development",
                    "Understanding public facilities",
                    "Interpreting development data"
                ],
                [
                    "Compare monetary and non-monetary development goals.",
                    "Make a table of income, health, education, security and equality indicators.",
                    "Practise explaining why development goals can differ between people.",
                    "Connect public facilities with quality of life.",
                    "When given data, identify the indicator first and then interpret it."
                ]
            ),

            ("4", "2"): (
                "What is hardest for you in Sectors of the Indian Economy?",
                [
                    "Distinguishing primary, secondary and tertiary sectors",
                    "Understanding organised and unorganised sectors",
                    "Understanding public and private sectors",
                    "Calculating or interpreting employment and production data",
                    "Applying sector concepts to examples"
                ],
                [
                    "Create a three-sector table with activities and examples.",
                    "Compare organised and unorganised sectors using working conditions.",
                    "Compare public and private sectors by ownership and purpose.",
                    "Practise interpreting employment and production figures.",
                    "Classify real-life jobs into the correct sector."
                ]
            ),

            ("4", "3"): (
                "What is hardest for you in Money and Credit?",
                [
                    "Understanding the functions of money",
                    "Understanding formal and informal sources of credit",
                    "Understanding terms of credit",
                    "Understanding self-help groups",
                    "Analysing credit situations"
                ],
                [
                    "Learn money through its main functions rather than a single definition.",
                    "Create a comparison table of formal and informal credit.",
                    "For terms of credit, identify interest, collateral, documentation and repayment.",
                    "Study self-help groups as a sequence of saving → lending → support.",
                    "Practise case studies by identifying the type and terms of credit."
                ]
            ),

            ("4", "4"): (
                "What is hardest for you in Globalisation and the Indian Economy?",
                [
                    "Understanding globalisation",
                    "Understanding the role of MNCs",
                    "Understanding production across countries",
                    "Understanding liberalisation",
                    "Understanding the effects of globalisation"
                ],
                [
                    "Make a flowchart showing how production becomes global.",
                    "Study MNCs through investment, production and market connections.",
                    "Connect liberalisation with removal or reduction of trade barriers.",
                    "Separate positive and negative effects before writing an answer.",
                    "Practise case studies involving producers, workers and consumers."
                ]
            ),

            ("4", "5"): (
                "What is hardest for you in Consumer Rights?",
                [
                    "Understanding consumer exploitation",
                    "Remembering consumer rights",
                    "Understanding the consumer movement",
                    "Understanding legal redressal",
                    "Applying rights to real-life cases"
                ],
                [
                    "Make a compact table of each consumer right and what it protects.",
                    "Learn common forms of exploitation through examples.",
                    "Understand the consumer movement as a response to exploitation.",
                    "Create a simple path: complaint → evidence → appropriate redressal.",
                    "Practise case studies by first identifying which right has been affected."
                ]
            )
        }

        # ====================================================
        # MAIN LOOP
        # ====================================================

        while True:

            print("\n========================================")
            print("      WHICH PART ARE YOU FINDING HARD?")
            print("========================================\n")

            for number, name in subparts.items():
                print(f"{number}. {name}")

            print("5. I am not having difficulty in Social Science")

            subpart_choice = input(
                "\nEnter the number: "
            ).strip()

            if subpart_choice == "5":
                print("\nThat's great! 😎")
                print("You don't currently have a specific Social Science")
                print("area that you feel unclear about.")
                break

            while subpart_choice not in subparts:
                print("Please choose 1, 2, 3 or 4.")
                subpart_choice = input("Enter the number: ").strip()

            subpart = subparts[subpart_choice]

            # ====================================================
            # CHAPTER SELECTION
            # ====================================================

            print("\n========================================")
            print(f"          {subpart.upper()}")
            print("========================================\n")

            for number, chapter_name in chapters[subpart_choice].items():
                print(f"{number}. {chapter_name}")

            chapter_choice = input(
                "\nWhich chapter are you not clear about? "
            ).strip()

            while chapter_choice not in chapters[subpart_choice]:
                print("Please enter a valid chapter number.")
                chapter_choice = input(
                    "Enter the chapter number: "
                ).strip()

            chapter = chapters[subpart_choice][chapter_choice]

            # ====================================================
            # Q5 - ACTUAL TOPIC NAME
            # ====================================================

            topic_names = {

                ("1", "1"): [
                    "Classification of resources",
                    "Resource planning",
                    "Land resources and land degradation",
                    "Soil types and soil conservation",
                    "Resource and soil-based application questions"
                ],
                ("1", "2"): [
                    "Biodiversity",
                    "Categories of species",
                    "Causes of depletion",
                    "Conservation methods",
                    "Examples and case studies"
                ],
                ("1", "3"): [
                    "Water scarcity",
                    "Multipurpose river projects",
                    "Advantages and disadvantages of dams",
                    "Rainwater harvesting",
                    "Water-resource case studies"
                ],
                ("1", "4"): [
                    "Types of farming",
                    "Cropping patterns",
                    "Major crops and conditions",
                    "Technological and institutional reforms",
                    "Agriculture map and application questions"
                ],
                ("1", "5"): [
                    "Classification of minerals",
                    "Occurrence and distribution",
                    "Major mineral-producing areas",
                    "Conventional and non-conventional energy",
                    "Mineral map questions"
                ],
                ("1", "6"): [
                    "Factors affecting industrial location",
                    "Classification of industries",
                    "Major industries",
                    "Industrial pollution",
                    "Industry map and case-based questions"
                ],
                ("1", "7"): [
                    "Modes of transport",
                    "Important transport networks",
                    "International trade",
                    "Tourism as a trade",
                    "Lifelines map questions"
                ],

                ("2", "1"): [
                    "French Revolution and nationalism",
                    "European events and chronology",
                    "Liberalism and nationalism",
                    "Unification of Germany and Italy",
                    "Historical source questions"
                ],
                ("2", "2"): [
                    "First World War and its effects",
                    "Non-Cooperation Movement",
                    "Civil Disobedience Movement",
                    "Participation of different social groups",
                    "Source and analytical questions"
                ],
                ("2", "3"): [
                    "Pre-modern global world",
                    "Nineteenth-century world economy",
                    "Colonialism",
                    "Migration and trade",
                    "Global connections and their effects"
                ],
                ("2", "4"): [
                    "Proto-industrialisation",
                    "Growth of factories",
                    "Workers and industrial society",
                    "Industrialisation in India",
                    "Historical examples and sources"
                ],
                ("2", "5"): [
                    "Invention and spread of print",
                    "Print and religious debates",
                    "Print and social reform",
                    "Print and nationalism",
                    "Print-culture source questions"
                ],

                ("3", "1"): [
                    "Why power sharing is desirable",
                    "Forms of power sharing",
                    "Belgian example",
                    "Sri Lankan example",
                    "Comparing power-sharing arrangements"
                ],
                ("3", "2"): [
                    "Features of federalism",
                    "Federal and unitary systems",
                    "Three lists",
                    "Language policy and decentralisation",
                    "Indian federal examples"
                ],
                ("3", "3"): [
                    "Gender division",
                    "Communalism",
                    "Caste inequalities",
                    "Social divisions and politics",
                    "Analytical answers"
                ],
                ("3", "4"): [
                    "Functions of political parties",
                    "Challenges faced by political parties",
                    "Political reforms",
                    "Examples",
                    "Analytical answers"
                ],
                ("3", "5"): [
                    "Accountable and responsive government",
                    "Economic outcomes",
                    "Reduction of inequality",
                    "Accommodation of social diversity",
                    "Evaluating democracy"
                ],

                ("4", "1"): [
                    "Different development goals",
                    "Income and other criteria",
                    "National development",
                    "Public facilities",
                    "Development data interpretation"
                ],
                ("4", "2"): [
                    "Primary, secondary and tertiary sectors",
                    "Organised and unorganised sectors",
                    "Public and private sectors",
                    "Employment and production data",
                    "Sector-based application questions"
                ],
                ("4", "3"): [
                    "Functions of money",
                    "Formal and informal credit",
                    "Terms of credit",
                    "Self-help groups",
                    "Credit case studies"
                ],
                ("4", "4"): [
                    "Globalisation",
                    "Role of MNCs",
                    "Production across countries",
                    "Liberalisation",
                    "Effects of globalisation"
                ],
                ("4", "5"): [
                    "Consumer exploitation",
                    "Consumer rights",
                    "Consumer movement",
                    "Legal redressal",
                    "Consumer case studies"
                ]
            }

            current_topics = topic_names[(subpart_choice, chapter_choice)]

            print("\n----------------------------------------")
            print("       WHICH TOPIC IS DIFFICULT?")
            print("----------------------------------------\n")

            for index, topic_name in enumerate(current_topics, start=1):
                print(f"{index}. {topic_name}")

            Q5_choice = input(
                "\nEnter the topic number: "
            ).strip()

            while Q5_choice not in [
                str(i) for i in range(1, len(current_topics) + 1)
            ]:
                print("Please enter a valid topic number.")
                Q5_choice = input("Enter the topic number: ").strip()

            # Q5 contains the actual topic name.
            Q5 = current_topics[int(Q5_choice) - 1]

            # ====================================================
            # Q_6 - SPECIFIC DIFFICULTY
            # ====================================================

            question, responses, guidance = topic_questions[
                (subpart_choice, chapter_choice)
            ]

            print("\n----------------------------------------")
            print("       LET'S UNDERSTAND THE PROBLEM")
            print("----------------------------------------\n")

            topic_question = (
                f"What is hardest for you in {Q5}?"
            )

            print(topic_question)

            topic_responses = {
                "1": [
                    "I don't understand the basic concept.",
                    "I struggle to remember the important points.",
                    "I cannot connect the concept with examples.",
                    "I struggle to apply it in questions.",
                    "I understand it while studying but forget it in tests."
                ],
                "2": [
                    "I don't understand the sequence or explanation.",
                    "I struggle to remember important facts and examples.",
                    "I get confused between similar concepts.",
                    "I struggle with source/case-based questions.",
                    "I understand it but cannot write a complete answer."
                ],
                "3": [
                    "I don't understand the main concept.",
                    "I confuse different terms or examples.",
                    "I struggle to remember the key points.",
                    "I cannot apply the concept to a situation.",
                    "I know the concept but struggle to frame answers."
                ],
                "4": [
                    "I don't understand the basic economic idea.",
                    "I confuse definitions, terms or categories.",
                    "I struggle with examples and data.",
                    "I cannot apply the concept to case studies.",
                    "I understand it but struggle to explain it in exams."
                ]
            }

            choices = topic_responses[subpart_choice]

            for index, response in enumerate(choices, start=1):
                print(f"{index}. {response}")

            print("6. Something else.")

            Q_6 = input(
                "\nEnter your choice: "
            ).strip()

            while Q_6 not in ["1", "2", "3", "4", "5", "6"]:
                print("Please enter a number from 1 to 6.")
                Q_6 = input("Enter your choice: ").strip()

            if Q_6 == "6":

                other_problem = input(
                    "\nTell me what usually makes this topic difficult for you: "
                ).strip()

                difficulty = "Other: " + other_problem

            else:

                difficulty = choices[int(Q_6) - 1]

            # ====================================================
            # TOPIC-SPECIFIC GUIDANCE
            # ====================================================

            print("\n========================================")
            print("          WHAT YOU CAN DO")
            print("========================================\n")

            if Q_6 == "1":

                print(
                    f"Start by understanding {Q5} in your own words."
                )
                print(
                    "Read one small section, close the book, and explain "
                    "the idea without looking."
                )
                print(
                    "Then connect it to one example from the chapter."
                )

            elif Q_6 == "2":

                print(
                    f"For {Q5}, use active recall instead of rereading."
                )
                print(
                    "Make a short revision sheet containing only keywords, "
                    "dates, terms, examples or important points."
                )
                print(
                    "Close the book and reproduce them from memory."
                )

            elif Q_6 == "3":

                print(
                    f"For {Q5}, build connections instead of memorising "
                    "isolated facts."
                )
                print(
                    "Create a simple concept map showing:"
                )
                print(
                    "CAUSE → EVENT/CONCEPT → EFFECT → EXAMPLE"
                )
                print(
                    "Then explain the connection in your own words."
                )

            elif Q_6 == "4":

                print(
                    f"For {Q5}, practise application questions."
                )
                print(
                    "Before answering, identify the concept being tested."
                )
                print(
                    "Then write the relevant facts or principle and apply "
                    "them to the situation."
                )
                print(
                    "Do not immediately look at the answer."
                )

            elif Q_6 == "5":

                print(
                    f"For {Q5}, practise exam-style recall."
                )
                print(
                    "Study the topic, close the book, and write a short answer "
                    "from memory."
                )
                print(
                    "Then compare it with your notes and add only the missing points."
                )
                print(
                    "Repeat this with one longer question."
                )

            else:

                print(
                    f"Your own explanation of the difficulty in {Q5} is useful."
                )
                print(
                    "Break the problem into: concept → example → application → answer."
                )
                print(
                    "Work on the exact step where you usually get stuck."
                )

            # ====================================================
            # MYSQL SAVE
            # ====================================================

            Database.save_response(
                Roll_no=Roll,
                Student_name=Q_name,
                student_class="10",
                Student_Section=Q4_1,
                subject=f"Social Science - {subpart}",
                chapter=chapter,
                topic=Q5,
                difficulty=difficulty
            )

            # ====================================================
            # LOOP
            # ====================================================

            print("\n----------------------------------------")

            another = input(
                "Do you have a doubt in another Social Science part? "
                "(yes/no): "
            ).strip().lower()

            if another == "yes":
                print("\nOkay! Let's identify the next part. 🔄")
                continue

            print("\n========================================")
            print("   SOCIAL SCIENCE ASSESSMENT COMPLETED")
            print("========================================\n")
            break

    def english(self, Roll, Q_name, Q4_1):

        print("\n========================================")
        print("          CLASS 10 ENGLISH")
        print("========================================\n")

        parts = {
            "1": "Grammar",
            "2": "Writing Skills",
            "3": "Literature",
            "4": "Time Management"
        }

        topics = {

            "1": {
                "1": "Tenses",
                "2": "Subject-Verb Agreement",
                "3": "Modals",
                "4": "Reported Speech",
                "5": "Determiners",
                "6": "Gap Filling and Error Correction",
                "7": "Grammar in Context"
            },

            "2": {
                "1": "Formal Letter Writing",
                "2": "Analytical Paragraph",
                "3": "Writing Structure and Format",
                "4": "Content and Organisation",
                "5": "Grammar and Vocabulary in Writing",
                "6": "Time Management in Writing Tasks"
            },

            "3": {
                "1": "Reading and Understanding Prose",
                "2": "Poetry and Poetic Devices",
                "3": "Character and Theme Analysis",
                "4": "Extract-Based Questions",
                "5": "Long-Answer Questions",
                "6": "Literary Vocabulary and Interpretation"
            },

            "4": {
                "1": "Planning Time Before the English Exam",
                "2": "Reading Section Time Management",
                "3": "Grammar Section Time Management",
                "4": "Writing Section Time Management",
                "5": "Literature Section Time Management",
                "6": "Checking Answers Before Submission"
            }
        }

        # ====================================================
        # GRAMMAR NOTES + LONG RESPONSES
        # ====================================================

        grammar_notes = {

            "1": {
                "name": "Tenses",
                "note": """
Tenses show the time of an action or state.

Present Simple:
Used for habits, routines, facts and general truths.
Example: She studies every day.

Present Continuous:
Used for an action happening around the present time.
Example: She is studying now.

Present Perfect:
Used for an action completed with a connection to the present.
Example: She has completed her work.

Past Simple:
Used for a completed action in the past.
Example: She studied yesterday.

Past Continuous:
Used for an action that was continuing at a particular time in the past.
Example: She was studying at 7 PM.

Past Perfect:
Used for an action completed before another past action.
Example: She had studied before the test began.

Future forms:
Used for actions or events expected to happen later.
Example: She will study tomorrow.
""",
                "long": """
How to improve:
First learn the meaning and use of each tense instead of memorising only its
formula. Make a timeline for past, present and future. Then practise changing
the same sentence into different tenses. When answering a question, look for
time expressions such as yesterday, now, already, since, for and tomorrow.
Finally, check whether the verb agrees with the time and meaning of the sentence.
"""
            },

            "2": {
                "name": "Subject-Verb Agreement",
                "note": """
The verb must agree with the subject in number and person.

Singular subject → singular verb.
Example: The boy plays cricket.

Plural subject → plural verb.
Example: The boys play cricket.

Words between the subject and verb do not normally change the agreement.
Example: The box of chocolates is on the table.

With phrases such as either/or and neither/nor, agreement depends on the
subject closer to the verb.
""",
                "long": """
How to improve:
Do not choose the verb based on the nearest noun. First identify the main
subject. Remove extra phrases mentally and check whether the subject is
singular or plural. Then select the verb. Practise sentences containing
collective nouns, either/or, neither/nor and intervening phrases because these
are common sources of mistakes.
"""
            },

            "3": {
                "name": "Modals",
                "note": """
Modals are helping verbs that express ideas such as ability, possibility,
permission, obligation, necessity and advice.

Can/Could → ability or possibility.
May/Might → permission or possibility.
Must → strong necessity or obligation.
Should/Ought to → advice or expected action.
Will/Would → future, willingness or polite requests.

A modal is followed by the base form of the main verb.
Example: You should study regularly.
""",
                "long": """
How to improve:
Instead of memorising modals as isolated words, connect each modal with its
meaning. When a question contains a blank, ask what meaning is required:
ability, permission, possibility, obligation or advice. Then choose the modal.
After selecting it, check that the main verb remains in its base form.
"""
            },

            "4": {
                "name": "Reported Speech",
                "note": """
Reported speech tells someone what another person said without quoting the
exact words.

Direct:
He said, "I am tired."

Reported:
He said that he was tired.

When reporting speech, pay attention to pronouns, tense changes, time
expressions and question structure.

Common changes include:
am/is → was
are → were
will → would
can → could
today → that day
tomorrow → the next day
yesterday → the previous day
""",
                "long": """
How to improve:
First identify the reporting verb and the type of sentence: statement,
question, command, request or exclamation. Then change the pronouns according
to the speaker and listener. Next check tense and time-expression changes.
For questions, remember that reported questions use statement word order.
Practise one type at a time before mixing them.
"""
            },

            "5": {
                "name": "Determiners",
                "note": """
Determiners come before nouns and help identify quantity, possession or
specificity.

Common determiners include:
a, an, the
some, any
much, many
few, a few
little, a little
each, every
this, that, these, those
my, your, his, her, their

The correct determiner depends on the noun and the meaning of the sentence.
""",
                "long": """
How to improve:
First identify whether the noun is countable or uncountable and whether it
is singular or plural. Then consider whether the sentence needs quantity,
specificity or possession. Pay special attention to pairs such as few/a few
and little/a little because the meaning changes.
"""
            },

            "6": {
                "name": "Gap Filling and Error Correction",
                "note": """
Grammar questions often test several concepts together. A blank may require
a tense, modal, determiner, preposition or correct verb form.

For error correction, read the complete sentence first. Identify the subject,
verb, tense and relationship between the words before deciding what is wrong.
""",
                "long": """
How to improve:
Do not fill a blank immediately after reading only the two surrounding words.
Read the whole sentence and identify its meaning. Then check tense, subject-
verb agreement, determiners, modals and other grammar rules. For editing
questions, read the sentence once for meaning and a second time specifically
for grammar.
"""
            },

            "7": {
                "name": "Grammar in Context",
                "note": """
Context-based grammar requires you to choose the form that fits both the
grammar rule and the meaning of the passage.

A grammatically possible answer may still be wrong if it does not match the
context.
""",
                "long": """
How to improve:
Read the complete passage before answering when possible. Identify the
relationship between sentences and look for time clues, subject clues and
logical connections. Then apply the grammar rule. Finally reread the entire
passage with your answers inserted to check whether it sounds logically and
grammatically correct.
"""
            }
        }

        # ====================================================
        # DIAGNOSTIC RESPONSES
        # ====================================================

        responses = {

            "1": [
                "I don't understand the basic rule.",
                "I forget the rule while solving questions.",
                "I get confused between similar rules.",
                "I can understand the rule but cannot apply it.",
                "I make mistakes mainly because I work too quickly."
            ],

            "2": [
                "I don't know the correct format or structure.",
                "I struggle to organise my ideas.",
                "I cannot develop enough content.",
                "I make grammar or vocabulary mistakes.",
                "I take too much time to complete the answer."
            ],

            "3": [
                "I don't understand the passage or poem properly.",
                "I struggle to remember important details.",
                "I find interpretation and analysis difficult.",
                "I struggle with extract-based questions.",
                "I cannot write long answers with enough explanation."
            ],

            "4": [
                "I spend too much time on one section.",
                "I don't know how much time to allocate to each section.",
                "I rush near the end of the exam.",
                "I leave questions unfinished.",
                "I don't get enough time to check my answers."
            ]
        }

        # ====================================================
        # GUIDANCE
        # ====================================================

        def give_guidance(part, topic, Q_6, selected_response):

            print("\n========================================")
            print("          WHAT YOU CAN DO")
            print("========================================\n")

            if part == "Grammar":

                if Q_6 == "1":
                    print(
                        f"Since the basic rule in {topic} is unclear, "
                        "don't start with difficult questions."
                    )
                    print(
                        "\nRead the short notes below and reduce the rule "
                        "to one simple sentence in your own words."
                    )
                    print(
                        "Then solve 5 very easy examples before moving to "
                        "mixed questions."
                    )

                elif Q_6 == "2":
                    print(
                        f"For {topic}, use active recall."
                    )
                    print(
                        "\nRead the rule once, close the notes, and write "
                        "the rule from memory."
                    )
                    print(
                        "Then solve questions without opening the notes."
                    )

                elif Q_6 == "3":
                    print(
                        f"For {topic}, make a comparison table of the rules "
                        "you keep confusing."
                    )
                    print(
                        "\nWrite: Rule → clue → example → common mistake."
                    )
                    print(
                        "Then solve mixed questions where you must choose "
                        "between the rules."
                    )

                elif Q_6 == "4":
                    print(
                        f"Your problem in {topic} is likely application."
                    )
                    print(
                        "\nBefore choosing an answer, identify the clue in "
                        "the sentence that tells you which rule is needed."
                    )
                    print(
                        "Then apply the rule and reread the complete sentence."
                    )

                elif Q_6 == "5":
                    print(
                        f"For {topic}, accuracy needs to come before speed."
                    )
                    print(
                        "\nSlowly solve 10 questions while checking each rule."
                    )
                    print(
                        "After that, repeat a similar set with a time limit."
                    )

                matched_item = next(
                    (value for value in grammar_notes.values() if value["name"] == topic),
                    None
                )
                if matched_item:
                    print("\n----- SLIGHT NOTES -----")
                    print(matched_item["note"])
                    print("\n----- LONG RESPONSE / HOW TO IMPROVE -----")
                    print(matched_item["long"])

            elif part == "Writing Skills":

                if Q_6 == "1":
                    print(
                        f"For {topic}, first learn the required format."
                    )
                    print(
                        "Write the format from memory before practising full answers."
                    )

                elif Q_6 == "2":
                    print(
                        f"For {topic}, plan the answer before writing."
                    )
                    print(
                        "Use: purpose → main points → supporting details → conclusion."
                    )

                elif Q_6 == "3":
                    print(
                        f"For {topic}, make a quick outline before writing."
                    )
                    print(
                        "Use 2–4 clear points and develop each point with relevant detail."
                    )

                elif Q_6 == "4":
                    print(
                        f"For {topic}, leave a short checking period."
                    )
                    print(
                        "Check grammar, spelling, punctuation, format and clarity."
                    )

                elif Q_6 == "5":
                    print(
                        f"For {topic}, practise under a timer."
                    )
                    print(
                        "Start with an achievable time limit and gradually reduce it."
                    )

            elif part == "Literature":

                if Q_6 == "1":
                    print(
                        f"Read {topic} in small sections and explain each section "
                        "in your own words."
                    )

                elif Q_6 == "2":
                    print(
                        "Make a one-page revision sheet with characters, events, "
                        "themes, important ideas and key evidence."
                    )

                elif Q_6 == "3":
                    print(
                        "For interpretation questions, always connect your point "
                        "with evidence from the text and then explain the meaning."
                    )

                elif Q_6 == "4":
                    print(
                        "For extract questions, first identify the context, speaker, "
                        "situation and central idea before answering."
                    )

                elif Q_6 == "5":
                    print(
                        "Use this long-answer structure:"
                    )
                    print(
                        "Point → Explanation → Textual reference/example → Analysis → Conclusion."
                    )

            elif part == "Time Management":

                if Q_6 == "1":
                    print(
                        "Use a section-based time plan before the exam starts."
                    )
                    print(
                        "Do not allow one difficult question to consume the time "
                        "needed for several easier questions."
                    )

                elif Q_6 == "2":
                    print(
                        "Assign an approximate time budget to reading, grammar, "
                        "writing and literature before starting."
                    )

                elif Q_6 == "3":
                    print(
                        "Use checkpoints during the exam."
                    )
                    print(
                        "If a section is taking longer than planned, move on and "
                        "return later if time permits."
                    )

                elif Q_6 == "4":
                    print(
                        "Attempt questions according to your planned order and "
                        "keep a reserve of time for unfinished questions."
                    )

                elif Q_6 == "5":
                    print(
                        "Reserve the final few minutes for checking."
                    )
                    print(
                        "Check unanswered questions first, then grammar, spelling, "
                        "formats and obvious calculation/reading mistakes."
                    )

        # ====================================================
        # MAIN LOOP
        # ====================================================

        while True:

            print("\n========================================")
            print("       WHICH ENGLISH AREA?")
            print("========================================\n")

            for number, part_name in parts.items():
                print(f"{number}. {part_name}")

            print("5. I am not having difficulty in English")

            part_choice = input(
                "\nEnter the number: "
            ).strip()

            if part_choice == "5":
                print("\nThat's great! 😎")
                break

            while part_choice not in parts:
                print("Please choose 1, 2, 3 or 4.")
                part_choice = input("Enter the number: ").strip()

            part = parts[part_choice]

            # ====================================================
            # TOPIC SELECTION
            # ====================================================

            print("\n========================================")
            print(f"             {part.upper()}")
            print("========================================\n")

            for number, topic_name in topics[part_choice].items():
                print(f"{number}. {topic_name}")

            Q5_choice = input(
                "\nWhich topic are you finding difficult? "
            ).strip()

            while Q5_choice not in topics[part_choice]:
                print("Please enter a valid topic number.")
                Q5_choice = input(
                    "Enter the topic number: "
                ).strip()

            # Q5 stores the ACTUAL topic name.
            Q5 = topics[part_choice][Q5_choice]

            # ====================================================
            # Q_6
            # ====================================================

            print("\n----------------------------------------")
            print("       LET'S UNDERSTAND THE PROBLEM")
            print("----------------------------------------\n")

            print(
                f"What is hardest for you about {Q5}?"
            )

            current_responses = responses[part_choice]

            for index, response in enumerate(
                current_responses,
                start=1
            ):
                print(f"{index}. {response}")

            print("6. Something else.")

            Q_6 = input(
                "\nEnter your choice: "
            ).strip()

            while Q_6 not in ["1", "2", "3", "4", "5", "6"]:
                print("Please enter a number from 1 to 6.")
                Q_6 = input("Enter your choice: ").strip()

            if Q_6 == "6":

                other_problem = input(
                    "\nTell me what exactly is difficult for you: "
                ).strip()

                difficulty = "Other: " + other_problem

            else:

                difficulty = current_responses[
                    int(Q_6) - 1
                ]

            # ====================================================
            # GUIDANCE
            # ====================================================

            give_guidance(
                part,
                Q5,
                Q_6,
                difficulty
            )

            # ====================================================
            # MYSQL SAVE
            # ====================================================

            Database.save_response(
                Roll_no=Roll,
                Student_name=Q_name,
                student_class="10",
                Student_Section=Q4_1,
                subject=f"English - {part}",
                chapter=part,
                topic=Q5,
                difficulty=difficulty
            )

            # ====================================================
            # LOOP
            # ====================================================

            print("\n----------------------------------------")

            another = input(
                "Do you have a doubt in another English area? "
                "(yes/no): "
            ).strip().lower()

            if another == "yes":
                print("\nOkay! Let's identify the next area. 🔄")
                continue

            print("\n========================================")
            print("       ENGLISH ASSESSMENT COMPLETED")
            print("========================================\n")
            break
