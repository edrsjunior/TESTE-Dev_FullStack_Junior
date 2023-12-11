from pydantic import BaseModel

class Carro(BaseModel):
    nome: str
    marca: str
    modelo: str
    valor: float
    desc: str

