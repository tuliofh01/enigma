import { useEffect, useRef, useState } from 'react';
import { ipcRenderer } from "electron";
import styles from './PasswordMenu.module.css';

function PasswordMenu(){

    const [passwords, setPasswords] = useState([]);

    const passwordRef = useRef();
    const descriptionRef = useRef();
    const loginRef = useRef();

    useEffect(() => {
      async function getData(){
        setPasswords(await ipcRenderer.invoke("getPasswords"));
      }
      getData();
    }, []);

    async function saveButtonHandler(){
      const descriptionValue = descriptionRef.current.value;
      const passwordValue = passwordRef.current.value;
      const loginValue = loginRef.current.value;
      await ipcRenderer.invoke("setPassword", passwordValue, descriptionValue, loginValue);
      setPasswords(await ipcRenderer.invoke("getPasswords")); 
    }

    async function deleteButtonHandler(){
      const deleteConfirmation = window.confirm("Você tem certeza que quer deletar estes dados?");
      if (deleteConfirmation){
        const descriptionValue = descriptionRef.current.value;
        ipcRenderer.invoke("deletePassword", descriptionValue);
        descriptionRef.current.value = "";
        passwordRef.current.value = "";
        loginRef.current.value = "";
        setPasswords(await ipcRenderer.invoke("getPasswords")); 
      }
    }

    async function tableDataHandler(event){
      const text = event.target.innerText;
      const object = passwords.filter(password => password["DESCRIPTION"] === text);
      descriptionRef.current.value = object[0]["DESCRIPTION"];
      loginRef.current.value = object[0]["LOGIN"];
      passwordRef.current.value = object[0]["PASSWORD"];
    }

    function createPassword(){
      descriptionRef.current.value = '';
      passwordRef.current.value = '';
      loginRef.current.value = '';
    }

    return (
      <div className={styles.container}>
        <div className={styles.leftCard}>
          <h3 className={styles.title}>Senhas:</h3>
          <table>
            <tbody>
              {passwords.map((password) => (
                <tr>
                  <td onClick={tableDataHandler}>{password["DESCRIPTION"]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className={styles.rightCard}>
          <label htmlFor="description" className={styles.label}>
            Descrição:
          </label>
          <input
            ref={descriptionRef}
            type="text"
            id="description"
            className={styles.input}
          />

          <label htmlFor="description" className={styles.label}>
            Login:
          </label>
          <input
            ref={loginRef}
            type="text"
            id="description"
            className={styles.input}
          />

          <label htmlFor="password" className={styles.label}>
            Senha:
          </label>
          <input
            ref={passwordRef}
            type="text"
            id="password"
            className={styles.input}
          />

          <div className={styles.buttonContainerRight}>
            <button className={styles.saveButton} onClick={saveButtonHandler}>
              Salvar
            </button>
            <button
              className={styles.deleteButton}
              onClick={deleteButtonHandler}
            >
              Deletar
            </button>
          </div>
          <button
            className={styles.createPasswordButton}
            onClick={createPassword}
          >
            Limpar campos
          </button>
        </div>
      </div>
    );

}

export default PasswordMenu;