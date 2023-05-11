
# Enigma
### *Last updated on - (05/05/2022)*
---

## Summary:
- Enigma is a simple terminal based password manager coded in SQLite 3 and Python 3.
- Its interface was built with the Python version of the nCurses graphical module, so as to provide a smoother user experience.
- All the code is free to use and any improvements are welcome!
---

## Cryptography:
- Enigma makes use of Fernet, PBKDF2HMAC, and AES encryption in order to protect its records.
---

## Important information:
- The program does not support UTF-8 **yet**, due to an issue on the inputs logic.
- The code has, **until now**, only been tested on Linux based operating systems (specifically Arch derivatives).
- You **must** run the setup.sh file before launching Engima (*~/enigma/bin/main.py*), otherwise the app won't work.
- Launch Engima through the launcher.sh file.
- Make sure to chmod both .sh files and to install all required python modules (check source code).
---

## TODO:
- Treat unknown user exception (login screen).
---

## Credits:
- Enigma was both created and is being maintained by **Túlio Horta**.
