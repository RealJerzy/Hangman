# © HankiElama oy
# Beta Release b1.0.12

#Imports
from random import choice
import os, sys, ctypes, json

#Open in fullscreen everytime
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

fullscreen = 3
window = kernel32.GetConsoleWindow()

user32.ShowWindow(window, fullscreen)

#Read JSON files
try:
    try:
        with open(os.path.join(os.getcwd(), "assets/chats.json"), "r") as file:
            chats = json.loads(file.read())

    except json.JSONDecodeError:
        print("ERROR: Failed to decode file \"chats.json\"")
        input()
        os._exit(0)

    try:
        with open(os.path.join(os.getcwd(), "assets/words.json"), "r") as file:
            words = json.loads(file.read())

    except json.JSONDecodeError:
        print("ERROR: Failed to decode file \"words.json\"")
        input()
        os._exit(0)

except FileNotFoundError as missing:
    print("ERROR: File \"" + missing.filename.split("/")[1] + "\" not found")
    input()
    os._exit(0)

categories = []

for c in words["categories"]:
    categories.append(c)

if len(categories) == 0:
    print("ERROR: No categories found in \"words.json\"")
    input()
    os._exit(0)

#GAME -->
alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
numbers = "1234567890"
specials = "- "

def print_random(label):
    try:
        os.system('cls')
        print(choice(chats[label]))
        input()
    except(KeyError, IndexError):
        pass

def print_line(text):
    os.system("cls")
    print(text)
    input()

try:
    for line in chats["prologue"]:
        print_line(line)

except KeyError:
    pass

def ready():
    os.system("cls")
    userReady = input("Are you down to play a game of hangman? (yes/no): ").lower()

    if userReady == "no":
        print_random("ready_neg")

        os._exit(0)

    elif userReady == "yes":
        print_random("ready_pos")

        choose_gamemode()

    else:
        print_random("dont_know")

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
    
    except ValueError:
        invalid()

    if userGamemode == 1:
        print_random("default_mode")

        choose_category()
    
    elif userGamemode == 2:
        print_random("random_mode")

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
        userCategoryNum = int(input("\nWhich category would like to play? (1-" + str(len(categories)) + "): "))

    except ValueError:
        invalid()

    global userCategory

    if userCategoryNum >= 1 and userCategoryNum <= len(categories):
        userCategory = categories[userCategoryNum - 1]

        print_random("ready_pos")

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

    if userRules == "yes":
        print_random("rules_pos")

        os.system("cls")
        print("Here's your first word.")
        input()

        play()

    elif userRules == "no":
        print_random("rules_neg")

        try:
            for line in chats["rules"]:
                print_line(line)

        except KeyError:
            pass

        play()

    else:
        print_random("dont_know")

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

            if len(guess) == 0:
                print_random("blank_input")

            elif len(guess) == 1:
                if guess in guessedLetters:
                    print_random("guessed")

                elif guess not in specials:
                    if guess not in alphabet and guess not in specials and guess not in numbers:
                        print_random("invalid_character")

                    elif guess not in word:
                        guessedLetters.append(guess)
                        attempts -= 1

                        print_random("incorrect")
                    
                    else:
                        guessedLetters.append(guess)

                        print_random("correct")

                else:
                    print_random("only_letters")

            elif len(guess) == len(word):
                if guess == word:
                    correct = True

                elif guess in guessedWords:
                    print_random("guessed")

                else:
                    guessedWords.append(guess)
                    attempts -= 1

                    print_random("incorrect")

            else:
                print_random("wrong_amount")
    else:
        if correct == True:
            print_random("won_game")

            again()
        
        else:
            print_random("lost_game")

            again()

def again():
    os.system("cls")
    userAgain = input("Would you like to play again? (yes/no): ").lower()

    if userAgain == "yes":
        print_random("replay_pos")

        play()

    elif userAgain == "no":
        print_random("replay_neg")

        os._exit(0)

    else:
        print_random("dont_know")

        again()
ready()