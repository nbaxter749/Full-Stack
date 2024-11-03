import random
import os

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

    #MODIFICATION 3 - high scores file maintains cumlative scores
    fin = open ("hangman_scores.txt", "r")
    # open a tempoary file for the updated output
    fout = open("temp.txt", "w")
    #need to keep track of whether the current player is a new one
    player_found = False
    #check each line in the scores file
    for line in fin:
        # split the line
        line_parts = line.strip().split(",")
        #does the player on this line match the name provided
        if line_parts[0] ==player:
            # names match, so add this score to the previous score in the file
            new_score = int(line_parts[1]) + score
            #line of output will be the players name and thier updated score
            new_line ="{},{}\n".format(line_parts[0], new_score)
            # record that the player was already in the scores file
            player_found = True
        else:
            # names dont match so line of output will be the oringinal name and score
            new_line ="{},{}\n".format(line_parts[0], line_parts[1])
        # add line of output to the temporary file
        fout.write(new_line)
    if not player_found:
        # all file entries checked and player not found
        #so add a line of output for the new player
        new_line = "{},{}".format(player, score)
        fout.write(new_line)
    fin.close()
    fout.close()
    #results file updated, so replace scores file with tempoary file
    os.replace("temp.txt" , "hangman_scores.txt")
else:

    # MODIFICATION 2 - game is over but word was not guessed, so show it
    print("The word was - {}".format(guess_word))


        
        