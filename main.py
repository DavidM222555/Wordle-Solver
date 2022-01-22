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

        scores[word] = frequency_score + 5*unique_letters # This is the overall metric I use and that I find works quite well

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

    if(hint_string == "11111"):
        print("You win!")
        return

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
    

def simulate_game():
    scores = initialize_scores()

    for x in range(6):
        guess = max(scores, key=scores.get) # Get the word with the highest score currently and show the user that string
        print("Input: ", guess) 

        hint_string = input("Hint string given for guess input: ") # Have the user enter the Wordle help string

        update_scores(scores, guess, hint_string) # And now update the scores based off 


simulate_game()
