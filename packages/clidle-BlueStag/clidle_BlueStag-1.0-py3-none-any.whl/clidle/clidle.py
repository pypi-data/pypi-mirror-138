import curses
import requests
from random import choice

WORD_LENGTH = 5
ATTEMPTS = 6
WORDS_SOURCE = "https://www.mit.edu/~ecprice/wordlist.10000"
NAMES_SOURCE = "https://www.usna.edu/Users/cs/roche/courses/s15si335/proj1/files.php%3Ff=names.txt&downloadcode=yes"


def clidle_main(stdscr: curses.window):
    # Get words from online
    words_response: requests.Response = requests.get(WORDS_SOURCE)
    if words_response.status_code != 200:  # Status code is not ok
        stdscr.addstr(f"Error code {words_response.status_code} when loading "
                      f"word list.\nPress a key to exit.",
                      curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    # Get names from online
    names_response: requests.Response = requests.get(NAMES_SOURCE)
    if names_response.status_code != 200:  # Status code is not ok
        stdscr.addstr(f"Error code {names_response.status_code} when loading "
                      f"name list.\nPress a key to exit.",
                      curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()
        return

    # Patience
    stdscr.addstr(0, 0, "Loading...")
    stdscr.move(0, 0)
    stdscr.refresh()

    # Get words
    words = words_response.content.decode().lower().splitlines()
    # Filter out words that do not match word length
    words = filter(lambda word: len(word) == WORD_LENGTH, words)
    # Get names
    names = names_response.content.decode().lower().splitlines()
    # Filter out names
    words = filter(lambda word: word not in names, words)
    # Convert words to list
    words = list(words)
    # Get random word
    correct_word = choice(words)

    # Setup game variables
    attempts = 0
    success = False
    chars = 0
    word = ""
    incorrect_chars = ""

    # Init color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK,
                     curses.COLOR_GREEN)  # Correct letter
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Wrong place

    # No more patience
    stdscr.addstr(0, 0, " " * 10)
    stdscr.move(0, 0)

    # Game loop
    while attempts < ATTEMPTS:
        # Draw word
        stdscr.addstr(attempts, 0, " " * WORD_LENGTH)
        stdscr.addstr(attempts, 0, word)

        # Draw incorrect letters
        stdscr.addstr(0, WORD_LENGTH + 1, "Incorrect:", curses.A_UNDERLINE)
        for i in range(len(incorrect_chars)):
            stdscr.addch(1 + i // 6,
                         i % 6 * 2 + WORD_LENGTH + 2,
                         incorrect_chars[i], curses.A_ITALIC)

        # Refresh
        stdscr.move(attempts, chars)
        stdscr.refresh()

        key = stdscr.getch()
        # Submit word
        if key in [curses.KEY_ENTER, ord("\n")] and chars == WORD_LENGTH:
            # Correction
            correct = 0
            for i in range(len(word)):
                if word[i] == correct_word[i]:
                    correct += 1
                    char_attr = curses.color_pair(1)  # Correct letter
                elif word[i] in correct_word:
                    char_attr = curses.color_pair(2)  # Wrong place
                else:
                    char_attr = curses.A_DIM  # Non-existant
                    if word[i] not in incorrect_chars:
                        incorrect_chars += word[i]  # Add incorrect character
                stdscr.addch(attempts, i, word[i], char_attr)
            stdscr.refresh()

            # Win screen
            if correct == WORD_LENGTH:
                stdscr.addstr(attempts + 2, 0, "CORRECT!", curses.A_BOLD)
                stdscr.refresh()
                stdscr.getch()
                break

            # Fail screen
            if attempts + 1 == ATTEMPTS:
                stdscr.addstr(attempts + 2, 0, "FAILED!", curses.A_BOLD)
                stdscr.addstr(attempts + 3, 0, "The correct word was:")
                stdscr.addstr(attempts + 4, 0, correct_word,
                              curses.color_pair(1))
                stdscr.refresh()
                stdscr.getch()
                break

            attempts += 1
            chars = 0
            word = ""
            continue
        # Backspace
        elif key in [curses.KEY_BACKSPACE, ord("\b")] and chars > 0:
            chars -= 1
            word = word[0:len(word)-1]
        # Add letter
        elif key >= ord("a") and key <= ord("z")\
                and chars < WORD_LENGTH\
                and chr(key) not in incorrect_chars:
            chars += 1
            word += chr(key)
