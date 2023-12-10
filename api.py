from typing import Union
from fastapi import FastAPI
from Middlewares.connectDB import connection
from Models.userModel import User
from  Middlewares.encryptPass import encryptPass,descriptPass
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os

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
    encodeToken = jwt.encode({"token": usuario.email},os.getenv("MY_JET_KEY"),None)
    return {"token" : encodeToken}
        

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
