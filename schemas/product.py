from pydantic import BaseModel

class ProdutSchema(BaseModel):
    name: str
    price: float
    price_cost: float
    quantity: int
    quantity_max: int
    
    class Config:
        orm_mode = True