from pydantic import BaseModel

class EmployeeSchema(BaseModel):
    name: str
    email: str
    admin_login: str
    admin_password: str
    phone:str
    cpf: str
    cep: str
    
    class Config:
        orm_mode = True