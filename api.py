import datetime
from typing import Annotated, Union
from fastapi import Depends, FastAPI, Form, Request, UploadFile, requests
from fastapi.security import OAuth2PasswordBearer
from Middlewares.checkAdm import isAdminUser
from Middlewares.connectDB import connection
from Models.userModel import User
from Models.loginModel import UserLogin
from  Utils.encryptPass import encryptPass,descriptPass
from Utils.jwtVerify import verifyJWTToken
from fastapi import HTTPException
import jwt
from dotenv import load_dotenv
import os
from Models.carroModel import Carro
from Utils.imageControler import uploadImg,deleteImg
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
    try:
        cursor.execute(query,(usuario.nome, usuario.sobrenome,usuario.email, encryptPass(usuario.senha)))
        connection.commit()
    except:
        raise HTTPException(
            status_code= 401,
            detail="Email Already in Use"
        )
    

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

@app.get("/carros")
async def listarCarros():
    query = "SELECT nome, marca, modelo, ano, km, valor, descricao, photoUrl,creator FROM veiculosAnuncio WHERE ativo = 1"
    cursor = connection.cursor()
    
    try:
         cursor.execute(query)
    except:
        raise HTTPException(
            status_code= 500,
            detail="Error to get data"
        )

    result = cursor.fetchall()

    return result


@app.post("/carros")
async def cadastrarCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], ano: Annotated[int, Form()], km: Annotated[float, Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()],image: Annotated[UploadFile, File()],token: Annotated[str, Depends(oauth2_scheme)]):

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

    # car = Carro(nome=nome, marca=marca, modelo=modelo, valor=valor, desc=desc)

   
    #AGORA VAMOS SALVAr AS INFOs no BD e a URL DO CAR
    query = "INSERT INTO veiculosAnuncio (nome, marca, modelo, ano, km, valor, descricao,creator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(nome, marca, modelo, ano, km,valor,desc,userId))
        connection.commit()
         #VAMOS SALVAr A IMG
        lastInsert = cursor.lastrowid
        content = await image.read()
        urlImg = await uploadImg(content,userId)
        query = "UPDATE veiculosAnuncio SET photoUrl = %s WHERE id = %s"
        cursor.execute(query, (urlImg['url'],lastInsert))
        connection.commit()
    except:
        raise HTTPException(
                status_code= 500,
                detail="Internal Error"
            )   

    return {"idPostCreated" : lastInsert}

@app.delete("/carros/{item_id}")
async def deleteCarro(item_id: int,token: Annotated[str, Depends(oauth2_scheme)]):
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
    query = "UPDATE veiculosAnuncio SET ativo = 0 WHERE id = %s"
    cursor = connection.cursor()
   
    cursor.execute(query,(item_id,))
    connection.commit()

@app.put("/carros/{item_id}")
async def updateCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], ano: Annotated[int, Form()], km: Annotated[float, Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()],image: Annotated[UploadFile, File()],item_id: int,token: Annotated[str, Depends(oauth2_scheme)]):   
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
    
    #CHECK SE O POST É DA PESSOA 
    query = "SELECT creator from veiculosAnuncio creator WHERE id = %s AND ativo = TRUE"
    cursor = connection.cursor()
    cursor.execute(query,(item_id,))
    result = cursor.fetchone()

    if not result:
         raise HTTPException(
                status_code= 404,
                detail="Object Not Found"
            )
    
    if not isAdminUser(userId):
        if not (result[0] == userId):
            raise HTTPException(
                    status_code= 405,
                    detail="Method Not Allowed to this Object"
                )

    ################################
    # deleteImg(item_id)
    content = await image.read()
    urlImg = await uploadImg(content,userId)
    #AGORA VAMOS SALVAr AS INFOs no BD e a URL DO CAR
    query = "UPDATE veiculosAnuncio SET nome = %s, marca = %s, modelo = %s, ano =%s, km = %s, valor = %s, descricao = %s, photoUrl = %s WHERE id = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(nome, marca, modelo, ano, km, valor,desc,urlImg['url'],item_id))
        connection.commit()
    except:
        raise HTTPException(
                status_code= 500,
                detail="Internal Error"
            )
    

# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
