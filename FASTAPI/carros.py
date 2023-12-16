from typing import Annotated
from fastapi import Depends, FastAPI, Form, Request, UploadFile
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt
from Middlewares.checkAdm import isAdminUser
from Middlewares.connectDB import connection
from Utils.jwtTools import validateAccess
from fastapi import HTTPException
from Utils.imageControler import uploadImg
from fastapi import FastAPI, Form
from fastapi import FastAPI, File, UploadFile

car = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")          

@car.middleware("http")
async def verificaToken(req: Request, call_next):
    try:    
        token = req.headers["authorization"].split(" ")[1]
        userId = validateAccess(token)
        req.state.userId = userId
        response = await call_next(req)
        return response
    except:
            return JSONResponse(content={
            "message": "Unauthorized"
        }, status_code=498)
    
  
    
  

    

@car.post("/cadastrar")

# Annotated[str,Form()] informa que o dado vira de um multipart 

async def cadastrarCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], ano: Annotated[int, Form()], km: Annotated[float, Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()],image: Annotated[UploadFile, File()],req: Request):

    userId = req.state.userId
    #AGORA VAMOS SALVAr AS INFOs no BD e a URL DO CAR
    query = "INSERT INTO veiculosAnuncio (nome, marca, modelo, ano, km, valor, descricao,creator) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        cursor.execute(query,(nome, marca, modelo, ano, km,valor,desc,userId))
        connection.commit()
         #VAMOS SALVAr A IMG
        # pega o ultimo id gerado pelo insert
        lastInsert = cursor.lastrowid
        # espera o arquivo subir
        content = await image.read()
        # espera a img subir para o Cloudnary
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

@car.delete("/delete/{item_id}")
async def deleteCarro(item_id: int,req: Request):
    userId = req.state.userId
    
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

    query = "UPDATE veiculosAnuncio SET ativo = 0 WHERE id = %s"
    cursor = connection.cursor()
   
    cursor.execute(query,(item_id,))
    connection.commit()

@car.put("/update/{item_id}")
async def updateCarro(nome: Annotated[str,Form()], marca: Annotated[str,Form()], modelo: Annotated[str,Form()], ano: Annotated[int, Form()], km: Annotated[float, Form()], valor: Annotated[float,Form()], desc: Annotated[str,Form()],image: Annotated[UploadFile, File()],item_id: int,req: Request):  

    userId = req.state.userId
    
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

