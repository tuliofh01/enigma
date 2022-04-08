#! python3

import curses

import frontEnd.windows.welcomeWindow
import frontEnd.windows.loginWindow
import frontEnd.windows.recordsWindow
import frontEnd.windows.errorWindow
import frontEnd.windows.recordsWindow

# This function will call all methods within the windows folder.
# Eventual backend function calls will be made directly from each individual window.
def parentWindow(stdScreen):
    # Clears the screen's previous content
    stdScreen.clear()

    # Launches the greetings window
    frontEnd.windows.welcomeWindow.initialize()

    # Launches the loging screen and stores beObject
    login = frontEnd.windows.loginWindow.initialize()
    if login:
        # launches menu
        frontEnd.windows.recordsWindow.initialize(login)
    else:
        # Launches error screen (failed to login)
        frontEnd.windows.errorWindow.initialize()
    
def initialize():
    # The wrapper function automatically initializes the stdScreen object.
    curses.wrapper(parentWindow)


