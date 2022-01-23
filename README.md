# Wordle-Solver
A basic solver for Wordle that utilizes a dictionary of five letter words and a scoring system to determine what the given word is.

# How to run
The program can be run as 'python main.py'. From here the user will be given an input string and then be asked to input the hint string. The way the user should enter the hint string is by using the following scheme: 0 = blank, 1 = yellow, 2 = green. 

# Results and Issues
Testing on over 5000 words from the answers.txt file (which is the same as fiveletterwords.txt) I have found that my algorithm works for approximately 98.7% of cases. Typically the words it fails on are the cases where it can't uniquely determine a word so it defaults (based off score) to the words with higher frequency letters like 'bears' vs 'gears' where g is more frequent that b so my algorithm would go with bears assuming there was no intermediate word that removed the letter b at that position from consideration.

For a complete list of words that this algorithm fails on you can look at log.txt where I have recorded all failed instances.

