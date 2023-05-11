#! python3

import sqlite3, pathlib, string, base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from cryptography.fernet import Fernet, MultiFernet

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class EnigmaBE:

    def __init__(self, username, password):
        # Stores given login data.
        self.username = username
        self.password = password
        
        # Will be used to store user salt (none by default).
        self.salt = None; 
        
        # Will be used to store encrypted key
        self.key = None
        
        # Will be used to check wether user authentication was successfull (false by default).
        self.status = False
        
        # Holds Enigma's dababase path
        self.dataBasePath = pathlib.Path("../resources/vault.db")

    def loginAuthentication(self):
        # Reads data from the object
        username = self.username; password = self.password
        
        # Connects to database
        with sqlite3.connect(self.dataBasePath) as dataBase:
            SQLInputOutput = dataBase.cursor()
            
            # The code bellow will gather data for the username within the parameters.  
            usernameQuery = f"SELECT * FROM USERS WHERE USERNAME IS \"{username}\""
            SQLInputOutput.execute(usernameQuery); usernameResult = SQLInputOutput.fetchall()[0]
            
            # Here is where login authentication takes place. 
            if len(usernameResult) == 0:
                # Stops auth in case user does not exist.
                return False
            else:
                # Gathers user login data within the database
                self.salt = usernameResult[2]; encryptedPassword = usernameResult[3]
                
                # Will be used during the authentication process (PEPPER).
                pepperList = list(string.ascii_letters)
                
                # Checks for matching password
                for genericPepper in pepperList:
                    temp = (password + genericPepper).encode('ascii')
                    kdf = PBKDF2HMAC(hashes.SHA256(), 32, self.salt, 10**5)
                    self.key = kdf.derive(temp)
                    encryptor = AES.new(self.key, AES.MODE_ECB)
                    experimentalPassword = encryptor.encrypt(pad(temp, AES.block_size))
                    
                    # Runs in case passwords match
                    if experimentalPassword == encryptedPassword:
                        # Switches status value
                        self.status = True
                        
                        # Alters the password variable in order to decode text later on
                        self.password = temp
                        return True
            
            # Stops auth in case password is wrong.
            return False

    def decryptRecord(self, number): 
        # Checks login status
        if self.status == True:
            # Connects to database
            with sqlite3.connect(self.dataBasePath) as dataBase:
                SQLInputOutput = dataBase.cursor()
                
                # Query string
                recordQuery = f"SELECT * FROM RECORDS WHERE RECORD_ID IS \"{number}\""
                SQLInputOutput.execute(recordQuery); recordResult = SQLInputOutput.fetchall()
                
                # Decoder objects
                decoder1 = Fernet(base64.urlsafe_b64encode(self.key)); decoder2 = Fernet(recordResult[0][3])
                f = MultiFernet([decoder1, decoder2])
                
                # Will be used to store decrypted data
                temp = list()
                
                # Decrypts record (encrypted data)
                for info in recordResult[0][-2:]:
                        aux = f.decrypt(info)
                        temp.append(aux)
                return temp
        else:
            return False

    def addRecord(self, dscp, usr, pwd):
        # Checks login status
        if self.status == True:
            # Connects to database
            with sqlite3.connect(self.dataBasePath) as dataBase:
                SQLInputOutput = dataBase.cursor()

                # Select query string
                selectQueryString = f"SELECT * FROM RECORDS WHERE OWNER IS \"{self.username}\""
                
                # Executes and stores query
                SQLInputOutput.execute(selectQueryString); results = SQLInputOutput.fetchall()

                # Insert query string
                userRecordQuery = "INSERT INTO RECORDS (OWNER, DESCRIPTION, SALT, USERNAME, PASSWORD) VALUES (?,?,?,?,?)" 
                
                # Encoder objects/data
                salt = Fernet.generate_key()
                encoder1 = Fernet(base64.urlsafe_b64encode(self.key)); encoder2 = Fernet(salt); f = MultiFernet([encoder1,encoder2])
                
                # Record data
                owner = self.username; description = dscp; username = f.encrypt(usr.encode('ascii')); password = f.encrypt(pwd.encode('ascii'))
                SQLInputOutput.execute(userRecordQuery, (owner, description, salt, username, password)); dataBase.commit()
                
                # Returns opperation status
                return True
        else:
            return False

    def listRecords(self):
        # Checks login status
        if self.status == True:
            # Connects to database
            with sqlite3.connect(self.dataBasePath) as dataBase:
                SQLInputOutput = dataBase.cursor()
                
                # Insert query string
                userRecordQuery = f"SELECT * FROM RECORDS WHERE OWNER IS \"{self.username}\"" 
                SQLInputOutput.execute(userRecordQuery)
                
                # Returns records (public data)
                temp = list()
                for record in SQLInputOutput.fetchall():
                    temp.append(record[:3])
                return temp
        else:
            return False

    def deleteRecord(self, number):
        # Checks login status
        if self.status == True:
            # Connects to database
            with sqlite3.connect(self.dataBasePath) as dataBase:
                SQLInputOutput = dataBase.cursor()
                # Insert query string
                deleteRecordQuery = f"DELETE FROM RECORDS WHERE OWNER IS \"{self.username}\" AND RECORD_ID IS \"{number}\"" 
                
                # Execute query
                SQLInputOutput.execute(deleteRecordQuery); dataBase.commit()
                return True
        else:
            return False



