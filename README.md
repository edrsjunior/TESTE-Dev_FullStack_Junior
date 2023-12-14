<h1 align="center" id="title">Site de Vendas de Carros Usados</h1>

<p align="center"><img src="https://socialify.git.ci/edrsjunior/TESTE-Dev_FullStack_Junior/image?description=1&amp;descriptionEditable=Um%20projeto%20feito%20como%20prova%20para%20Dev%20Fullstack%20Junior&amp;forks=1&amp;issues=1&amp;language=1&amp;logo=https%3A%2F%2Fgithub.com%2Fedrsjunior.png&amp;name=1&amp;owner=1&amp;pattern=Signal&amp;pulls=1&amp;stargazers=1&amp;theme=Light" alt="project-image"></p>

<p id="description">A ideia do projeto é desenvolver um sistema de catálogo de veículos a venda utilizando Python/FASTAPI e NodeJS/REACT junto a um banco de dados MySQL hospedado na AWS.</p>

<h2>🚀 Demo</h2>

[url demo](url demo)

<h2>Project Screenshots:</h2>

<img src="https://github.com/edrsjunior/TESTE-Dev_FullStack_Junior/blob/frontStart/screenshots/Captura%20da%20Web_13-12-2023_191055_localhost.jpeg?raw=true" alt="project-screenshot" width="1920" height="/">

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   No projeto temos as seguintes features/regras de negócio:
*   Autenticação com token JWT
*   CRUD de Veículos
*   Somente o usuário dono do post ou os usuários administrativos podem alterar ou deletar um post
*   Non Destructive Delete

<h2>🛠️ Installation Steps:</h2>

<p>1. Baixar as dependências para o backend/FASTAPI</p>

```
pip install mysql-connector bcrypt cloudinary python-dotenv fastapi PyJWT pydantic pydantic-settings pydantic_core
```

<p>2. Baixar as dependências para o frontEnd</p>

```
npm i axios react react-dom react-scripts web-vitals
```

<p>3. Go to FastAPI directory</p>

```
 cd .\FASTAPI\
```

<p>4. Run FastAPI</p>

```
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

<p>5. Send HTTP requests to</p>

```
http://localhost:8000
```

<p>6. Go to REACT App directory</p>

```
 cd .\REACT\car-sell\
```

<p>7. Run REACT App</p>

```
npm start
```

<p>8. Access the web page on</p>

```
http://localhost:3000
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   Python
*   NodeJS
*   React
*   FastAPI
*   JWT