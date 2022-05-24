__version__ = 'Pre-release b1.2.0'
__author__ = 'RealJerzy'

import random
import time
import msvcrt
import os
import json_managing as jsm
from json_managing import JsonManagement

os.system('title Hangman')
os.system('color 7')
jsm = JsonManagement()
CURRENT_FUNCTION = ''

def print_statistics():
    out = 'Statistics:\n\n'
    min_length = 0
    for k, value in jsm.player_data['statistics'].items():
        if len(value['id']) > min_length:
            min_length = len(value['id'])
    for i in jsm.player_data['statistics']:
        current_stat = jsm.player_data['statistics'][i]['id']
        out += (
            current_stat
            + ': '
            + (min_length - len(current_stat)) * ' '
            + str(jsm.player_data['statistics'][i]['count'])
            + '\n'
        )
    print_line(out, None, None, None)


def reset(target):
    while True:
        if target == 'Statistics':
            user_reset = print_line(
                'You are about to reset '
                + target
                + '!\nThis action cannot be reverted!\nAre you sure?',
                None,
                4,
                0.2,
            )
            if user_reset in ['yes', 'y']:
                for stat in jsm.player_data['statistics']:
                    jsm.player_data['statistics'][stat]['count'] = 0
            elif user_reset in ['no', 'n']:
                print_line('The reset has been cancelled.', None, None, None)
                break
            else:
                print_line(
                    'It\'s a freaking yes/no question! Lights on dummy fricky.',
                    None,
                    None,
                    None,
                )
                continue
        else:
            jsm.player_data['skips'] = {
                skip: False for skip in jsm.player_data['skips']
            }
        jsm.write_json(jsm.player_data)
        print_line(str(target) + ' have been reset succesfully. ', None, None, None)
        break


def get_user_input(text):
    user_input = input(text).lower()
    if user_input == 'skip':
        jsm.player_data['skips']['skipIntro'] = True
        jsm.write_json(jsm.player_data)
        if CURRENT_FUNCTION == 'prologue':
            rules()
    elif user_input == 'stats':
        print_statistics()
    elif user_input == 'reset stats':
        reset('Statistics')
    elif user_input == 'reset skips':
        reset('Skips')
    elif user_input == 'quit':
        exit()
    elif user_input == 'help':
        print_line(
            'Write \'skip\' to skip and never see intro again.\n'
            + 'Write \'statistics\' to read your game statistics\n'
            + 'Write \'quit\' anytime to quit.',
            None,
            None,
            None,
        )
    return user_input


def print_line(text, random_category, color, delay):
    if text is not None:
        while True:
            os.system('cls')
            print(text)
            if color is not None:
                while True:
                    os.system('color 7')
                    time.sleep(delay)
                    os.system('color ' + str(color))
                    time.sleep(delay)
                    if msvcrt.kbhit():
                        os.system('color 7')
                        break
            return get_user_input('')
    elif random_category is not None:
        try:
            print_line(
                random.choice(jsm.chats[random_category]),
                None,
                color,
                delay
            )
        except (KeyError, IndexError):
            pass


def invalid(target, num1, num2):
    print_line(
        'Invalid input!\nYou can choose the '
        + target
        + ' by typing any number between '
        + str(num1)
        + ' and '
        + str(num2)
        + '.',
        None,
        None,
        None,
    )
    if target == 'gamemode':
        choose_gamemode()
    else:
        choose_category()


def prologue():
    global CURRENT_FUNCTION
    CURRENT_FUNCTION = 'prologue'
    if jsm.player_data['skips']['skipIntro'] is False:
        try:
            for line in jsm.chats['prologue']:
                print_line(line, None, None, None)
        except KeyError:
            pass
        while True:
            print_input = print_line(
                'Are you down to play a game of hangman? (yes/no): ',
                None,
                None,
                None
            )
            if print_input in ['no', 'n']:
                print_line(None, 'ready_neg', None, None)
                exit()
            elif print_input in ['yes', 'y']:
                print_line(None, 'ready_pos', None, None)
                break
            else:
                print_line(None, 'dont_know', None, None)
    rules()


def rules():
    if jsm.player_data['skips']['skipRules'] is False:
        user_rules = print_line(
            'So, do you know the rules of hangman? (yes/no): ',
            None,
            None,
            None
        )
        if user_rules in ['yes', 'y']:
            print_line(None, 'rules_pos', None, None)
            jsm.player_data['skips']['skipRules'] = True
            jsm.write_json(jsm.player_data)
        elif user_rules in ['no', 'n']:
            print_line(None, 'rules_neg', None, None)
            try:
                for line in jsm.chats['rules']:
                    print_line(line, None, None, None)
            except KeyError:
                pass
        else:
            print_line(None, 'dont_know', None, None)
            rules()
    choose_gamemode()


