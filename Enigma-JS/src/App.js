import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login.js";
import PasswordMenu from "./pages/PasswordMenu.js";
import './App.css'
import CreateUser from "./pages/CreateUser.js";

function App() {
  
  return (
    <Router>
        <Routes>
          <Route path="/" element={<Login/>} />
          <Route path="/pwdMenu" element={<PasswordMenu/>} />
          <Route path="/createUser" element={<CreateUser/>} />
        </Routes>
    </Router>
  );
}

export default App;
