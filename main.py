from mimetypes import init
from turtle import position

# This initializes a score dictionary that contains keys of five letter words and scores values
# that aree determined based off combined letter frequency -- sourced from Wikipedia 
# and a metric that I found worked relatively well for determining how unique a string is. 
# I also take account for the fact that strings with multiple high frequency letters shouldn't have
# every letter regarded equally highly, so I scale the frequency score down based off how many times that character has 
# been seen in the string thus far
 
def initialize_scores():
    frequency_scores = {'e': 13, 't': 9.1, 'a': 8.2, 'o': 7.5, 'i': 7, 
                        'n': 6.7, 's': 6.3, 'h': 6.1, 'r': 6, 'd': 4.3,
                        'l': 4, 'c': 2.8, 'u': 2.8, 'm': 2.5, 'w': 2.4,
                        'f': 2.2, 'g': 2, 'y': 2, 'p': 1.9, 'b': 1.5, 'v': 0.98,
                        'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.095, 'z':0.074}

    five_letter_words = []

    with open("fiveletterwords.txt") as file:
        five_letter_words = file.read().splitlines()

    scores = {}

    for word in five_letter_words:
        unique_letters = 5 # Start with the maximum number of unique letters, decrement as we see repeats
        frequency_score = 0
        letters_accessed = []

        for letter in word:
            if(letter in letters_accessed): # Penalize strings that have multiple letters by making the frequnecy less highly valued
                frequency_score += 0.5*letters_accessed.count(letter) # Decrease frequency scores as we see them more often -- making a word like 'weeds' less valuable even though it has two high frequency letters
                unique_letters -= 1 # Decrease the uniqueness metric
            else: 
                frequency_score += frequency_scores[letter]

            letters_accessed.append(letter)

        scores[word] = frequency_score + 3*unique_letters # This is the overall metric I use and that I find works quite well

    # Sort the strings so we can easily access the highest valued string
    scores = dict(sorted(scores.items(), key = lambda item : item[1], reverse=True))

    return scores

# @param scores: a dictionary mapping five letter words to scores
# @param prev_string: string that generated the hint_string
# @param hint_string: a string encoding the results wordle gives back for 
# a given input. 0 = missed, 1 = yellow (letter in word but incorrect position), 
# 2 = green (correct letter in correct position
# 
# Purpose: Updates the scores of words based off the hints that Wordle gives us
def update_scores(scores, prev_string, hint_string):
    words_removed = 0
    keys_to_remove = []

    position_counter = 0

    for letter, hint in zip(prev_string, hint_string):
        if(hint == "0"): # Remove all words that contain letter in them
            for word_key in scores.keys():
                if(letter in word_key):
                    scores[word_key] = -1000 # Set the score to zero effectively making it not a possibility

        elif(hint == "1"): # Remove all words that contain 'letter' at the position in the prev_string
            for word_key in scores.keys():
                if(word_key[position_counter] == letter):
                    scores[word_key] = -1000

        elif(hint == "2"): # Increase the score of all words that contain the letter at a specific location
            for word_key in scores.keys():
                if(word_key[position_counter] == letter):
                    scores[word_key] += 10

        position_counter += 1

    scores = dict(sorted(scores.items(), key = lambda item : item[1], reverse=True))
    
# Interactive version of the script to be used by a person testing the program
def simulate_game_with_user_input():
    scores = initialize_scores()

    print("Welcome to Wordle solver! The following program begins with three predetermined words and will ask you to enter the help string")
    print("those words. The help string should be made by converting green to 2, yellow to 1, and blank to 0. For example,")
    print("if Wordle outputs green green blank blank yellow for the word atone, you would type 22001")
    print("\nAfter the first three rounds you will be given unique inputs based off the most likely choices from the previous three rounds\n")

    # Round 1 is always the same, start with 'atone'
    guess_1 = "atone"
    help_string = input("Help string for atone: ")
    update_scores(scores, guess_1, help_string)
    
    # Round 2 is always the same as well.
    guess_2 = "whirs"
    help_string = input("Help string for whirs: ")
    update_scores(scores, guess_2, help_string)

    # Round 3 is the last of the predetermined rounds
    guess_3 = "clump"
    help_string = input("Help string for clump: ")
    update_scores(scores, guess_3, help_string)

    for round in range(4):
        guess = max(scores, key=scores.get) # Get the word with the highest score currently and show the user that string

        hint_string = input(f"Help string for {guess}: ") # Have the user enter the Wordle help string

        update_scores(scores, guess, hint_string) # And now update the scores based off 

# Generates a help string given the answer and a guess string
def make_help_string(guess_string, answer):
    help_string = ""

    letter_counts = {} # This accounts for the cases where we have multiple of the same letter in the string

    for char in answer:
        if(char not in letter_counts):
            letter_counts[char] = answer.count(char)

    for ans_char, guess_char in zip(answer, guess_string):
        if(guess_char == ans_char):
            help_string += "2"
        elif(guess_char in letter_counts and letter_counts[guess_char] >= 1):
            help_string += "1"
            letter_counts[guess_char] -= 1
        else:
            help_string += "0"

    return help_string


# Non-interactive version used to test the script against given answers
def test_algorithm():
    results_file = open("log_file.txt", "w")

    answers = [] 
    correct_answers = 0
    round_sum = 0 # Used for finding the average round for correct answers

    # First 200 answers to Wordle
    # https://medium.com/@owenyin/here-lies-wordle-2021-2027-full-answer-list-52017ee99e86
    with open("answers.txt") as file:
        for line in file:
            answers.append(line.split()[0])

    # From here we basically run the algorithm and see if it gets the correct answer at any point
    for answer in answers:
        scores = initialize_scores()

        # Round 1 is always the same, start with 'atone'
        guess_1 = "atone"
        help_string = make_help_string(guess_1, answer)
        update_scores(scores, guess_1, help_string)
        
        # Round 2 is always the same as well.
        guess_2 = "whirs"
        help_string = make_help_string(guess_2, answer)
        update_scores(scores, guess_2, help_string)

        # Round 3 is the last of the predetermined rounds
        guess_3 = "clump"
        help_string = make_help_string(guess_3, answer)
        update_scores(scores, guess_3, help_string)

        for round in range(4):
            guess = max(scores, key = scores.get)
            help_string = make_help_string(guess, answer)

            update_scores(scores, guess, help_string)

        if(answer == guess):
            correct_answers += 1
        else:
            error_result = "Incorrect result of: " + str(guess) + " for expected result of: " + str(answer) + "\n"
            results_file.write(error_result)

    number_of_incorrect_answers = len(answers) - correct_answers
    correct_percentage = correct_answers / len(answers)

    percentage_results = "Percentage of correct answers: " + str(correct_percentage) + "\n"
    results_file.write(percentage_results)


simulate_game_with_user_input()