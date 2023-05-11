#! python3
import curses, pathlib, os

# Initializes the window
def initialize():
    # Creates a window that covers all the screen
    window = curses.newwin(curses.LINES, curses.COLS)

    # The following code fetches the enigma ascii art path
    asciiArtPath = pathlib.Path("../resources/asciiErrorArt.txt")

    # Displays error message
    greetingMessage = "ERROR: FAILED TO LOGIN"
    window.addstr(0, (curses.COLS // 2) - len(greetingMessage) // 2,
        greetingMessage, curses.A_BOLD)
    
    # Adds the ascii text logo to the window
    with open(asciiArtPath, "r") as asciiArtFile:
        counter = -7
        for lineContent in asciiArtFile.readlines():
            window.addstr(((curses.LINES // 2) + counter),
                ((curses.COLS // 2) - len(lineContent) // 2), lineContent)
            counter += 1
    
    # Displays instructions
    instructions = "PRESS ANY KEY TO CONTINUE..."
    window.addstr(curses.LINES - 1, (curses.COLS // 2) - len(instructions) // 2,
        instructions, curses.A_BOLD)

    # Waits for an user input
    window.getkey()




