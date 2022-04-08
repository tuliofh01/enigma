#! python3
import curses
import pathlib, sys, time, os
import backEnd.backEnd

# Initializes the login window
def initialize():

    # Creates a window that covers all the screen
    window = curses.newwin(curses.LINES, curses.COLS)
    
    # Displays instructions
    instructions = "PLEASE TYPE IN YOUR LOGIN DATA"
    window.addstr(0, (curses.COLS // 2) - len(instructions) // 2,
        instructions, curses.A_BOLD)
    
    # Displays username message
    usernameLabel = "USERNAME:"
    window.addstr(curses.LINES // 4, (curses.COLS // 5),
        usernameLabel, curses.A_BOLD)
    
    # Displays password message
    passwordLabel = "PASSWORD:"
    window.addstr(curses.LINES // 3, (curses.COLS // 5),
        passwordLabel, curses.A_BOLD)

    # Moves the cursor to the correct position after writing to the screen
    window.move(curses.LINES // 4, (curses.COLS // 5) + len(usernameLabel))

    # Username input logic:
    username = ""; counter = 1
    lastKey = window.getch()
    while lastKey != ord('\n'):
        if lastKey in range(32,126):
            username = username + chr(lastKey)
            window.addstr(curses.LINES // 4, (curses.COLS // 5) 
                + len(usernameLabel) + counter, chr(lastKey))
            counter += 1
        elif counter == 1:
            pass
        else:
            username = username[:-1]; counter -= 1
            window.delch(curses.LINES // 4, (curses.COLS // 5) + len(usernameLabel) + counter)
        lastKey = window.getch()
    
    # Moves the cursor to the correct position after writing to the screen
    window.move(curses.LINES // 3, (curses.COLS // 5) + len(passwordLabel))
    
    # Password input logic:
    password = ""; counter = 1
    lastKey = window.getch()
    while lastKey != ord('\n'):
        if lastKey in range(32,126):
            password = password + chr(lastKey)
            window.addstr(curses.LINES // 3, (curses.COLS // 5) 
                + len(passwordLabel) + counter, chr(42))
            counter += 1
        elif counter == 1:
            pass
        else:
            password = password[:-1]; counter -= 1
            window.delch(curses.LINES // 3, (curses.COLS // 5) + len(passwordLabel) + counter)
        lastKey = window.getch()
    
    # Clears window for the loading text to be displayed
    window.clear()
    
    # Adds the ascii loading text to the window
    asciiArtPath = pathlib.Path("../resources/asciiLoadingArt.txt")
    with open(asciiArtPath, "r") as asciiArtFile:
        counter = -7
        for lineContent in asciiArtFile.readlines():
            window.addstr(((curses.LINES // 2) + counter),
                ((curses.COLS // 2) - len(lineContent) // 2), lineContent)
            counter += 1
    
    # Apply changes to the window
    window.refresh()
    
    # Validates user data
    beObject = backEnd.backEnd.EnigmaBE(username, password)
    
    # Enable the display of the loading text while login input is processed.
    time.sleep(5); 
    
    # Ignores keys pressed during the loading process
    curses.flushinp()
    
    # Returns beObject in case auth is successful
    if beObject.loginAuthentication():
        return beObject
    else:
        return False

