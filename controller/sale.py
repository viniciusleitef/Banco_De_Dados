from sqlalchemy.orm import Session
from schemas.sale import SaleSchema
from models.model import Sale, Product, Client, Employee
from fastapi import HTTPException

def create_sale_db(sale_data: SaleSchema, db: Session):
    
    # Verificando se o cliente existe no banco de dados
    client = db.query(Client).filter(Client.id == sale_data.client_id).first()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Verificando se o employee existe no banco de dados
    employee = db.query(Employee).filter(Employee.id == sale_data.employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Client not found")

    # Verificando se o produto existe no banco de dados
    product = db.query(Product).filter(Product.id == sale_data.product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    # Verificando se há estoque suficiente do produto
    if sale_data.quantity > product.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    # Registrando a venda na tabela de vendas
    new_sale = Sale(
        client_id=sale_data.client_id,
        employee_id=sale_data.employee_id,
        product_id=sale_data.product_id,
        quantity=sale_data.quantity
    )
    db.add(new_sale)

    # Atualizando a quantidade de estoque do produto
    product.quantity -= sale_data.quantity

    db.commit()
    db.refresh(new_sale)
    return new_sale

def get_sale_db(db: Session):
    sales=db.query(Sale).all()
    if len(sales) <= 0:
        raise HTTPException(status_code=404, detail="Sales not found")
    return sales

def get_sale_by_id_db(id, db: Session):
    sale_id = db.query(Sale).filter(Sale.id == id).first()
    if sale_id is None:
        raise HTTPException(status_code=404, detail="Sale not found")   
    return sale_id    

def delete_sale_by_id(sale_id: int, db: Session):
    
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")

    db.delete(sale)
    db.commit()
    return "Histórico da venda número:" + str(sale.id) + " foi deletada!"


def sale_report(db: Session):
    sales=db.query(Sale).all()
    products = db.query(Product).all()
    faturamento = 0
    lucro = 0
    lista_produtos_price = []
    lista_produtos_cost = []
    cost_saled_products = 0
    
    for produtos in products:
        lista_produtos_price.append(produtos.price)
        lista_produtos_cost.append(produtos.price_cost)
        cost_saled_products += produtos.price_cost * (produtos.quantity_max - produtos.quantity)
        
    for venda in sales:
        faturamento += venda.quantity * lista_produtos_price[venda.product_id - 1]
    lucro += faturamento - cost_saled_products
    
    relatorio = ("-----Sale report-----" +
                 "\nForam realizadas " + str(len(sales)) + " vendas no total" +
                 "\nO custo dos produtos vendidos foi de: R$" + str(cost_saled_products) +
                 "\nO faturamento total da loja foi de: R$" + str(faturamento) +
                 "\nO lucro baseado nas vendas ja feitas eh de: R$" + str(lucro)
                 )
    
    
    return relatorio

def create_sale_report(relatorio):
  arquivo = open("./relatórios/sale_report.txt", "w")
  arquivo.write(relatorio)