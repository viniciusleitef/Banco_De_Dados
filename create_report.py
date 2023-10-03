from controller.sale import sale_report
from controller.clients import client_report
from controller.product import product_report
from controller.employee import employee_report
from database import SessionLocal

db=SessionLocal()

def all_report(db):
    relatorio = client_report(db) + employee_report(db) + product_report(db) + sale_report(db) 
    return relatorio
    
def create_all_report(db):
    relatorio = all_report(db)
    arquivo = open("./relatórios/sale_report.txt", "w")
    arquivo.write(relatorio)
    
create_all_report(db)
