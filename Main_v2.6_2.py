import Class
import Class10
import Class11
import Class12
import Database
import DoubtDiagnostic
from DoubtDiagnostic_General import DoubtDiagnostic_General

print("\n\nHello there 🫱🏻‍🫲🏻! I am your personal assistant and I am here to help you with your mental health.\n")
print("I will help you overcome your mental issues and help you to become a better version of yourself.\n")
print("Please answer my questions honestly and I will provide you with the best advice possible.\n")

Q4_1 = input("Enter Your Section: \n").strip()
Q_name = input("Enter Your Name: \n").strip()
Roll = input("Enter Your Roll Number: \n").strip()
mood = input("How are you feeling now? (happy/sad/angry/anxious/stressed): \n").strip().lower()

# ==========================================================
# MOOD & DE-STRESSING / WELLNESS SECTION
# ==========================================================
if mood in ("anxious", "stressed", "angry"):
    print("\nI understand that you're feeling anxious or stressed. It's important to take a deep breath and try to relax.")
    
    while True:    
        response = input("\nWould you like to play some mini games or do a breathing exercise to relax? (yes/no): \n").strip().lower()
        if response == "yes":
            print("\nGreat! Let's help you relax.")
            print("Here's a simple breathing exercise: Inhale for 4s, hold for 4s, exhale for 4s, and hold for 4s. Repeat this for a few minutes.")
            breathing_response = input("Would you like to try it now? (yes/no): \n").strip().lower()
            
            if breathing_response == "yes":
                print("\nLet's begin the breathing exercise. Follow the instructions and take your time.")
                breathe = Class.Breathe()
                breathe.breathing_exercise()
                breathe_mood = input("\nHow are you feeling now? (happy/sad/angry/anxious/stressed): \n").strip().lower()
                if breathe_mood in ("happy", "sad", "relaxed", "fine", "better"):
                    print("Glad to hear you're feeling more grounded now! 🌟")
                    break
                else:
                    print("Take your time. Let's see if another activity helps.")
                    continue
                
            elif breathing_response == "no":
                other_games_response = input("\nDo you need any other mini games or activities to help you relax? (yes/no): \n").strip().lower()
                
                if other_games_response == "yes":
                    print("\nHere are some mini games you can try:")
                    print("1. Memory Game: Try to remember a sequence of numbers or colors.")
                    print("2. Puzzle Game: Solve a simple puzzle or riddle.")
                    option = input("Enter the number of the game you want to play (1 or 2): \n").strip()
                    
                    if option == "1":
                        print("\nGreat! Let's play the Memory Game. I will show you a sequence of numbers, and you have to remember them.")
                        minigame = Class.Minigame()
                        minigame.memory_game()
                        option_next = input("\nWould you like to play the other game as well? (yes/no): \n").strip().lower()
                        if option_next == "yes":
                            print("\nGreat! Let's play the Puzzle Game.")
                            puzzle_game = Class.PuzzleGame()
                            puzzle_game.puzzle_game()
                            break
                        else:
                            break
                        
                    elif option == "2":
                        print("\nGreat! Let's play the Puzzle Game. I will give you a simple puzzle or riddle to solve.")
                        puzzle_game = Class.PuzzleGame()
                        puzzle_game.puzzle_game()
                        option_next = input("\nWould you like to play the other game as well? (yes/no): \n").strip().lower()
                        if option_next == "yes":
                            print("\nGreat! Let's play the Memory Game.")
                            minigame = Class.Minigame()
                            minigame.memory_game()
                            break
                        else:
                            break
                    else:
                        print("Invalid option. Please choose either 1 or 2.")
                        continue

                elif other_games_response == "no":
                    print("Understood! Let's take it one step at a time.")
                    break
                else:
                    print("Please answer yes or no.")
                    continue
            else:
                print("Please answer yes or no.")
                continue

        elif response == "no":
            print("No problem at all! Let's proceed directly.")
            break
        else:
            print("Please answer yes or no.")
            continue

elif mood in ("happy", "sad"):
    print(f"\nThank you for sharing how you feel, {Q_name}. Let's focus on supporting you today.")
else:
    print(f"\nThank you for checking in, {Q_name}. Whatever you are feeling right now is completely valid.")

# ==========================================================
# ACADEMIC MENTORING SECTION
# ==========================================================
print("\nOkay, let's take a look at your studies and academic workflow.\n")
print("Please answer the following questions honestly and I will provide you with the best guidance possible.\n")
print("Don't feel overwhelmed, take your time and answer each question carefully.\n")

Q_1 = input("Are you facing any difficulties in your studies? (yes/no): \n").strip().lower()

