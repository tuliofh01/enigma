async function dbSetup(username, password){
  const path = require("path");
  const Database = require("better-sqlite3");

  const dbPath = path.join(__dirname, "../assets/vault.db");

  // Creating tables
  const db = new Database(dbPath);

  let stmt = db.prepare(
    `CREATE TABLE IF NOT EXISTS USERS (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    USERNAME TEXT,
    PASSWORD BLOB)`
  );
  stmt.run();
  
  stmt = db.prepare(
    `CREATE TABLE IF NOT EXISTS PASSWORDS (
    DESCRIPTION TEXT PRIMARY KEY,
    USERNAME TEXT,  
    PASSWORD BLOB)`
  );
  stmt.run();

  // Inserting user
  stmt = db.prepare("INSERT INTO USERS (USERNAME, PASSWORD) VALUES (?, ?)");
  stmt.run(username, password);

  db.close()

  console.log("Database setup complete!");
}

function main(){
  const prompt = require("prompt-sync")();
  const { SHA256 } = require("sha2");


  const username = prompt("Please, enter your username:");
  const password = prompt("Please, enter your password:");

  const passwordBuffer = SHA256(password);
  const encodedPassword = passwordBuffer.toString("base64");

  dbSetup(username, encodedPassword);
}

main();


