#Pre-release b1.1.8


#Imports
from random import choice
from ctypes import WinDLL
from sys import _getframe
from time import sleep
from msvcrt import getwche, kbhit
from json import loads, dump, JSONDecodeError
from os import system, getcwd, path, listdir, _exit


#Screen setup
system("title Hangman")
system("color 7")

kernel32 = WinDLL("kernel32")
user32 = WinDLL("user32")

fullscreen = 3
window = kernel32.GetConsoleWindow()

user32.ShowWindow(window, fullscreen)


#Read JSON files
try:
    try:
        chats = loads(open(path.join(getcwd(), "assets/chats.json"), "r").read())
        plData = loads(open(path.join(getcwd(), "data/player_data.json"), "r").read())

        categories = []
        for f in listdir(path.join(getcwd(), "assets/categories")):
            if f.lower().endswith(".json"):
                thisLoad = loads(open(path.join(getcwd(), "assets/categories", f), "r").read())

                if ("name" and "words") in thisLoad:
                    if (len(thisLoad["name"]) or len(thisLoad["words"])) != 0:
                        categories.append(thisLoad)

        if len(categories) == 0:
            system("cls")
            print("ERROR: No categories found in \"assets/categories\"")
            input()
            _exit(0)

    #If any JSON file is empty:
    except JSONDecodeError:
        system("cls")
        print("ERROR: Failed to decode file \"" + str(f) + "\"")
        input()
        _exit(0)

#If any JSON file cannot be found:
except FileNotFoundError as missing:
    system("cls")
    print("ERROR: File \"" + missing.filename.split("/")[1] + "\" not found")
    input()
    _exit(0)


#Write JSON files
def writePlayerData(plData):
    dump(plData, open(path.join(getcwd(), "data/player_data.json"), "w"), indent = 4)


#Statistics
def print_statistics():
    out = ""
    out += "Statistics:\n\n"
    for i in plData["playerData"]["statistics"]:
        out += plData["playerData"]["statistics"][i]["id"] + ":\n"
        out += 5 * " " + str(plData["playerData"]["statistics"][i]["count"]) + "\n"

    print_line(out, None, None, None)


#Resetting
def reset(target):
    while True:
        if target == "Statistics":
            userReset = print_line("You are about to reset " + target
                                    + "!\nThis action can't be reverted!\nAre you sure?"
                                    , None, 4, 0.2)

            if userReset in ["yes", "y"]:
                for d in plData["playerData"]["statistics"]:
                    plData["playerData"]["statistics"][d]["count"] = 0

            elif userReset in ["no", "n"]:
                print_line("The reset has been cancelled.", None, None, None)
                break
        
            else:
                print_line("It's a freaking yes/no question! Lights on dummy fricky.", None, None, None)
                continue

        else:
            for d in plData["playerData"]["skips"]:
                plData["playerData"]["skips"][d] = False

        writePlayerData(plData)
        print_line(str(target) + " have been reset succesfully. ", None, None, None)
        break


#User input
def get_user_input(text):
    global commands
    commands = ["skip", "skip intro forever", "stats", "reset stats", "reset skips", "quit", "help"]

    userInput = input(text).lower()
    if userInput == "skip":
        if currentFunction == "prologue":
            choose_gamemode()
        
        elif currentFunction == "rules":
            play()

    elif userInput == "skip intro forever":
        plData["playerData"]["skips"]["skipIntro"] = True
        writePlayerData(plData)
        
        if currentFunction == "prologue":
            choose_gamemode()
            
    elif userInput == "stats":
        print_statistics()

    elif userInput == "reset stats":
        reset("Statistics")

    elif userInput == "reset skips":
        reset("Skips")

    elif userInput == "quit":
        _exit(0)

    elif userInput == "help":
        print_line("Write \"skip\" to skip prologue or rules.\nWrite \"skip intro forever\" to skip the intro forever.\nWrite \"statistics\" to read your game statistics\nWrite \"quit\" anytime to quit.", None, None, None)

    return userInput


#Printing
def print_line(text, random, color, delay):
    if text != None:
        while True:
            system("cls")
            print(text)

            if color != None:
                while True:
                    system("color 7")
                    sleep(delay)
                    system("color " + str(color))
                    sleep(delay)

                    if kbhit():
                        system("color 7")
                        break
        
            temporary = get_user_input("")
            if temporary not in commands:
                return temporary

    elif random != None:
        try:
            print_line(choice(chats[random]), None, color, delay)

        except(KeyError, IndexError):
            pass


#GAME -->
def prologue():
    global currentFunction
    currentFunction = _getframe().f_code.co_name

    if plData["playerData"]["skips"]["skipIntro"] == False:
        try:
            for line in chats["prologue"]:
                print_line(line, None, None, None)

        except KeyError:
            pass

        while True:
            printInput = print_line("Are you down to play a game of hangman? (yes/no): ", None, None, None)

            if printInput in ["no", "n"]:
                print_line(None, "ready_neg", None, None)
                _exit(0)

            elif printInput in ["yes", "y"]:
                print_line(None, "ready_pos", None, None)
                break

            else:
                print_line(None, "dont_know", None, None)
                
    choose_gamemode()


def invalid(target, num1, num2):
    print_line("Invalid input!\nYou can choose the " + target
                + " by typing any number between " + str(num1)
                + " and " + str(num2) + ".", None, None, None)

    if target == "gamemode":
        choose_gamemode()
    
    else:
        choose_category()


