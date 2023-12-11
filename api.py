import datetime
from typing import Annotated, Union
from fastapi import Depends, FastAPI, Form, Request, UploadFile, requests
from fastapi.security import OAuth2PasswordBearer
from Middlewares.connectDB import connection
from Models.userModel import User
from Models.loginModel import UserLogin
from  Middlewares.encryptPass import encryptPass,descriptPass
from Middlewares.jwtVerify import verifyJWTToken
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from Models.carroModel import Carro
from Middlewares.uploadImage import uploadImg
from pydantic import BaseModel
from fastapi import FastAPI, Form
from fastapi import FastAPI, File, UploadFile

SESSION_TIME = 60

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/users")
async def newUser(usuario: User):
    query = "INSERT INTO usuario (nome, sobrenome,email, senha) VALUES (%s, %s, %s, %s)"
    cursor = connection.cursor()
    cursor.execute(query,(usuario.nome, usuario.sobrenome,usuario.email, encryptPass(usuario.senha)))
    connection.commit()

@app.post("/login")
async def loginUser(usuario: UserLogin):
    cursor = connection.cursor()

    
    cursor.execute("SELECT COUNT(*) AS total FROM usuario WHERE email = %(usuario.email)s AND ativo = TRUE", {'usuario.email':usuario.email})
    result = cursor.fetchone()[0]
    if result == 0:
        raise HTTPException(
            status_code= 401,
            detail="Usuário ou senha incorreto"
        )
    
    cursor.execute("SELECT id,senha FROM usuario WHERE email = %s", (usuario.email,))
    result = cursor.fetchone()
    

    if  not descriptPass(usuario.senha, result[1]):
        raise HTTPException(
            status_code= 401,
            detail="Usuário ou senha incorreto"
        )
        
    # CREATE TOKEN
    # VAMOS CRIAR UM TOKEN TEMP
    payload = {
        "id" : result[0],
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=SESSION_TIME)
         
    }
    print(os.getenv("MY_JWT_KEY"))
    encodeToken = jwt.encode(payload,os.getenv("MY_JWT_KEY"),"HS256")
    return {"token" : encodeToken}
        
@app.post("/carros")
async def cadastrarCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()],image: Annotated[UploadFile, File()],token: Annotated[str, Depends(oauth2_scheme)]):
    car = Carro(nome=nome, marca=marca, modelo=modelo, valor=valor, desc=desc)

    try:
        userId = verifyJWTToken(token)
           
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
    # print("AUTENTICADO MEU CHEFE")

    #VAMOS SALVAr A IMG
    content = await image.read()
    urlImg = await uploadImg(content,"carros/")
    #AGORA VAMOS SALVAr AS INFOs no BD e a URL DO CAR
    query = "INSERT INTO veiculosAnuncio (nome, marca, modelo, valor, descricao, photoUrl,creator) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(nome, marca, modelo,valor,desc,urlImg['url'],userId))
        connection.commit()
    except:
        raise HTTPException(
                status_code= 500,
                detail="Internal Error"
            )
    

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
