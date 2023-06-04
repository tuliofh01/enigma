import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Login.module.css';
import padlock from '../assets/padlock.png';
import { ipcRenderer } from 'electron';

function Login(){

    const usrRef = useRef(null);
    const pwdRef = useRef(null);
    const navigate = useNavigate();

    async function loginHandler(event){
        event.preventDefault();
        const username = usrRef.current.value;
        const password = pwdRef.current.value;

        const authStatus = await ipcRenderer.invoke(
          "loginUser",
          username,
          password
        );

        if (authStatus === true){
          navigate("/pwdMenu");
        }
        else {
          alert("Usuário ou senha inválidos!");
        }
    }

    return (
      <div className={styles.container}>
        <div className={styles.leftCard}>
          <h2 className={styles.title}>enigma-js</h2>
          <form className={styles.form} onSubmit={loginHandler}>
            <input ref={usrRef} type="text" className={styles.input} placeholder='Usuário'/>
            <input ref={pwdRef} type="password" className={styles.input} placeholder='Senha'/>
            <button type='submit' className={styles.button}>Logar</button>
          </form>
        </div>

        <div className={styles.rightCard}>
          <img className={styles.image} src={padlock} />
          <p className={styles.imageDescription}>
            v1.0 - created by Túlio Horta
          </p>
        </div>
      </div>
    );

}

export default Login;