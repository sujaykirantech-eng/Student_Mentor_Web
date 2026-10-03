import time
import sys  
import random

class Breathe:
    def __init__(self):
        pass

    def breathing_exercise(self):
        print("Starting breathing exercise...\n")
        try:
            for cycle in range(3):
                # Clear line and print Breathe In
                sys.stdout.write("\r🟢 \a Breathe IN...  [4s]                    ")
                sys.stdout.flush()
                time.sleep(4)
                
                # Clear line and print Breathe Out
                sys.stdout.write("\r🔵 \a Breathe OUT... [4s]                    ")
                sys.stdout.flush()
                time.sleep(4)
                
                # Clear line and print Hold
                sys.stdout.write("\r⚪ \a Hold...        [4s]                    ")
                sys.stdout.flush()
                time.sleep(4)
                
            sys.stdout.write("\r                                             \r")
            sys.stdout.flush()
            print("Breathing exercise completed. Well done! 🌿\n")
                
        except KeyboardInterrupt:
            print("\n\nExercise stopped. Do you wish to continue with the program? (yes/no)")
            continue_response = input("> ").strip().lower()
            if continue_response == "yes":
                print("Continuing...")
            else:
                print("Exiting program.")

class Minigame:
    def __init__(self):
        pass
    
    def memory_game(self):
        print("Starting Memory Game...\n")
        choice = "yes"
        try:
            while choice == "yes":
                num = random.randint(100000, 999999)
                sys.stdout.write(f"\rRemember this number: {num}")
                sys.stdout.flush() 
                time.sleep(1.5)
                sys.stdout.write("\r" + " " * 40 + "\r") 
                sys.stdout.flush()
                user_input = input("Please enter the third digit of the number you just saw: ").strip()
                if user_input == str(num)[2]:
                    print("Correct! Well done.")
                else:
                    print(f"Incorrect. The correct answer was {str(num)[2]}.")
                choice = input("Would you like to try again? (yes/no): ").strip().lower()
            print("Exiting Memory Game.\n")
        except KeyboardInterrupt:
            print("\nThe game was interrupted.\n")
            
class PuzzleGame:
    def __init__(self):
        pass
    
    def puzzle_game(self):
        print("Starting Puzzle Game...\n")
        choice = "yes"
        try:
            while choice == "yes":
                puzzles = [
                    {"question": "What has keys but can't open locks?", "answer": "piano"},
                    {"question": "What has a heart that doesn't beat?", "answer": "artichoke"},
                    {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "m"}
                ]
                puzzle = random.choice(puzzles)
                user_input = input(f"Puzzle: {puzzle['question']} ").strip()
                if user_input.lower() == puzzle['answer']:
                    print("Correct! Well done.")
                else:
                    print(f"Incorrect. The correct answer was '{puzzle['answer']}'.")
                choice = input("Would you like to try another puzzle? (yes/no): ").strip().lower()
            print("Exiting Puzzle Game.\n")
        except KeyboardInterrupt:
            print("\nThe game was interrupted.\n")
