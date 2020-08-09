# Pre-release b1.1.1

#Imports
from random import choice
from ctypes import WinDLL
import os, sys, json

#Title
def change_title(title):
    os.system('title ' + title)

change_title('Hangman')

#Open in fullscreen everytime
kernel32 = WinDLL('kernel32')
user32 = WinDLL('user32')

fullscreen = 3
window = kernel32.GetConsoleWindow()

user32.ShowWindow(window, fullscreen)

#Read JSON files
try:
    try:
        chats = json.loads(open(os.path.join(os.getcwd(), "assets/chats.json"), "r").read())
        plData = json.loads(open(os.path.join(os.getcwd(), "assets/player_data.json"), "r").read())

        categories = []

        for f in os.listdir(os.path.join(os.getcwd(), "assets/categories")):
            if f.lower().endswith(".json"):
                thisLoad = json.loads(open(os.path.join(os.getcwd(), "assets/categories", f), "r").read())

                #First, check if keys "name" and "words" exist in the current category
                if "name" in thisLoad and "words" in thisLoad:
                    #Second, check if either one is empty
                    if len(thisLoad["name"]) != 0 or len(thisLoad["words"]) != 0:
                        categories.append(thisLoad)

        if len(categories) == 0:
            print("ERROR: No categories found in \"assets/categories\"")
            input()
            os._exit(0)

    #If any JSON file is empty:
    except json.JSONDecodeError:
        print("ERROR: Failed to decode file \"" + str(f) + "\"")
        input()
        os._exit(0)

#If any JSON file cannot be found:
except FileNotFoundError as missing:
    print("ERROR: File \"" + missing.filename.split("/")[1] + "\" not found")
    input()
    os._exit(0)

#Write JSON files
data = {}
data["playerData"] = plData["playerData"]

def writePlayerData(data):
    json.dump(data, open(os.path.join(os.getcwd(), "assets/player_data.json"), "w"), indent=4)

#GAME -->
alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
numbers = "1234567890"
specials = "- "

def getUserInput(text):
    userInput = input(text).lower()
    
    if userInput == 'skip':
        if currentFunction == 'prologue':
            choose_gamemode()
        
        elif currentFunction == 'rules':
            play()
    
    elif userInput == 'skip intro forever':
        data['playerData']["skips"]["skipIntro"] = True
        writePlayerData(data)
        
        if currentFunction == 'prologue':
            choose_gamemode()

    elif userInput == 'statistics':
        print_statistics()

    elif userInput == 'quit':
        os._exit(0)

    elif userInput == 'help':
        os.system('cls')
        print('Write "skip" to skip prologue or rules.\nWrite "skip intro forever" to skip the intro forever.\nWrite "statistics" to read your game statistics\nWrite "quit" anytime to quit.')
        getUserInput('')

    return userInput

def print_random(label):
    try:
        os.system('cls')
        print(choice(chats[label]))
        getUserInput('')
    except(KeyError, IndexError):
        pass

def print_line(text):
    os.system("cls")
    print(text)
    getUserInput('')

def print_statistics():
    os.system('cls')
    print('Statistics:\n')

    for i in plData["playerData"]["statistics"]:
        print(plData["playerData"]["statistics"][i]["id"] + ':')
        print('     ' + str(plData["playerData"]["statistics"][i]["count"]))

    getUserInput('')

def prologue():
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name

    if plData["playerData"]["skips"]["skipIntro"] == False:
        try:
            for line in chats["prologue"]:
                print_line(line)

        except KeyError:
            pass

        while True:
            os.system("cls")
            userReady = getUserInput("Are you down to play a game of hangman? (yes/no): ")

            if userReady == "no":
                print_random("ready_neg")

                os._exit(0)

            elif userReady == "yes":
                print_random("ready_pos")
                break

            else:
                print_random("dont_know")
                
    choose_gamemode()

def choose_gamemode():
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name
    def invalid():
        os.system("cls")
        print("Invalid input!", "You can choose gamemode by typing 1 or 2.", sep="\n")
        getUserInput('')

        choose_gamemode()

    global userGamemode

    os.system("cls")
    print("Gamemodes:", "", "1. Default", "2. Random category", "", sep="\n")

    try:
        userGamemode = int(getUserInput("Which gamemode would you like to play? (1-2): "))
    
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
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name
    def invalid():
        os.system("cls")
        print("Invalid input!",
            "You can choose the category by using the numbers 1-" + str(len(categories)) + " on your keyboard.", sep="\n")
        getUserInput('')

        choose_category()

    os.system("cls")
    for c in categories:
        print(str(categories.index(c) + 1) + ". " + c["name"])

    try:
        userCategoryNum = int(getUserInput("\nWhich category would like to play? (1-" + str(len(categories)) + "): "))

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
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name

    if plData["playerData"]["skips"]["skipRules"] == False:
        os.system("cls")
        userRules = getUserInput("So, do you know the rules of hangman? (yes/no): ")

        if userRules == "yes":
            print_random("rules_pos")

            os.system("cls")
            print("Here's your first word.")
            getUserInput('')

        elif userRules == "no":
            print_random("rules_neg")

            try:
                for line in chats["rules"]:
                    print_line(line)

            except KeyError:
                pass

        else:
            print_random("dont_know")

            rules()

        data['playerData']["skips"]["skipRules"] = True
        writePlayerData(data)
    
    play()

def play():
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name
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
            guess = getUserInput("Please enter your guess. It can be a character or a full word: ")

            if len(guess) == 0:
                print_random("blank_input")

            elif len(guess) == 1:
                if guess in guessedLetters:
                    print_random("guessed")

                elif guess not in specials:
                    if guess not in alphabet and guess not in specials and guess not in numbers:
                        print_random("invalid_character")

                    else:
                        if guess not in word:
                            data["playerData"]["statistics"]["wrongGuesses"]["count"] += 1
                            guessedLetters.append(guess)
                            attempts -= 1

                            print_random("incorrect")
                        
                        else:
                            data["playerData"]["statistics"]["rightGuesses"]["count"] += 1
                            guessedLetters.append(guess)

                            print_random("correct")

                        data["playerData"]["statistics"]["guessesMade"]["count"] += 1
                        data["playerData"]["statistics"]["charactersGuessed"]["count"] += 1
                        writePlayerData(data)

                else:
                    print_random("only_letters")

            elif len(guess) == len(word):
                if guess in guessedWords:
                    print_random("guessed")

                else:
                    if guess == word:
                        data["playerData"]["statistics"]["rightGuesses"]["count"] += 1
                        correct = True
                        
                    else:
                        data["playerData"]["statistics"]["wrongGuesses"]["count"] += 1
                        guessedWords.append(guess)
                        attempts -= 1

                        print_random("incorrect")
                
                    data["playerData"]["statistics"]["guessesMade"]["count"] += 1
                    data["playerData"]["statistics"]["wordsGuessed"]["count"] += 1
                    writePlayerData(data)

            else:
                print_random("wrong_amount")
    else:
        if correct == True:
            data["playerData"]["statistics"]["roundsWon"]["count"] += 1

            print_random("won_game")
            os.system('cls')
            print('The correct word was "' + word + '".')
        
        else:
            data["playerData"]["statistics"]["roundsLost"]["count"] += 1

            print_random("lost_game")
            os.system('cls')
            print('The correct word would\'ve been "' + word + '".')

        data["playerData"]["statistics"]["roundsPlayed"]["count"] += 1
        writePlayerData(data)

        getUserInput('')

        again()

def again():
    global currentFunction
    currentFunction = sys._getframe().f_code.co_name
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

prologue()