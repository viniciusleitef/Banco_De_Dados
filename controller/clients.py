from sqlalchemy.orm import Session
from schemas.client import ClientSchema
from models.model import Client
from fastapi import HTTPException

def get_clients(db: Session):
    clients=db.query(Client).all()
    if len(clients) <= 0:
        raise HTTPException(status_code=404, detail="Clients not found")
    return clients

def get_client_id(id, db: Session):
    client_id = db.query(Client).filter(Client.id == id).first()
    if client_id is None:
        raise HTTPException(status_code=404, detail="Client not found")   
    return client_id    

def get_clients_by_partial_name_db(partial_name: str, db: Session):
    clients = db.query(Client).filter(Client.name.ilike(f"%{partial_name}%")).all()
    return clients

def get_clients_by_name_db(name: str, db: Session):
    clients = db.query(Client).filter(Client.name == name).all()
    if clients is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients

def create_client_db(client:ClientSchema, db:Session):
    db_client=db.query(Client).filter(Client.cpf==client.cpf).first()
    if db_client is not None:
        raise HTTPException(status_code=400,detail="Client already exists")
    
    new_client=Client(
        name=client.name,
        email=client.email,
        phone=client.phone,
        cpf=client.cpf,
        cep=client.cep
    )
    db.add(new_client)
    db.commit()
    return new_client 


def update_client_by_id(client_id: int, client_data: ClientSchema, db: Session):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    for field, value in client_data.dict().items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client

def delete_client_by_id(client_id: int, db: Session):
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return client

def client_report(db: Session):
    quantity_cients = db.query(Client).all()
    relatorio = ("-----Client report-----" + "\nAtualmente existem " +str(len(quantity_cients))+ " clientes cadastrados no sistema\n\n")
    return relatorio