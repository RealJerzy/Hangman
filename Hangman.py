# © HankiElama oy
# Beta Release v1.0.7

#Imports
from random import choice
import os
import sys
import ctypes
import json

#Open in fullscreen everytime
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

fullscreen = 3
window = kernel32.GetConsoleWindow()

user32.ShowWindow(window, fullscreen)

#Read JSON files
with open(os.path.join(sys.path[0], "assets/chats.json"), "r") as f:
  chats = json.loads(f.read())

with open(os.path.join(sys.path[0], "assets/words.json"), "r") as f:
  words = json.loads(f.read())

categories = []

for c in words["categories"]:
    categories.append(c)

if len(categories) == 0:
    print("No categories found in 'words.json'")
    os._exit(5000)

#GAME -->
alphabet = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"
specials = "- "

def print_line(s):
    os.system("cls")
    print(s)
    input()

for line in chats["prologue"]:
    print_line(line)

def ready():
    os.system("cls")
    userReady = input("Are you down to play a game of hangman? (yes/no): ").lower()
    os.system("cls")

    if userReady == "no":
        print(choice(chats["ready_neg"]))
        input()

        os._exit(0)

    elif userReady == "yes":
        print(choice(chats["ready_pos"]))
        input()

        choose_gamemode()

    else:
        print(choice(chats["dont_know"]))
        input()

        ready()

def choose_gamemode():
    def invalid():
        os.system("cls")
        print("Invalid input!", "You can choose gamemode by typing 1 or 2.", sep="\n")
        input()

        choose_gamemode()

    global userGamemode

    os.system("cls")
    print("Gamemodes:", "", "1. Default", "2. Random category", "", sep="\n")

    try:
        userGamemode = int(input("Which gamemode would you like to play? (1-2): "))
        os.system("cls")
    
    except ValueError:
        invalid()

    if userGamemode == 1:
        print(choice(chats["default_mode"]))
        input()

        choose_category()
    
    elif userGamemode == 2:
        print(choice(chats["random_mode"]))
        input()

        choose_random_category()
    
    else:
        invalid()

def choose_category():
    def invalid():
        os.system("cls")
        print("Invalid input!",
            "You can choose the category by using the numbers 1-" + str(len(categories)) + " on your keyboard.", sep="\n")
        input()

        choose_category()

    os.system("cls")
    for c in categories:
        print(str(categories.index(c) + 1) + ". " + c["name"])

    try:
        userCategoryNum = int(input("Which category would like to play? (1-" + str(len(categories)) + "): "))
        os.system("cls")

    except ValueError:
        invalid()

    global userCategory

    if userCategoryNum >= 1 and userCategoryNum <= len(categories):
        userCategory = categories[userCategoryNum - 1]

        print(choice(chats["ready_pos"]))
        input()

        rules()
    
    else:
        invalid()

def choose_random_category():

    global userCategory
    userCategory = choice(categories)

    rules()

def rules():
    os.system("cls")
    userRules = input("So, do you know the rules of hangman? (yes/no): ").lower()
    os.system("cls")

    if userRules == "yes":
        print(choice(chats["rules_pos"]))
        input()

        os.system("cls")
        print("Here's your first word.")
        input()

        play()

    elif userRules == "no":
        print(choice(chats["rules_neg"]))
        input()

        for line in chats["rules"]:
            print_line(line)

        play()

    else:
        print(choice(chats["dont_know"]))
        input()

        rules()

def play():
    guessedLetters = []
    guessedWords = []
    attempts = 5
    correct = False
    word = choice(userCategory["words"])
        
    while correct == False and attempts > 0:
        show = ""
        current = ""

        for char in word:
            if char == " " or char == "-" or char in guessedLetters:
                current += char
            else:
                current += '_'

        show = ' '.join(current)

        if current == word:
            correct = True
        
        else:
            os.system("cls")
            print(show, "You have " + str(attempts) + " tries left.", sep="\n")
            guess = input("Please enter your guess. It can be a character or a full word: ")
            os.system("cls")

            if len(guess) == 0:
                print(choice(chats["blank_input"]))
                input()

            elif len(guess) == 1:
                if guess in guessedLetters:
                    print(choice(chats["guessed"]))
                    input()

                elif guess not in specials:
                    if guess not in alphabet and guess not in specials and guess not in numbers:
                        print(choice(chats["invalid_character"]))
                        input()

                    elif guess not in word:
                        guessedLetters.append(guess)
                        attempts -= 1

                        print(choice(chats["incorrect"]))
                        input()
                    
                    else:
                        guessedLetters.append(guess)

                        print(choice(chats["correct"]))
                        input()

                else:
                    print(choice(chats["only_letters"]))
                    input()

            elif len(guess) == len(word):
                if guess == word:
                    correct = True

                elif guess in guessedWords:
                    print(choice(chats["guessed"]))
                    input()

                else:
                    guessedWords.append(guess)
                    attempts -= 1

                    print(choice(chats["incorrect"]))
                    input()

            else:
                print(choice(chats["wrong_amount"]))
                input()
    else:
        os.system('cls')

        if correct == True:
            print(choice(chats["won_game"]))
            input()

            again()
        
        else:
            print(choice(chats["lost_game"]))
            input()

            again()

def again():
    os.system("cls")
    userAgain = input("Would you like to play again? (yes/no): ").lower()
    os.system("cls")

    if userAgain == "yes":
        print(choice(chats["replay_pos"]))
        input()

        play()

    elif userAgain == "no":
        print(choice(chats["replay_neg"]))
        input()

        os._exit(0)

    else:
        print(choice(chats["dont_know"]))
        input()

        again()
ready()