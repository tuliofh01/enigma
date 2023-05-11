#! python3

'''
This script must be triggered during the installation process 
(from the backEnd folder).
Basically, it will create a database in case it doesn't exist.
Otherwise, it will add users to the database. 
'''

import sqlite3, pathlib, os, random, string, base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

dataBasePath = "../../resources/vault.db"

# Creates a new database file in case it doesn't exist.
if os.path.isfile(dataBasePath) == False:
    with sqlite3.connect(dataBasePath) as dataBase:
        SQLInputOutput = dataBase.cursor()

        # Creates TABLES within the database
        usersQuery = "CREATE TABLE USERS (USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                USERNAME TEXT, SALT BLOB, PASSWORD BLOB)"
        recordsQuery = "CREATE TABLE RECORDS (RECORD_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
                OWNER TEXT, DESCRIPTION TEXT, SALT BLOB, USERNAME TEXT, PASSWORD BLOB)"
        SQLInputOutput.execute(usersQuery)
        SQLInputOutput.execute(recordsQuery)
        
        # Correctly initializes the record variables.
        print("Warning: Please use only ASCII characters.")
        usernameInput = None; passwordInput = None
        while True:
            try:
                usernameInput = input("Type in a username:"); passwordInput = input("Type in a password:")
                usernameInput.encode('ascii'); passwordInput.encode('ascii')
                break
            except:
                print("Error: Try again; non ascii character detected!")
        salt = os.urandom(16); pepper = random.choice(list(string.ascii_letters))
        username = usernameInput; password = (passwordInput + pepper).encode('ascii')
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 10**5)
        key = kdf.derive(password)
        
        # Encrypts password
        encryptor = AES.new(key, AES.MODE_ECB)
        encryptedPassword = encryptor.encrypt(pad(password, AES.block_size))

        # Adds a record to the USERS TABLE.
        userRecordQuery = "INSERT INTO USERS (USERNAME, SALT, PASSWORD) VALUES (?,?,?)" 
        SQLInputOutput.execute(userRecordQuery, (username, salt, encryptedPassword))

        # Saves changes to the db
        dataBase.commit()

# Adds users to existing database.
else:
    with sqlite3.connect(dataBasePath) as dataBase:
        SQLInputOutput = dataBase.cursor()
        
        # Correctly initializes the record variables.
        print("Warning: Please use only ASCII characters.")
        usernameInput = None; passwordInput = None
        while True:
            try:
                usernameInput = input("Type in a username:"); passwordInput = input("Type in a password:")
                usernameInput.encode('ascii'); passwordInput.encode('ascii')
                break
            except:
                print("Error: Try again; non ascii character detected!")
        salt = os.urandom(16); pepper = random.choice(list(string.ascii_letters))
        username = usernameInput; password = (passwordInput + pepper).encode('ascii')
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 10**5)
        key = kdf.derive(password)
        
        # Encrypts password
        encryptor = AES.new(key, AES.MODE_ECB)
        encryptedPassword = encryptor.encrypt(pad(password, AES.block_size))
        
        # Adds a record to the USERS TABLE.
        userRecordQuery = "INSERT INTO USERS (USERNAME, SALT, PASSWORD) VALUES (?,?,?)" 
        SQLInputOutput.execute(userRecordQuery, (username, salt, encryptedPassword))

        # Saves changes to the db
        dataBase.commit()
