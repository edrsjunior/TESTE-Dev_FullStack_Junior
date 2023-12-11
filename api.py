import datetime
from typing import Annotated, Union
from fastapi import FastAPI, Form, Request, UploadFile, requests
from Middlewares.connectDB import connection
from Models.userModel import User
from  Middlewares.encryptPass import encryptPass,descriptPass
from Middlewares.jwtVerify import verifyJWTToken
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from Models.carroModel import Carro
from Models.tokenModel import token
from Middlewares.uploadImage import uploadImg
from pydantic import BaseModel
from fastapi import FastAPI, Form
from fastapi import FastAPI, File, UploadFile

SESSION_TIME = 60

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
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=SESSION_TIME)
         
    }
    print(os.getenv("MY_JWT_KEY"))
    encodeToken = jwt.encode(payload,os.getenv("MY_JWT_KEY"),"HS256")
    return {"token" : encodeToken}
        
@app.post("/carros")
async def cadastrarCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()], token: Annotated[str,Form()],image: Annotated[UploadFile, File()]):
    car = Carro(nome=nome, marca=marca, modelo=modelo, valor=valor, desc=desc)
    # print(car)
    #print(token)

    try:
        verifyJWTToken(token)
           
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

    #VAMOS SALVAr A IMG
    content = await image.read()
    urlImg = await uploadImg(content,"carros/")
    #AGORA VAMOS SALVAr AS INFOs no BD e a URL DO CAR
    query = "INSERT INTO veiculosAnuncios (nome, marca, modelo, valor, descricao, photoUrl) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(nome, marca, modelo,valor,desc,urlImg['url']))
        connection.commit()
    except:
        print("ERRO PAI")
    

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
