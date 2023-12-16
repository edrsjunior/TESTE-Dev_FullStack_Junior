from pydantic import BaseModel


class User(BaseModel):
    nome: str
    sobrenome: str
    email: str
    senha: str
