from pydantic import BaseModel

class ClientSchema(BaseModel):
    name: str
    email: str
    phone:str
    cpf: str
    cep: str

    class Config:
        orm_mode =True