const {app, BrowserWindow, Menu, ipcMain} = require("electron");
const path = require("path");

let mainWindow;

function createWindow() {
  // Create the browser window.
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: { nodeIntegration: true, contextIsolation: false },
    resizable: false,
    title: "Enigma-JS",
  });
  Menu.setApplicationMenu(null);
  // and load the index.html of the app.
  mainWindow.loadFile(path.join(__dirname, "../build/index.html"));
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on("ready", createWindow);

// Enigma variables
let currentUsername, currentPassword;

const Database = require("better-sqlite3");

const {encryptText, decryptText} = require("../src/scripts/encoder");

// Authenticates user
ipcMain.handle('loginUser', async (event, ...args) => {
  // Gets user login data
  const [username, password] = args;
  let authStatus = false;

  // Encodes user password
  const { SHA256 } = require("sha2");
  const passwordBuffer = SHA256(password);
  const encodedPassword = passwordBuffer.toString("base64");

  // Connects to the database
  const dbPath = path.join(__dirname, "../src/assets/vault.db");
  const db = new Database(dbPath);

  // Checks for user existence and matching encoded passwords
  const query = `SELECT * FROM USERS WHERE USERNAME = '${username}' AND PASSWORD = '${encodedPassword}'`;
  const stmt = db.prepare(query)
  const rows = stmt.all()
  
  if (rows.length > 0) {
    // Sets backend variables
    currentUsername = rows[0]["USERNAME"];
    currentPassword = password;
    authStatus = true;
  }
  
  db.close();

  return authStatus;
});

// Returns passwords related to the logged user
ipcMain.handle('getPasswords', async (event, ...args) => {
  let results = [];

  // Connects to the database
  const dbPath = path.join(__dirname, "../src/assets/vault.db");
  const db = new Database(dbPath);

  // Gets passwords
  const query = `SELECT * FROM PASSWORDS WHERE USERNAME = '${currentUsername}'`;
  const stmt = db.prepare(query);
  const rows = stmt.all();

  results = rows;

  for (let i = 0; i < results.length; i++) {
    results[i]["PASSWORD"] = decryptText(
      results[i]["PASSWORD"],
      currentPassword
    );
  }

  db.close();

  return results;
});

// Creates or updates a password entry
ipcMain.handle('setPassword', async (event, ...args) => {
  const [targetPassword, targetDescription, targetLogin] = args;
  const encryptedPassword = encryptText(targetPassword, currentPassword);
  let results = [];

  // Connects to the database
  const dbPath = path.join(__dirname, "../src/assets/vault.db");
  const db = new Database(dbPath);

  const query = `SELECT * FROM PASSWORDS WHERE USERNAME = '${currentUsername}' AND DESCRIPTION = '${targetDescription}'`;
  const stmt = db.prepare(query);
  const rows = stmt.all();
  results = rows;

  if (results.length === 1){
    // Update password
    const query = `UPDATE PASSWORDS SET PASSWORD = '${encryptedPassword}', LOGIN = '${targetLogin}' WHERE DESCRIPTION = '${targetDescription}' AND USERNAME = '${currentUsername}'`;
    const stmt = db.prepare(query)
    stmt.run()
    
  } else if (results.length === 0){
    // Create password
    const query = `INSERT INTO PASSWORDS (USERNAME, DESCRIPTION, LOGIN, PASSWORD) VALUES (?, ?, ?, ?)`;
    const stmt = db.prepare(query);
    stmt.run(currentUsername, targetDescription, targetLogin, encryptedPassword);
  }
  
  db.close();

});

// Deletes a password
ipcMain.handle('deletePassword', async (event, ...args) => {
  const [targetDescription] = args;

  // Connects to the database
  const dbPath = path.join(__dirname, "../src/assets/vault.db");
  const db = new Database(dbPath);

  const query = `DELETE FROM PASSWORDS WHERE DESCRIPTION = '${targetDescription}' AND USERNAME = '${currentUsername}' `;
  const stmt = db.prepare(query);
  stmt.run();

  db.close();

});