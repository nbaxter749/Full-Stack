import random
import os
import pickle

def get_words(num):
    words_found=[]
    fin = open("words.txt")
    for line in fin:
        word = line.strip()
        if len(word) == num:
            words_found.append(word)
    fin.close()		
    return words_found

def replace_all(guess, word, letter):
    for pos in range(len(guess)):
        if word[pos] == letter:
            guess = guess[:pos] + letter + guess[pos+1:]
    return guess


# read high score table from pickled dictionary if it exists
if os.path.isfile("hangman_scores_dictionary.txt"):
    fin = open ("hangman_scores_dictionary.txt", "rb")
    high_scores = pickle.load(fin)
    fin.close()
else:
    high_scores = {}


number_of_letters = int(input("Enter word length: "))
words = get_words(number_of_letters)
print("There are {} words with {} letters".format(len(words), number_of_letters))

guess_word = words[random.randint(0, len(words) - 1)]

print("Guessing the word: {}".format(guess_word))

lives = 6
# Modification 1 - initialise the string of letters available
letters_available = "abcdefghijklmnopqrstuvwxyz"
guess_string = "_" * number_of_letters
while lives > 0:
    # show the string of letters available
    print("Letters available: {}".format(letters_available))
    this_letter = input("Guess a letter: ")
    if this_letter in guess_word:
        guess_string = replace_all(guess_string, guess_word, this_letter)
        if guess_string == guess_word:
            print("\nYou guessed the word!")
            break
    else:
        lives = lives -1
        print("Letter not found - Lives remaining: {}".format(lives))
    print("\n" + guess_string)
    # replace the guessed letter with _ in the string of letters available
    letters_available = letters_available.replace(this_letter, "_")
print("\nGame over!\n")

if guess_string == guess_word:
    #game is over and word was guessed
    player = input("Enter player name: ")
    score = lives * number_of_letters

    #update the high scores dictionary
    if player in high_scores:
        high_scores[player] = high_scores[player] + score
    else:
        high_scores[player] = score
    fout = open("hangman_scores_dictionary.txt", "wb")
    pickle.dump(high_scores, fout)
    fout.close()
    
else:
    # game is over but word was not guessed, so show it
    print("The word was - {}".format(guess_word))

# show the new current high scores
print("\nHIGH SCORES TABLE")
for person in high_scores.keys():
    print (str(high_scores[person]).rjust(4) + "   " + person)