def choose_gamemode():
    global currentFunction
    currentFunction = _getframe().f_code.co_name

    try:
        global userGamemode
        userGamemode = int(print_line("Gamemodes:\n\n1. Default\n2. Random category\n\nWhich gamemode would you like to play? (1-2): ", None, None, None))
    
    except ValueError:
        invalid("gamemode", 1, 2)

    if userGamemode == 1:
        print_line(None, "default_mode", None, None)

        choose_category()
    
    elif userGamemode == 2:
        print_line(None, "random_mode", None, None)

        random_category()
    
    else:
        invalid("gamemode", 1, 2)


def choose_category():
    global currentFunction
    currentFunction = _getframe().f_code.co_name

    system("cls")
    for c in categories:
        print(str(categories.index(c) + 1) + ". " + c["name"])

    try:
        userCategoryNum = int(get_user_input("\nWhich category would like to play? (1-" + str(len(categories)) + "): "))

    except ValueError:
        invalid("category", 1, len(categories))

    global userCategory
    if userCategoryNum >= 1 and userCategoryNum <= len(categories):
        userCategory = categories[userCategoryNum - 1]

        print_line(None, "ready_pos", None, None)
        rules()
    
    else:
        invalid("category", 1, len(categories))


def random_category():
    global userCategory
    userCategory = choice(categories)

    rules()


def rules():
    global currentFunction
    currentFunction = _getframe().f_code.co_name

    if plData["playerData"]["skips"]["skipRules"] == False:
        userRules = print_line("So, do you know the rules of hangman? (yes/no): ", None, None, None)

        if userRules in ["yes", "y"]:
            print_line(None, "rules_pos", None, None)

            print_line("Here's your first word.", None, None, None)

        elif userRules in ["no", "n"]:
            print_line(None, "rules_neg", None, None)

            try:
                for line in chats["rules"]:
                    print_line(line, None, None, None)

            except KeyError:
                pass

        else:
            print_line(None, "dont_know", None, None)

            rules()

        plData["playerData"]["skips"]["skipRules"] = True
        writePlayerData(plData)
    
    play()


def play():
    global currentFunction
    currentFunction = _getframe().f_code.co_name
    guessedLetters = []
    guessedWords = []
    attempts = 5
    correct = False
    primaryDelay = 0.2
    secondaryDelay = 0.4
    word = choice(userCategory["words"])

    while correct == False and attempts > 0:
        current = ""

        for i, char in enumerate(word.lower(), 0):
            if char in guessedLetters or (char.isdigit() or char.isalpha() == False) :
                if char in guessedLetters:
                    if word[i].isupper():
                        current += char.upper()
                        continue

                current += char
            else:
                current += "_"

        if current == word:
            correct = True
        
        else:
            current = " ".join(current)

            guess = print_line(current + "\nYou have " + str(attempts) 
                                + " tries left.\nPlease enter your guess. It can be a character or a full word: "
                                , None, None, None)

            if len(guess) == 0:
                print_line(None, "blank_input", 6, secondaryDelay)

            elif len(guess) == 1:
                if guess in guessedLetters:
                    print_line(None, "guessed", 6, secondaryDelay)

                elif guess.isdigit() or guess.isalpha():
                    if guess not in word.lower():
                        plData["playerData"]["statistics"]["wrongGuesses"]["count"] += 1
                        guessedLetters.append(guess)
                        attempts -= 1

                        print_line(None, "incorrect", 4, primaryDelay)
                    
                    else:
                        plData["playerData"]["statistics"]["rightGuesses"]["count"] += 1
                        guessedLetters.append(guess)

                        print_line(None, "correct", "A", primaryDelay)

                    plData["playerData"]["statistics"]["guessesMade"]["count"] += 1
                    plData["playerData"]["statistics"]["charactersGuessed"]["count"] += 1
                    writePlayerData(plData)

                else:
                    print_line(None, "only_letters", 6, secondaryDelay)

            elif len(guess) == len(word):
                if guess in guessedWords:
                    print_line(None, "guessed", 6, secondaryDelay)

                else:
                    if guess == word.lower():
                        plData["playerData"]["statistics"]["rightGuesses"]["count"] += 1
                        correct = True

                        print_line(None, "correct", "A", primaryDelay)
                        
                    else:
                        plData["playerData"]["statistics"]["wrongGuesses"]["count"] += 1
                        guessedWords.append(guess)
                        attempts -= 1

                        print_line(None, "incorrect", 4, primaryDelay)
                
                    plData["playerData"]["statistics"]["guessesMade"]["count"] += 1
                    plData["playerData"]["statistics"]["wordsGuessed"]["count"] += 1
                    writePlayerData(plData)

            else:
                print_line(None, "wrong_amount", 6, secondaryDelay)
    else:
        if correct == True:
            plData["playerData"]["statistics"]["roundsWon"]["count"] += 1

            print_line(None, "won_game", None, None)
            print_line("The correct word was \"" + word + "\".", None, None, None)
        
        else:
            plData["playerData"]["statistics"]["roundsLost"]["count"] += 1

            print_line(None, "lost_game", None, None)
            print_line("The correct word would\'ve been \"" + word + "\".", None, None, None)

        plData["playerData"]["statistics"]["roundsPlayed"]["count"] += 1
        writePlayerData(plData)

        replay()


def replay():
    global currentFunction
    currentFunction = _getframe().f_code.co_name

    userReplay = print_line("Would you like to play again? (yes/no): ", None, None, None)

    if userReplay in ["yes", "y"]:
        print_line(None, "replay_pos", None, None)

        play()

    elif userReplay in ["no", "n"]:
        print_line(None, "replay_neg", None, None)

        _exit(0)

    else:
        print_line(None, "dont_know", None, None)

        replay()


prologue()