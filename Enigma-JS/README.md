# Enigma-JS
### *Último update - (04/06/2023)*

## Resumo:
- Enigma-JS é um *password manager* simples feito totalmente em JS (Node, React e Electron).
- Os dados são armazenados em um banco de dados local SQLite3.
- O código é de graça para usar e quaisquer sugestões para melhorias são bem vindas.

## Criptografia:
- Enigma-JS faz o uso da criptografia *aes-256-cbc* para proteger as senhas armazenadas.

## Informações importantes:
- A versão CLI do Engima é consideravelmente mais segura do que a versão GUI, pois faz uso de salt, pepper e repetição do algoritmo de criptografia, porém a versão GUI oferece um nível de segurança razoável para a utilização cotidiana.
- O código foi, **até agora**, testado nos sistemas Windows 10 e Linux (Manjaro OS). Alterações talvez necessitem de ser feitas para compatibilidade com outros sistemas.
- Você **deve** executar o script db-setup.js (*./src/assets/scripts/db-setup.js*) para criar o seu usuário e configurar o banco de dados local antes de executar o Enigma, ou então o app não funcionará.

## Building:
- Use o comando *npm i --force* para instalar as dependências do programa.
- Execute o script db-setup.js para configurar o banco de dados e criar usuários (não mais necessário depois da última atualizaç).
- Execute os scrips build, rebuild e postinstall, definidos no package.json, antes de executar o programa por meio de *npm run start*.
- Para gerar um arquivo executável utilize a plataforma "electron-packager".

## Créditos:
- Engima-JS está sendo criado, mantido e desenvolvido por **Túlio Horta**.