def choose_gamemode():
    global CURRENT_FUNCTION
    CURRENT_FUNCTION = 'choose_gamemode'
    try:
        user_gamemode = int(
            print_line(
                'Gamemodes:\n\n1. Default\n'
                + '2. Random category\n\n'
                + 'Which gamemode would you like to play? (1-2): ',
                None,
                None,
                None,
            )
        )
    except ValueError:
        invalid('gamemode', 1, 2)
    if user_gamemode == 1:
        print_line(None, 'default_mode', None, None)
        choose_category()
    elif user_gamemode == 2:
        print_line(None, 'random_mode', None, None)
        user_gamemode = random.choice(jsm.categories)
    else:
        invalid('gamemode', 1, 2)


def choose_category():
    os.system('cls')
    for category in jsm.categories:
        print(
            str(jsm.categories.index(category) + 1)
            + '. '
            + category['name']
        )
    try:
        user_category_num = int(
            print_line(
                (
                    '\nWhich category would like to play? (1-'
                    + str(len(jsm.categories))
                    + '): '
                ),
                None,
                None,
                None,
            )
        )
    except ValueError:
        invalid('category', 1, len(jsm.categories))
    if user_category_num < 1 or user_category_num > len(jsm.categories):
        invalid('category', 1, len(jsm.categories))
    user_category = jsm.categories[user_category_num - 1]
    print_line(None, 'ready_pos', None, None)
    print_line('Here\'s your first word.', None, None, None)
    play(user_category)


def play(user_gamemode):
    guessed_letters = []
    guessed_words = []
    attempts = 5
    correct = False
    primary_delay = 0.2
    secondary_delay = 0.4
    word = random.choice(user_gamemode['words'])
    while correct is False and attempts > 0:
        current = ''
        for i, char in enumerate(word.lower(), 0):
            if char in guessed_letters or (char.isdigit() or not char.isalpha()):
                if char in guessed_letters and word[i].isupper():
                    current += char.upper()
                    continue
                current += char
            else:
                current += '_'
        if current == word:
            correct = True
        else:
            current = ' '.join(current)
            guess = print_line(
                current
                + '\nYou have '
                + str(attempts)
                + ' tries left.\nPlease enter your guess. It can be a character or a full word: ',
                None,
                None,
                None,
            )
            if not guess:
                print_line(None, 'blank_input', 6, secondary_delay)
            elif len(guess) == 1:
                if guess in guessed_letters:
                    print_line(None, 'guessed', 6, secondary_delay)
                elif guess.isdigit() or guess.isalpha():
                    if guess not in word.lower():
                        jsm.player_data['statistics']['wrongGuesses']['count'] += 1
                        guessed_letters.append(guess)
                        attempts -= 1
                        print_line(None, 'incorrect', 4, primary_delay)
                    else:
                        jsm.player_data['statistics']['rightGuesses']['count'] += 1
                        guessed_letters.append(guess)
                        print_line(None, 'correct', 'A', primary_delay)
                    jsm.player_data['statistics']['guessesMade']['count'] += 1
                    jsm.player_data['statistics']['charactersGuessed']['count'] += 1
                    jsm.write_json(jsm.player_data)
                else:
                    print_line(None, 'only_letters', 6, secondary_delay)
            elif len(guess) == len(word):
                if guess in guessed_words:
                    print_line(None, 'guessed', 6, secondary_delay)
                else:
                    if guess == word.lower():
                        jsm.player_data['statistics']['rightGuesses']['count'] += 1
                        correct = True
                        print_line(None, 'correct', 'A', primary_delay)
                    else:
                        jsm.player_data['statistics']['wrongGuesses']['count'] += 1
                        guessed_words.append(guess)
                        attempts -= 1
                        print_line(None, 'incorrect', 4, primary_delay)
                    jsm.player_data['statistics']['guessesMade']['count'] += 1
                    jsm.player_data['statistics']['wordsGuessed']['count'] += 1
                    jsm.write_json(jsm.player_data)
            else:
                print_line(None, 'wrong_amount', 6, secondary_delay)
    if correct is True:
        jsm.player_data['statistics']['roundsWon']['count'] += 1
        print_line(None, 'won_game', None, None)
        print_line('The correct word was \''
                   + word
                   + '\'.',
                   None,
                   None,
                   None
                   )
    else:
        jsm.player_data['statistics']['roundsLost']['count'] += 1
        print_line(None, 'lost_game', None, None)
        print_line(
            'The correct word would\'ve been \''
            + word
            + '\'.',
            None,
            None,
            None
        )
    jsm.player_data['statistics']['roundsPlayed']['count'] += 1
    jsm.write_json(jsm.player_data)
    replay(user_gamemode)


def replay(user_gamemode):
    user_replay = print_line(
        'Would you like to play again? (yes/no): ',
        None,
        None,
        None
    )
    if user_replay in ['yes', 'y']:
        print_line(None, 'replay_pos', None, None)
        play(user_gamemode)
    elif user_replay in ['no', 'n']:
        print_line(None, 'replay_neg', None, None)
        exit()
    else:
        print_line(None, 'dont_know', None, None)
        replay(user_gamemode)


if __name__ == '__main__':
    prologue()
