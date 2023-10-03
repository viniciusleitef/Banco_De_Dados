from pydantic import BaseModel

class SaleSchema(BaseModel):
    client_id: int
    employee_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True