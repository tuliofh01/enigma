import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { ipcRenderer } from "electron";
import styles from './CreateUser.module.css'
import padlock from '../assets/padlock.png'


function CreateUser(){

    const userRef = useRef();
    const passwordRef = useRef();
    const navigate = useNavigate();

    async function formHandler(event){
        event.preventDefault();

        const username = userRef.current.value;
        const password = passwordRef.current.value;

        try {
            await ipcRenderer.invoke(
                "createUser",
                username,
                password
            );
            alert("Usuário criado com sucesso!");
            navigate("/")
        } catch(err){
            alert("Erro ao criar usuário...");
            navigate("/");
        }
    }

    return (
      <div className={styles.container}>
        <div className={styles.leftCard}>
          <img className={styles.image} src={padlock} />
          <p className={styles.imageDescription}>
            v1.0 - created by Túlio Horta
          </p>
        </div>

        <div className={styles.rightCard}>
          <h3 className={styles.header}>Criar Usuário</h3>
          <form className={styles.form} onSubmit={formHandler}>
            <input
              ref={userRef}
              className={styles.input}
              placeholder="Usuário"
            />
            <input
              ref={passwordRef}
              className={styles.input}
              placeholder="Senha"
            />
            <button type="submit" className={styles.button}>
              Confirmar
            </button>
          </form>
        </div>
      </div>
    );

}

export default CreateUser;