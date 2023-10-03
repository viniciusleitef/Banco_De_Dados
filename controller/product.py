from sqlalchemy.orm import Session
from schemas.product import ProdutSchema
from models.model import Product
from fastapi import HTTPException

def get_product_db(db: Session):
    products = db.query(Product).all()
    if len(products) <= 0:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

def get_product_by_partial_name_db(partial_name: str, db: Session):
    product = db.query(Product).filter(Product.name.ilike(f"%{partial_name}%")).all()
    return product

def get_product_by_name_db(name: str, db: Session):
    product = db.query(Product).filter(Product.name == name).all()
    if product is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return product

def create_product_db(product: ProdutSchema, db: Session):
    db_product=db.query(Product).filter(Product.name==product.name).first()
    if db_product is not None:
        raise HTTPException(status_code=400,detail="Product already exists")
    
    new_product=Product(
        name = product.name,
        price = product.price,
        price_cost = product.price_cost,
        quantity = product.quantity,
        quantity_max = product.quantity_max
    )
    
    db.add(new_product)
    db.commit()
    
    return new_product


def get_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def update_product_by_id(product_id: int, product_data: ProdutSchema, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product_data.dict().items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

def delete_product_by_id(product_id: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    
    return product

def product_report(db: Session):
    quantity_products = db.query(Product).all()
    custo_total = 0
    faturamento_esperado = 0
    quantidade_estoque = ""
    faturamento_atual = 0
    lucro_atual = 0
    
    for product in quantity_products:
        custo_total += (product.price_cost * product.quantity_max)
        faturamento_esperado += (product.price * product.quantity_max)
        quantidade_estoque += "O produto '" +  product.name + "' possui " + str(product.quantity) + " unidades em estoque\n" 
        faturamento_atual += (product.quantity_max - product.quantity) * product.price
    lucro_atual += faturamento_atual - custo_total
    
    if lucro_atual < 0:
        lucro_atual_text = "\n- Ainda nao obtivemos lucro, estamos do prejuizo de: -R$" + str(lucro_atual * -1)
    elif lucro_atual == 0:
        lucro_atual_text = "\n- Ja pagamos todo o estoque, tudo que for vendido a partir de agora eh lucro: R$" + str(lucro_atual)
    else:
        lucro_atual_text = "\n- O lucro atual eh: R$" + str(lucro_atual)
        
    relatorio = ("-----Product report-----" +
                 "\n- Existem " + str(len(quantity_products)) + " produtos cadastrados no sistema"+
                 "\n- O custo total do estoque foi de: R$" + str(custo_total) +
                 "\n- O faturamento total esperado(venda de todos os produtos) eh de: R$" + str(faturamento_esperado) + 
                 "\n- O lucro total esperado(venda de todos os produtos) eh de: R$" + str(faturamento_esperado - custo_total) + 
                 "\n- O faturamento atual eh de: R$" + str(faturamento_atual) +
                 lucro_atual_text + "\n" +
                 "\n" + quantidade_estoque + "\n")
        
    return relatorio

def create_product_report(relatorio):
  arquivo = open("./relatórios/product_report.txt", "w")
  arquivo.write(relatorio)