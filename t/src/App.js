<<<<<<< HEAD
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
=======
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
>>>>>>> master
  );
}

export default App;
