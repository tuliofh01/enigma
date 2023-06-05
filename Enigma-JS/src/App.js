import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login.js";
import PasswordMenu from "./pages/PasswordMenu.js";
import './App.css'

function App() {
  
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/pwdMenu" element={<PasswordMenu/>} />
        </Routes>
    </Router>
  );
}

export default App;
