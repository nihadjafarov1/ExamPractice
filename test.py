import re
from random import shuffle

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    UNDERLINE = '\033[4m'

# Define a class to store the question and its variants
class Question:
    def __init__(self, number, text, variants, correct):
        self.number = number # The question number
        self.text = text # The question text
        self.variants = variants # A dictionary of variants
        self.correct = correct

    def __str__(self):
        # A string representation of the question
        strquestion = self.text
        shuffledvariants = (list(self.variants.values()))
        shuffle(shuffledvariants)

        for variant in self.variants.keys():
            varianttext = shuffledvariants.pop()
            self.variants[variant] = varianttext
            strquestion += "\n" + f"{variant}) {varianttext}" 
        return strquestion

# Define a function to parse a text file and return a list of questions
def parse_questions(filename):
    questions = [] # A list to store the questions
    with open(filename, "r", encoding="utf-8") as f: # Open the file for reading
        question_number = None
        question_text = "" # A variable to store the question text
        question_variants = {} # A dictionary to store the question variants
        variant_key = "" # A variable to store the current variant key
        variant_value = "" # A variable to store the current variant value
        correct = "" # Variable to store the correct answer text

        for line in f: # Loop through each line in the file
            line = line.strip() # Remove any leading or trailing whitespace
            if line: # If the line is not empty
                if re.match(r'^\d+', line): # If the line starts with a digit, it is a new question
                    if question_text: # If there is an existing question, add it to the list
                        if variant_key: # If there is an existing variant, add it to the dictionary
                            question_variants[variant_key] = variant_value.strip()
                        questions.append(Question(question_number, question_text, question_variants, correct))
                    question_number = int(re.match(r'^\d+', line).group()) # Extract the question number
                    question_text = line # Set the new question text
                    question_variants = {} # Reset the question variants
                    correct = ""
                    variant_key = "" # Reset the variant key
                    variant_value = "" # Reset the variant value
                elif line[0].isalpha() and line[1] == ")": # If the line starts with a letter and a parenthesis, it is a new variant
                    if variant_key: # If there is an existing variant, add it to the dictionary
                        if variant_key == 'A':
                            correct = variant_value.strip()
                        question_variants[variant_key] = variant_value.strip()
                    variant_key = line[0] # Set the new variant key (A, B, C, D or E)
                    variant_value = line[3:] + "\n" # Set the new variant value (the rest of the line plus a newline)
                else: # If the line is neither a question nor a new variant, it is a continuation of the current variant
                    variant_value += line + "\n" # Append the line to the current variant value plus a newline
        if question_text: # If there is a remaining question, add it to the list
            if variant_key: # If there is an existing variant, add it to the dictionary
                question_variants[variant_key] = variant_value.strip()
            questions.append(Question(question_number, question_text, question_variants, correct))
    return questions # Return the list of questions

# Define a function to prompt the questions and wait for user input
def quiz(questions):
    total_questions = len(questions)
    correct_count = 0
    wrong_count = 0
    wrong_ones = []

    for i, question in enumerate(questions): # Loop through each question in the list
        print(f"Question {i + 1} of {total_questions}")
        print(question) # Print the question and its variants
        answer = input("Enter your answer (A, B, C, D, E) or type 'exit', 'quit', or 'q' to finish: ").strip().lower() # Get the user input and convert to lowercase

        if answer in ['exit', 'quit', 'q']: # Check if the user wants to exit
            print(bcolors.WARNING + "Quiz terminated early." + '\x1b[0m')
            break

        answer = answer.upper() # Convert answer to uppercase for comparison

        if answer in question.variants: # If the input is a valid variant key
            if question.variants[answer] == question.correct:
                correct_count += 1
                print(bcolors.OKGREEN + "\nCorrect\n" + '\x1b[0m')
            else:
                wrong_count += 1
                correct_variant = next(k for k, v in question.variants.items() if v == question.correct)
                print(bcolors.FAIL + f"\nFALSE\nCorrect answer: {correct_variant}) {question.correct}" + '\x1b[0m')
                wrong_ones.append(question.number) # Append the question number to the wrong_ones list
        else: # If the input is not valid
            wrong_count += 1
            correct_variant = next(k for k, v in question.variants.items() if v == question.correct)
            print(bcolors.WARNING + f"Invalid answer. Correct answer: {correct_variant}) {question.correct}" + '\x1b[0m') # Print an error message with the correct answer
            wrong_ones.append(question.number) # Append the question number to the wrong_ones list

        # Show current status
        print(f"Current: {i + 1}/{total_questions} - Correct: {correct_count} - Wrong: {wrong_count}")
        print() # Print an empty line

    # Show all wrong answer question numbers at the end of the quiz
    print(bcolors.WARNING + "Wrong answer question numbers: " + str(wrong_ones) + '\x1b[0m')

# Main program
filename = "test.txt" # The name of the text file containing questions
questions = parse_questions(filename) # Parse the text file and get the list of questions

shuffle(questions)

quiz(questions) # Start the quiz with the questions
