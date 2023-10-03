from fastapi import FastAPI,Depends, HTTPException, status
from schemas.client import ClientSchema
from schemas.product import ProdutSchema
from schemas.sale import SaleSchema
from schemas.employee import EmployeeSchema
from controller.sale import create_sale_db, get_sale_db, get_sale_by_id_db, delete_sale_by_id, sale_report
from controller.clients import get_clients, create_client_db, get_client_id, update_client_by_id, delete_client_by_id,get_clients_by_name_db, get_clients_by_partial_name_db
from controller.product import get_product_db, create_product_db, get_product_by_id, update_product_by_id, delete_product_by_id, get_product_by_name_db, get_product_by_partial_name_db
from controller.employee import get_all_employee_db, create_employee_db, update_employee_by_id, delete_employee_by_id, get_employee_by_id_bd, get_employee_by_partial_name_db, get_employee_by_name_db
from database import SessionLocal,Base,engine
from sqlalchemy.orm import Session
from typing import List
from database import Base,engine

Base.metadata.create_all(engine)

db=SessionLocal()

app = FastAPI()
    
@app.get("/")
def index():
    return {"message":"Hello world"}

#Clients

@app.get('/client', response_model=List[ClientSchema], status_code=200)
def get_all_clients():
    return get_clients(db)

@app.get('/client/id/{client_id}')
def get_client_by_id(client_id:int):
    return get_client_id(client_id, db)

@app.get('/client/name/{client_name}')
def get_client_by_name(client_name:str):
    return get_clients_by_name_db(client_name, db)

@app.get('/client/partial_name/{client_name}')
def get_clients_by_partial_name(client_name:str):
    return get_clients_by_partial_name_db(client_name, db)


@app.post('/client', response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
def create_client(client: ClientSchema):
    return create_client_db(client, db)


@app.put('/client/id/{client_id}', response_model=ClientSchema, status_code=status.HTTP_200_OK)
def update_client(client_id: int, client_data: ClientSchema):
    client = update_client_by_id(client_id, client_data, db)
    return client

@app.delete('/client/id/{client_id}', response_model=ClientSchema, status_code=status.HTTP_200_OK)
def delete_client(client_id: int):
    client = delete_client_by_id(client_id, db)
    return client

#Employee

@app.get('/employee', response_model=List[EmployeeSchema], status_code=200)
def get_all_employee():
    return get_all_employee_db(db)

@app.get('/employee/id/{employee_id}')
def get_employee_by_id(employee_id:int):
    return get_employee_by_id_bd(employee_id, db)

@app.get('/employee/name/{employee_name}')
def get_employee_by_name(employee_name:str):
    return get_employee_by_name_db(employee_name, db)

@app.get('/employee/partial_name/{employee_name}')
def get_employee_by_partial_name(employee_name:str):
    return get_employee_by_partial_name_db(employee_name, db)

@app.post('/employee', response_model=EmployeeSchema, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeSchema):
    return create_employee_db(employee, db)

@app.put('/employee/id/{employee_id}', response_model=EmployeeSchema, status_code=status.HTTP_200_OK)
def update_employee(employee_id: int, employee_data: EmployeeSchema):
    employee = update_employee_by_id(employee_id, employee_data, db)
    return employee

@app.delete('/employee/id/{employee_id}', response_model=EmployeeSchema, status_code=status.HTTP_200_OK)
def delete_employee(employee_id: int):
    employee = delete_employee_by_id(employee_id, db)
    return employee

#Produts

@app.get('/product', response_model=List[ProdutSchema], status_code=200)
def get_all_products():
    return get_product_db(db)

@app.get('/product/id/{product_id}', response_model=ProdutSchema, status_code=status.HTTP_200_OK)
def get_product(product_id: int):
    product = get_product_by_id(product_id, db)
    return product

@app.get('/product/name/{product_name}')
def get_product_by_name(product_name:str):
    return get_product_by_name_db(product_name, db)

@app.get('/product/partial_name/{product_name}')
def get_product_by_partial_name(product_name:str):
    return get_product_by_partial_name_db(product_name, db)

@app.post('/product', response_model=ProdutSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProdutSchema):
    return create_product_db(product, db)

@app.put('/product/id/{product_id}', response_model=ProdutSchema, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_data: ProdutSchema):
    product = update_product_by_id(product_id, product_data, db)
    return product

@app.delete('/product/id/{product_id}', status_code=status.HTTP_200_OK)
def delete_product(product_id: int):
    product = delete_product_by_id(product_id, db)
    return product


#Sales

@app.get('/sale', response_model=List[SaleSchema], status_code=200)
def get_sale():
    return get_sale_db(db)

@app.get('/sale/id/{sale_id}', response_model=SaleSchema, status_code=status.HTTP_200_OK)
def get_sale_by_id(sale_id: int):
    sale = get_sale_by_id_db(sale_id, db)
    return sale

@app.post('/sale', response_model=SaleSchema, status_code=status.HTTP_201_CREATED)
def create_sale(sale_data: SaleSchema):
    sale = create_sale_db(sale_data, db)
    return sale

@app.delete('/sale/id/{sale_id}', status_code=status.HTTP_200_OK)
def delete_sale(sale_id: int):
    sale = delete_sale_by_id(sale_id, db)
    return sale
