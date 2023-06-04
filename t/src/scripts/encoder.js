const crypto = require("crypto");

function encryptText(text, password) {
  const cipher = crypto.createCipher("aes-256-cbc", password);
  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");
  return encrypted;
}

function decryptText(encryptedText, password) {
  const decipher = crypto.createDecipher("aes-256-cbc", password);
  let decrypted = decipher.update(encryptedText, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}

module.exports = {
    encryptText: encryptText,
    decryptText : decryptText
}