import datetime
import json
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from Middlewares.connectDB import connection
from DTOs.userModel import User
from DTOs.loginModel import UserLogin
from  Utils.encryptPass import encryptPass,descriptPass
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi import FastAPI

from carros import car

SESSION_TIME = 60

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ISSO PARA EVITAR O PROBLEMA DE CROSS 
# ORIGIN QUANDO FEITO AS REQs HTTP PELO REACT

from fastapi.middleware.cors import CORSMiddleware
            

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------

# CADASTRO DE NOVOS USUARIOS

@app.post("/users")
async def newUser(usuario: User):
    query = "INSERT INTO usuario (nome, sobrenome,email, senha) VALUES (%s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(usuario.nome, usuario.sobrenome,usuario.email, encryptPass(usuario.senha)))
        connection.commit()
    # CASO NAO CONSIGA INSERIR POR MOTIVO DE O EMAIL QUE É A PK JA EXISTIR NO BD
    # LANCAMOS UMA EXCECAO
    except:
        raise HTTPException(
            status_code= 401,
            detail="Email Already in Use"
        )
    
# ------------------------------------------------------------------------

# O LOGIN QUE GERA O TOKEN JWT, LEMBRANDO QUE O TOKEN DE VALIDADE DE 60 MINUTOS DEFINIDO PELA 
# CONSTANTE <SESSION>

@app.post("/login")
async def loginUser(usuario: UserLogin):
    cursor = connection.cursor()

    
    cursor.execute("SELECT COUNT(*) AS total FROM usuario WHERE email = %(usuario.email)s AND ativo = TRUE", {'usuario.email':usuario.email})
    #TEMOS O FETCHONE PARA RETORNA A PRIMEIRA LINHA DA RESPOSTA DO BD 
    #E O[0] para retornar apenas o primeiro valor ja que o padrão é retornar uma tupla ex.: (1,)
    result = cursor.fetchone()[0]
    if result == 0:
        raise HTTPException(
            status_code= 401,
            detail="Usuário ou senha incorreto"
        )
    
    # pega o id para associar ao token para ser utilizado em outras reqs
    cursor.execute("SELECT id,senha FROM usuario WHERE email = %s", (usuario.email,))
    result = cursor.fetchone()
    
    # verifica se s a senha passada é igual a registrada no bd com o bcrypt
    if  not descriptPass(usuario.senha, result[1]):
        raise HTTPException(
            status_code= 401,
            detail="Usuário ou senha incorreto"
        )
        
    # CREATE TOKEN
    # VAMOS CRIAR UM TOKEN TEMP
    # o payload é a carga ou seja a informacao a ser salva no token
    payload = {
        "id" : result[0],
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=SESSION_TIME)
         
    }
    encodeToken = jwt.encode(payload,os.getenv("MY_JWT_KEY"),"HS256")
    return {"token" : encodeToken}

#-----------------------------------------------------------------------------------------------------

@app.get("/carros")
async def listarCarros():
    query = "SELECT id, nome, marca, modelo, ano, km, valor, descricao, photoUrl,creator FROM veiculosAnuncio WHERE ativo = 1 ORDER BY valor DESC"
    cursor = connection.cursor()
    
    try:
         cursor.execute(query)
    except:
        raise HTTPException(
            status_code= 500,
            detail="Error to get data"
        )

    # pega todas a linhas que a querry retorna
    result = cursor.fetchall()

    # Cria um array para salvar tudo
    carros = []
    for carro in result:
        # Aqui que que que temos uma detalhe legal, armazenamemos antes de salvar
        # na lista a combinação dos valores de cursor.description que possui o nome e tipo dos
        # campos do retorno da querry e após junta o primeiro valor de coluna ou seja o nome do campo
        #com seu valor real
        carro_dict = dict(zip([coluna[0] for coluna in cursor.description], carro))
        carros.append(carro_dict)

    return json.dumps(carros)


app.mount("/carros/", car)