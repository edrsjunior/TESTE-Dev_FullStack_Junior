import datetime
from typing import Union
from fastapi import FastAPI, Request, requests
from Middlewares.connectDB import connection
from Models.userModel import User
from  Middlewares.encryptPass import encryptPass,descriptPass
from Middlewares.jwtVerify import verifyJWTToken
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from Models.tokenModel import token


load_dotenv()
app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/users")
async def newUser(usuario: User):
    query = "INSERT INTO usuario (email, senha) VALUES (%s, %s)"
    cursor = connection.cursor()
    cursor.execute(query,(usuario.email, encryptPass(usuario.senha)))
    connection.commit()

@app.post("/login")
async def loginUser(usuario: User):
    cursor = connection.cursor()

    
    cursor.execute("SELECT COUNT(*) AS total FROM usuario WHERE email = %(usuario.email)s", {'usuario.email':usuario.email})
    result = cursor.fetchone()[0]

    if result == 0:
        raise HTTPException(
            status_code= 401,
            detail="Usuário não encontrado"
        )
    
    cursor.execute("SELECT senha FROM usuario WHERE email = %s", (usuario.email,))
    result = cursor.fetchone()[0]

    if  not descriptPass(usuario.senha, result):
        raise HTTPException(
            status_code= 401,
            detail="Senha Incorreta"
        )
        
    # CREATE TOKEN
    # VAMOS CRIAR UM TOKEN TEMP
    payload = {
        "email" : usuario.email,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)
         
    }
    print(os.getenv("MY_JWT_KEY"))
    encodeToken = jwt.encode(payload,os.getenv("MY_JWT_KEY"),"HS256")
    return {"token" : encodeToken}
        
@app.post("/carros")
async def cadastrarCarro(tokenModel: token):
    
    print(tokenModel.token)
    try:
        verifyJWTToken(tokenModel.token)
           
    except jwt.exceptions.InvalidSignatureError:
             raise HTTPException(
                status_code= 498,
                detail="Invalid Token"
            )
    
    except jwt.ExpiredSignatureError:
             raise HTTPException(
                status_code= 498,
                detail="Expired Token"
            )
    print("AUTENTICADO MEU CHEFE")    

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