if Q_1 == "yes":
    print("\nRelax, I understand that you're facing difficulties in your studies. It's completely normal and we can work through it step by step.\n")
    Q_2 = input("Are you facing any difficulties in any specific subject? (yes/no): \n").strip().lower()
    
    # ----------------------------------------------------------
    # BRANCH 1: SUBJECT-SPECIFIC DIFFICULTY (Q_2 == "yes")
    # ----------------------------------------------------------
    if Q_2 == "yes":
        print("\nI understand that you're facing difficulties in a specific subject. Let's get your class details first:\n")
        
        while True:
            Q4 = input("Which class are you in? (10th/11th/12th): \n").strip().lower()
            if Q4 not in ("10th", "10", "11th", "11", "12th", "12"):
                print("Invalid class. Please enter 10th, 11th, or 12th.")
                continue
            
            # --- Check Previous History in Database ---
            previous_history = Database.check_student_history(Roll)
            
            if previous_history:
                print("\n🧠 Previous study records found!")
                print("==========================================")
                print(f"Student : {Q_name}")
                print(f"Roll No : {Roll}")
                print("\nYour previous recorded doubts:")
                for doubt in previous_history:
                    print("------------------------------------------")
                    print("Subject   :", doubt[0])
                    print("Chapter   :", doubt[1])
                    print("Topic     :", doubt[2])
                    print("Difficulty:", doubt[3])
                    print("Date      :", doubt[4])
                print("==========================================")
                
                Clarity_response = input("\nAre you clear with your previous doubts now? (yes/no): \n").strip().lower()
                
                if Clarity_response == "yes":
                    print("\nAwesome! Reviewing and mastering previous doubts builds solid momentum. Keep it up!")
                else:
                    print("\n🔄 No problem! Let's revisit your previous doubt.")
                    for i, doubt in enumerate(previous_history, start=1):
                        print(f"{i}. {doubt[0]} → {doubt[1]} → {doubt[2]}")

                    while True:
                        try:
                            choice = int(input("\nWhich doubt do you want to revisit? (Enter number): \n"))
                            if 1 <= choice <= len(previous_history):
                                break
                            print(f"❌ Enter a number between 1 and {len(previous_history)}.")
                        except ValueError:
                            print("❌ Please enter a valid number.")

                    selected_doubt = previous_history[choice - 1]
                    previous_subject = selected_doubt[0]
                    previous_chapter = selected_doubt[1]
                    previous_topic = selected_doubt[2]
                    previous_difficulty = selected_doubt[3]

                    print("\n==================================================")
                    print("             🔄 PREVIOUS DOUBT DETAILS")
                    print("==================================================")
                    print("Subject    :", previous_subject)
                    print("Chapter    :", previous_chapter)
                    print("Topic      :", previous_topic)
                    print("Previous difficulty notes:")
                    print(previous_difficulty)
                    print("==================================================")

                    still_confused = input("\nAre you still facing this difficulty? (yes/no): \n").strip().lower()
                    if still_confused == "yes":
                        diagnostic = DoubtDiagnostic.DoubtDiagnostic(
                            previous_subject,
                            previous_chapter,
                            previous_topic,
                            previous_difficulty
                        )
                        result = diagnostic.diagnose()
                    else:
                        print("\n🎉 Great! Looks like you've overcome that difficulty.")

                    another_check = input("\nDo you want to assess a new subject now? (yes/no): \n").strip().lower()
                    if another_check != "yes":
                        print("\nKeep up the great work! I'm always here whenever you need study help. 🚀")
                        break

            # --- Subject Selection Prompt ---
            print("\nAvailable Subjects:")
            print("Maths | Science | Social Science | English | Physics | Chemistry | Biology | Computer Science")
            Q_3 = input("\nWhich subject are you facing difficulties in?: \n").strip().lower()

            # Class availability guardrails
            if Q_3 in ("science", "social science") and Q4 not in ("10th", "10"):
                print("❌ This subject is available only for 10th class.")
                continue

            if Q_3 in ("physics", "chemistry", "biology", "computer science") and Q4 not in ("11th", "11", "12th", "12"):
                print("❌ This subject is available only for 11th and 12th class.")
                continue

            # --- Subject Routing ---
            if Q_3 == "maths":
                if Q4 in ("10th", "10"):
                    Class10.Class10().maths(Roll, Q_name, Q4_1)
                elif Q4 in ("11th", "11"):
                    Class11.Class11().maths(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().maths(Roll, Q_name, Q4_1)
                else:
                    print("Maths module is not available for this class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                
            elif Q_3 == "science":
                if Q4 in ("10th", "10"):
                    Class10.Class10().science(Roll, Q_name, Q4_1)
                else:
                    print("Science module is available only for 10th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                
            elif Q_3 == "social science":
                if Q4 in ("10th", "10"):
                    Class10.Class10().social_science(Roll, Q_name, Q4_1)
                else:
                    print("Social Science module is available only for 10th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                
            elif Q_3 == "english":
                if Q4 in ("10th", "10"):
                    Class10.Class10().english(Roll, Q_name, Q4_1)
                elif Q4 in ("11th", "11"):
                    Class11.Class11().english(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().english(Roll, Q_name, Q4_1)
                else:
                    print("English module is not available for this class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break

            elif Q_3 == "physics":
                if Q4 in ("11th", "11"):
                    Class11.Class11().physics(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().physics(Roll, Q_name, Q4_1)
                else:
                    print("Physics module is available only for 11th and 12th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                    
            elif Q_3 == "chemistry":
                if Q4 in ("11th", "11"):
                    Class11.Class11().chemistry(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().chemistry(Roll, Q_name, Q4_1)
                else:
                    print("Chemistry module is available only for 11th and 12th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                
            elif Q_3 == "biology":
                if Q4 in ("11th", "11"):
                    Class11.Class11().biology(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().biology(Roll, Q_name, Q4_1)
                else:
                    print("Biology module is available only for 11th and 12th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break
                    
            elif Q_3 == "computer science":
                if Q4 in ("11th", "11"):
                    Class11.Class11().computer_science(Roll, Q_name, Q4_1)
                elif Q4 in ("12th", "12"):
                    Class12.Class12().computer_science(Roll, Q_name, Q4_1)
                else:
                    print("Computer Science module is available only for 11th and 12th class.")

                continue_response = input("\nDo you still need help in another subject? (yes/no): \n").strip().lower()
                if continue_response == "yes":
                    continue
                else:       
                    break

            else:
                print("❌ Invalid subject. Please choose one of the listed subjects.")
                continue

    # ----------------------------------------------------------
    # BRANCH 2: GENERAL STUDY / NON-SUBJECT DIFFICULTY (Q_2 == "no")
    # ----------------------------------------------------------
    else:
        What_Else = input("\nAre you facing any other general difficulties in your studies? (yes/no): \n").strip().lower()
        
        if What_Else == "yes":
            print("\nPlease let me know what other difficulties you are facing in your studies and I will help you with them.\n")
            print(
                "That's completely okay. Not every study difficulty comes from a particular subject.\n"
                "Sometimes the difficulty may be related to your study environment, teachers, concentration, "
                "time management, motivation, friends, reading habits, revision, or your daily learning routine."
            )

            print(
                "\nI would like to understand what is actually happening before suggesting anything.\n"
                "Please describe your difficulty in your own words."
            )

            general_problem = input(
                "\nWhat difficulty are you facing in your studies? Please explain it honestly in your own words:\n> "
            ).strip()

            while not general_problem:
                print("\nPlease describe at least a little about what you are facing. There is no right or wrong answer.")
                general_problem = input("\nTell me what is troubling you:\n> ").strip()

            print("\nThank you for explaining it. Let's analyze your study workflow together.")
            
            while True:
                Q4 = input("\nWhich class are you in? (10th/11th/12th): \n").strip().lower()
                if Q4 in ("10th", "10", "11th", "11", "12th", "12"):
                    break
                print("Please enter a valid class (10th, 11th, or 12th).")

            # Check if Database has a get_last_general_diagnostic method, else pass None
            prev_record = None
            if hasattr(Database, "get_last_general_diagnostic"):
                prev_record = Database.get_last_general_diagnostic(Roll)

            diagnostic = DoubtDiagnostic_General(
                Roll_no=Roll,
                Student_name=Q_name,
                student_class=Q4,
                Student_Section=Q4_1,
                problem=general_problem,
                previous_record=prev_record
            )

            result = diagnostic.diagnose()

            # Save general diagnostic to MySQL database
            if hasattr(Database, "save_general_diagnostic"):
                Database.save_general_diagnostic(result)
            elif hasattr(diagnostic, "save_to_mysql_direct"):
                diagnostic.save_to_mysql_direct()

            print("\n" + "=" * 60)
            print("              GENERAL STUDY DIAGNOSIS REPORT")
            print("=" * 60)
            print(result)
            
        else:
            print("\nIf there are personal issues, emotional distress, or any other difficulties you are facing,")
            print("please connect with your school counselor, parents, or a trusted adult for caring support. You are never alone! 💙\n")

# ----------------------------------------------------------
# BRANCH 3: NO STUDY DIFFICULTIES (Q_1 == "no")
# ----------------------------------------------------------
else:
    print(f"\n🎉 That's fantastic to hear, {Q_name}! I am glad you are feeling confident and clear with your studies right now.")
    print("Consistency and a steady routine are the real keys to mastery. Keep up your excellent work!")
    print("If you ever hit a roadblock, need to test a chapter, or want to refresh your study habits, feel free to come back anytime. Have a wonderful day! 🌟\n")
