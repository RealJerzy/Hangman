# © HankiElama oy
# Beta Release v1.0.7

#Imports
from random import choice
import assets.chats as chats
import assets.words as words
import os
import ctypes

#Open in fullscreen everytime
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

fullscreen = 3
window = kernel32.GetConsoleWindow()

user32.ShowWindow(window, fullscreen)

#GAME -->
alphabet = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"
specials = "- "

chats.prologue()

def ready():
    os.system("cls")
    userReady = input("Are you down to play a game of hangman? (yes/no): ").lower()
    os.system("cls")

    if userReady == "no":
        print(choice(chats.reneg_chats))
        input()

        os._exit(0)

    elif userReady == "yes":
        print(choice(chats.repos_chats))
        input()

        choose_gamemode()

    else:
        print(choice(chats.dunno_chats))
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
    print("Gamemodes:", "", "1. Default gamemode", "2. Custom gamemode", "", sep="\n")

    try:
        userGamemode = int(input("Which gamemode would you like to play? (1-2): "))
        os.system("cls")
    
    except ValueError:
        invalid()

    if userGamemode == 1:
        print(choice(chats.defmd_chats))
        input()

        choose_category()
    
    elif userGamemode == 2:
        print(choice(chats.cusmd_chats))
        input()

        add_words()
    
    else:
        invalid()

def choose_category():
    def invalid():
        os.system("cls")
        print("Invalid input!",
            "You can choose the category by using the numbers 1-7 on your keyboard.", sep="\n")
        input()

        choose_category()

    global userCategory

    os.system("cls")
    print("1. Animals",
        "2. School subjects",
        "3. Kitchen",
        "4. Food",
        "5. Drinks",
        "6. Stuff",
        "7. Random",
        "", sep="\n")

    try:
        userCategory = int(input("Which category would like to play? (1-7): "))
        os.system("cls")

    except ValueError:
        invalid()

    if userCategory >= 1 and userCategory <= 7:
        userCategory -= 1

        print(choice(chats.repos_chats))
        input()

        rules()
    
    else:
        invalid()

def add_words():
    os.system("cls")

    try:
        i = int(input("How many words would you like to add? (atleast 10): "))
        os.system("cls")

    except ValueError:
        os.system("cls")
        print("Invalid input!", "Please use integers.", sep="\n")
        input()

        add_words()

    if i < 10:
        if i == 1:
            print("1 word is not enough.", "Please add atleast 10 words.", sep="\n")

        else:
            print(str(i) + " words is not enough.", "Please add atleast 10 words.", sep="\n")

        input()

        add_words()

    else:
        print("Ok, adding " + str(i) + " words.")
        input()

    newWord = ""
    while i > 0:
        os.system("cls")
        print("Please add a word now!")
        newWord = input("").lower()
        os.system('cls')

        if newWord not in words.custom:
            for char in newWord:
                if char not in alphabet and char not in specials and char not in numbers:
                    print('Invalid input!',
                        "You're allowed to use letters, numbers, hyphens and spaces!", sep='\n')
                    input()

                    add_words()

            if len(newWord) > 1:
                words.custom.append(newWord)
                i -= 1

                print("You have added " + str(len(words.custom)) + " words!")
                input()

            else:
                print("The word has to be atleast 2 characters long.")
                input()

        else:
            print("You have already added that word!")
            input()
    
    os.system("cls")
    print(choice(chats.repos_chats))
    input()

    rules()

def rules():
    os.system("cls")
    userRules = input("So, do you know the rules of hangman? (yes/no): ").lower()
    os.system("cls")

    if userRules == "yes":
        print(choice(chats.rupos_chats))
        input()

        os.system("cls")
        print("Here's your first word.")
        input()

        play()

    elif userRules == "no":
        print(choice(chats.runeg_chats))
        input()

        chats.rules()
        play()

    else:
        print(choice(chats.dunno_chats))
        input()

        rules()

def play():
    guessedLetters = []
    guessedWords = []
    attempts = 5
    correct = False
    word = words.getWord(userGamemode, userCategory)
        
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
                print(choice(chats.nothg_chats))
                input()

            elif len(guess) == 1:
                if guess in guessedLetters:
                    print(choice(chats.gessd_chats))
                    input()

                elif guess not in specials:
                    if guess not in alphabet and guess not in specials and guess not in numbers:
                        print(choice(chats.noalp_chats))
                        input()

                    elif guess not in word:
                        guessedLetters.append(guess)
                        attempts -= 1

                        print(choice(chats.wrong_chats))
                        input()
                    
                    else:
                        guessedLetters.append(guess)

                        print(choice(chats.right_chats))
                        input()

                else:
                    print(choice(chats.onlyl_chats))
                    input()

            elif len(guess) == len(word):
                if guess == word:
                    correct = True

                elif guess in guessedWords:
                    print(choice(chats.gessd_chats))
                    input()

                else:
                    guessedWords.append(guess)
                    attempts -= 1

                    print(choice(chats.wrong_chats))
                    input()

            else:
                print(choice(chats.amont_chats))
                input()
    else:
        os.system('cls')

        if correct == True:
            print(choice(chats.winnd_chats))
            input()

            again()
        
        else:
            print(choice(chats.loser_chats))
            input()

            again()

def again():
    os.system("cls")
    userAgain = input("Would you like to play again? (yes/no): ").lower()
    os.system("cls")

    if userAgain == "yes":
        print(choice(chats.agpos_chats))
        input()

        play()

    elif userAgain == "no":
        print(choice(chats.agneg_chats))
        input()

        os._exit(0)

    else:
        print(choice(chats.dunno_chats))
        input()

        again()
ready()