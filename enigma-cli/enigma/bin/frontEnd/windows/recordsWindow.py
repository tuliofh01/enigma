#! python3
import curses, sys, time

def initialize(beObject):
    # Initializes color pairs
    curses.init_pair(1, curses.COLOR_WHITE, 234); curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_GREEN, 234); curses.init_pair(4, curses.COLOR_RED, 234)
    
    # Creates a window that covers half of the screen (info display for records)
    infoDisplay = curses.newwin(curses.LINES, curses.COLS//2, 0, curses.COLS//2)

    # Changes info display background (for differentiation purposes)
    infoDisplay.bkgd(curses.color_pair(1))
    infoDisplay.refresh()
    
    # Creates a window that covers half of the screen (selector menu for records)
    selectorMenu = curses.newwin(curses.LINES, curses.COLS//2)

    def inputCurses(window, targetVar, text, x, y):
        window.move(y, x + len(text))
        targetVar = ""; counter = 1
        lastKey = window.getch()
        while lastKey != ord('\n'):
            if lastKey in range(32,126):
                targetVar = targetVar + chr(lastKey)
                window.addstr(y, x + len(text) + counter, chr(lastKey))
                counter += 1
            elif lastKey not in range(0,128):
                return False
            elif counter == 1:
                pass
            else:
                targetVar = targetVar[:-1]; counter -= 1
                window.delch(y, x + len(text) + counter)
            window.refresh()
            lastKey = window.getch()
        return targetVar

    # Draws selector menu for a given page (sub-set of records) and highlights selected item.
    def drawSelectorMenu(currentPage = 1, selectedItem = 1):
        # Splits the record list into sub-sets according to the page number
        global completeRecordList, slicedRecordList
        completeRecordList = beObject.listRecords()
        slicedRecordList = completeRecordList[5 * (currentPage - 1): 5 * currentPage]
        
        # Clears previous content
        selectorMenu.clear()

        # Hides cursor
        curses.curs_set(0)
        
        # Header text -> header must be present regardless of the page (default element).        
        infoText1 = "PRESS ENTER TO SELECT A RECORD."; infoText2 = "PRESS U TO GO UP AND D TO GO DOWN."
        selectorMenu.addstr(0,(curses.COLS//4) - len(infoText1)//2, infoText1, curses.A_BOLD)
        selectorMenu.addstr(1,(curses.COLS//4) - len(infoText2)//2, infoText2, curses.A_BOLD)
        for cell in range(curses.COLS//2):
            selectorMenu.addstr(2,cell,'_')

        # Adds create new record entry (default element) to the record list. 
        slicedRecordList.insert(0, [-1, beObject.username, "SELECT ME TO CREATE A NEW RECORD"])

        # Adds save and exit (default element) to the record list.
        slicedRecordList.append([-2, beObject.username, "EXIT"])

        # Creates menu entries
        counter = 5
        for record in slicedRecordList:
            counter += 2
            if slicedRecordList.index(record) == selectedItem - 1:
                selectorMenu.attron(curses.color_pair(2))
                selectorMenu.addstr(counter,(curses.COLS//4) - len(record[2])//2, record[2])
                selectorMenu.attroff(curses.color_pair(2))
            else:
                selectorMenu.addstr(counter,(curses.COLS//4) - len(record[2])//2, record[2])

        # Prints menu to the screen.
        selectorMenu.refresh()
    
    def drawInfoDisplay_RecordDecryption(page, item):
        # Calculates the actual record index
        index = (((item - 1) + (5 * (page - 1))) - 1) 
        
        # Decrypts and stores record
        recordData = beObject.decryptRecord(completeRecordList[index][0])

        # Clear previous entries
        infoDisplay.clear()

        # Adds the results to the screen
        infoDisplay.addstr(5, 5, "USERNAME:", curses.A_BOLD)
        infoDisplay.addstr(5, 5 + len("USERNAME:"), recordData[0])
        infoDisplay.addstr(10, 5, "PASSWORD:", curses.A_BOLD)
        infoDisplay.addstr(10, 5 + len("PASSWORD:"), recordData[1])

        # Adds control options to the screen
        infoDisplay.addstr((curses.LINES - 1), ((curses.COLS // 4) - \
            (len("PRESS E TWICE TO ERASE RECORD OR OTHER KEY TO RETURN")//2)), "PRESS TWICE E TO ERASE RECORD OR OTHER KEY TO RETURN", curses.A_BOLD)

        # Updates the screen
        infoDisplay.refresh()

        lastKey = infoDisplay.getch()
        if lastKey in (ord('e'), ord('E')):
            infoDisplay.addstr((curses.LINES - 1), ((curses.COLS // 4) - \
                (len("PRESS E TWICE TO ERASE RECORD OR OTHER KEY TO RETURN")//2)),\
                    "PRESS TWICE E TO ERASE RECORD OR OTHER KEY TO RETURN", curses.A_BOLD | curses.color_pair(4))
            infoDisplay.refresh()
            time.sleep(2)
            if lastKey in (ord('e'), ord('E')):
                beObject.deleteRecord(completeRecordList[index][0])
        else:
            pass

    def drawInfoDisplay_RecordCreation():
        # Enables cursor to be displayed
        curses.curs_set(1)
        
        # Clears previous entries
        infoDisplay.clear()
        
        # Adds default strings to the screen
        infoDisplay.addstr(5, 5, "DESCRIPTION:", curses.A_BOLD)
        infoDisplay.addstr(10, 5, "USERNAME:", curses.A_BOLD)
        infoDisplay.addstr(15, 5, "PASSWORD:", curses.A_BOLD)

        # Updates the cursor
        infoDisplay.refresh()

        # Record variables creation
        description = None; username = None; password = None

        # Record variables assignment
        description = inputCurses(infoDisplay, description, "DESCRIPTION:", 5, 5)        
        username = inputCurses(infoDisplay, username, "USERNAME:", 5, 10)
        password = inputCurses(infoDisplay, password, "PASSWORD:", 5, 15)

        # Hides cursor once again
        curses.curs_set(0)

        # Clears screen
        infoDisplay.clear()

        # Displays loading text
        infoDisplay.addstr(5, ( (curses.COLS // 4)) - (len("LOADING...") // 2),\
            "LOADING...", curses.A_BOLD | curses.A_BLINK)

        # Updates the screen
        infoDisplay.refresh(); time.sleep(5)

        # Submits data to backend function
        if description != False and username != False and password != False: 
            # Creates record
            beObject.addRecord(description, username, password)
            
            # Clears screen
            infoDisplay.clear()

            # Displays record creation final status
            infoDisplay.addstr(5, ( (curses.COLS // 4)) - (len("RECORD SUCCESSFULLY CREATED") // 2),\
                "RECORD SUCCESSFULLY CREATED", curses.A_BOLD | curses.color_pair(3))
        else:
            # Clears screen
            infoDisplay.clear()
            # Displays record creation final status
            infoDisplay.addstr(5, ( (curses.COLS // 4)) - (len("ERROR: UNABLE TO CREATE RECORD") // 2),\
                "ERROR: UNABLE TO CREATE RECORD", curses.A_BOLD | curses.color_pair(4))
            
        # Updates the screen
        infoDisplay.refresh()

    # Draws selectorMenu (first instance)
    drawSelectorMenu(1, 1)

    # Updates selector menu/info display according to keyboard inputs.
    page = 1; item = 1
    while True:
        # Gets user input
        lastKey = selectorMenu.getch()
        
        # Clears previous content
        infoDisplay.clear()

        # Updates the screen
        infoDisplay.refresh()

        # Visual part (frontend related).
        if lastKey in (ord('d'), ord('D')) and (item != len(slicedRecordList)):
            item += 1
        elif lastKey in (ord('d'), ord('D')) and (item == len(slicedRecordList)):
            if ((page * 5)-1) > len(completeRecordList):
                page = 1; item = 1
            else:
                item = 1; page += 1
        elif lastKey in (ord('u'),ord('U')) and item == 1 and page != 1:
            item = 1; page -= 1
        elif lastKey in (ord('u'),ord('U')) and item == 1 and page == 1:
            pass
        elif lastKey in (ord('u'),ord('U')) and item != 1:
            item -= 1
        
        # Functional part (backend related).
        elif lastKey == ord('\n') and item == len(slicedRecordList):
            # Triggers exit (default record)
            sys.exit(0)
        elif lastKey == ord('\n') and item == 1:
            # Triggers record creation
            drawInfoDisplay_RecordCreation()
        elif lastKey == ord('\n'):
            # Triggers record decryption
            drawInfoDisplay_RecordDecryption(page, item)

        # Draws selectorMenu (subsequent instances).
        drawSelectorMenu(page, item)
