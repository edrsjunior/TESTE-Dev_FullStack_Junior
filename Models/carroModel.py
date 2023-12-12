from pydantic import BaseModel

class Carro(BaseModel):
    nome: str
    marca: str
    modelo: str
    ano: int
    km: float
    valor: float
    desc: str

