# © JerzyEntertainmentCompany oy
# Early access

import assets.chats as chats
import assets.words as words
import random
import os

alph = "abcdefghijklmnopqrstuvwxyz"
spec = "- "
nums = "1234567890"

def prologue():
    chats.prologue()

    ready()

def ready():
    os.system("cls")
    user_ready = (input("Are you down to play a game of hangman? (yes/no): ").lower())

    if user_ready == "no":
        os.system("cls")
        print(random.choice(chats.reneg_chats))
        input()

        exit()

    elif user_ready == "yes":
        os.system("cls")
        print(random.choice(chats.repos_chats))
        input()

        choose_gamemode()

    else:
        os.system("cls")
        print(random.choice(chats.dunno_chats))
        input()

        ready()

def choose_gamemode():
    while True:
        os.system("cls")
        print("Gamemodes:", "", "1. Default gamemode", "2. Custom gamemode", "", sep="\n")
        global user_gamemode
        user_gamemode = input("Which gamemode would you like to play?: ")

        if user_gamemode == "1" or user_gamemode == "2":
            user_gamemode = int(user_gamemode)
            break
        else:
            os.system("cls")
            print("Invalid input!", "You can choose gamemode by typing 1 or 2.", sep="\n")
            input()
            continue

    if user_gamemode == 1:
        os.system("cls")
        print(random.choice(chats.defmd_chats))
        input()

        choose_category()

    elif user_gamemode == 2:
        os.system("cls")
        print(random.choice(chats.cusmd_chats))
        input()

        add_words()

def choose_category():
    while True:
        os.system("cls")
        print("1. Animals", "2. School subjects", "3. Kitchen", "4. Food", "5. Drinks", "6. Stuff", "7. Random", "", sep="\n")
        global user_category
        user_category = input("Which category would like to play?: ")

        if user_category == '1' or user_category == '2' or user_category == '3' or user_category == '4' or user_category == '5' or user_category == '6' or user_category == '7':
            user_category = int(user_category) - 1
            os.system("cls")
            print(random.choice(chats.repos_chats))
            input()

            break
        else:
            os.system("cls")
            print("Invalid input!", "You can choose the category by using the numbers 1-7 on your keyboard.", sep="\n")
    rules()

def add_words():
    os.system("cls")
    i = int(input("How many words would you like to add? (atleast 10): "))
    
    for letter in str(i):
        if letter not in nums:
            os.system("cls")
            print("Invalid input!", "Please use integers.", sep="\n")
            input()

            add_words()

    if i < 10:
        os.system("cls")
        print(str(i) + "words is not enough.", "Please add atleast 10 words.", sep="\n")
        input()

        add_words()

    else:
        os.system("cls")
        print("Ok, adding " + str(i) + " words.")
        input()

    new_word = ""

    while i > 0:
        os.system("cls")
        print("Please add a word now!")
        new_word = input("").lower()

        if new_word not in words.custom:
            if len(new_word) > 1:
                words.custom.append(new_word)
                i -= 1

                os.system("cls")
                print("You have added " + (str(len(words.custom))) + " words!")
                input()

            else:
                os.system("cls")
                print("The length of the word has to be atleast 2 characters")
                input()

        else:
            os.system("cls")
            print("You have already added that word!")
            input()
    
    os.system("cls")
    print(random.choice(chats.repos_chats))
    input()

    rules()

def rules():
    os.system("cls")
    user_rules = input("So, do you know the rules of hangman?: ").lower()

    if user_rules == "yes":
        os.system("cls")
        print(random.choice(chats.rupos_chats))
        input()
        os.system("cls")
        print("Here's your first word.")
        input()

        play()

    elif user_rules == "no":
        chats.rules()
        play()

    else:
        os.system("cls")
        print(random.choice(chats.dunno_chats))
        input()

        rules()

def play():
    guessedlet = []
    guessedwor = []
    begin = ""
    attempts = 5
    correct = False

    if user_gamemode == 1:
        if user_category == 6:
            word = words.random

        else:
            word = random.choice(words.categories[user_category])

    elif user_gamemode == 2:
        word = words.custom_words()

    for letter in word:
        if letter in alph or letter in spec or letter in nums:
            if letter == " ":
                begin += "* "
            elif letter == "-":
                begin += "- "
            else:
                begin += "_ "
        else:
            play()

    os.system("cls")
    print(begin)
    
    while correct == False and attempts > 0:
        print("You have " + str(attempts) + " tries left.")
        guess = input("Please enter your guess. It can be a letter or the full word. ")

        if len(guess) == 0:
            os.system("cls")
            print(random.choice(chats.nothg_chats))
            input()

        elif len(guess) == 1:
            if guess not in alph and guess not in spec and guess not in nums:
                os.system("cls")
                print(random.choice(chats.noalp_chats))
                input()

            elif guess in guessedlet:
                os.system("cls")
                print(random.choice(chats.gessd_chats))
                input()

            elif guess not in word and guess not in spec:
                guessedlet.append(guess)
                attempts -= 1
                os.system("cls")
                print(random.choice(chats.wrong_chats))
                input()

            elif guess in word and guess not in spec:
                guessedlet.append(guess)
                os.system("cls")
                print(random.choice(chats.right_chats))
                input()
    
            elif guess == " ":
                os.system("cls")
                print(random.choice(chats.onlyl_chats))
                input()

            elif guess == "-":
                os.system("cls")
                print(random.choice(chats.onlyl_chats))
                input()

            else:
                os.system("cls")
                print(random.choice(chats.dunno_chats))
                input()

        elif len(guess) == len(word):
            if guess == word:
                correct = True
                os.system("cls")
                print(random.choice(chats.winnd_chats))
                input()

                again()

            elif guess in guessedwor:
                os.system("cls")
                print(random.choice(chats.gessd_chats))
                input()

            else:
                guessedwor.append(guess)
                attempts -= 1
                os.system("cls")
                print(random.choice(chats.wrong_chats))
                input()

        else:
            os.system("cls")
            print(random.choice(chats.amont_chats))
            input()

        curr = ""
        this = ""

        for letter in word:
            if letter == " ":
                curr += letter
                this += "* "

            elif letter == "-":
                curr += letter
                this += "- "

            elif letter in guessedlet:
                curr += letter
                this += letter + " "

            else:
                this += "_ "

        os.system("cls")
        print(this)
        input()

        if curr == word:
            correct == True
            os.system("cls")
            print(random.choice(chats.winnd_chats))
            input()

            again()
        
        elif attempts == 0:
            os.system("cls")
            print(random.choice(chats.loser_chats))
            input()

            again()

def again():
    os.system("cls")
    againA = input("Would you like to play again?").lower()

    if againA == "yes":
        os.system("cls")
        print(random.choice(chats.agpos_chats))
        input()

        play()

    elif againA == "no":
        os.system("cls")
        print(random.choice(chats.agneg_chats))
        input()

        exit()

    else:
        print(random.choice(chats.dunno_chats))
        input()

        again()
prologue()