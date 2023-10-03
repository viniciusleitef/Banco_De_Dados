from sqlalchemy.orm import Session
from schemas.employee import EmployeeSchema
from models.model import Employee
from fastapi import HTTPException

def get_all_employee_db(db: Session):
    employee = db.query(Employee).all()
    if len(employee) <= 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def get_employee_by_id_bd(employee_id: int, db: Session):
    employee_id = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee_id is None:
        raise HTTPException(status_code=404, detail="Employee not found")   
    return employee_id 

def get_employee_by_partial_name_db(partial_name: str, db: Session):
    employee = db.query(Employee).filter(Employee.name.ilike(f"%{partial_name}%")).all()
    return employee

def get_employee_by_cpf_bd(employee_cpf: str, db: Session):
    employee_cpf = db.query(Employee).filter(Employee.cpf == employee_cpf).first()
    if employee_cpf is None:
        raise HTTPException(status_code=404, detail="Employee not found")   
    return employee_cpf 

def get_employee_by_cep_bd(employee_cep: str, db: Session):
    employee = db.query(Employee).filter(Employee.cep.ilike(f"%{employee_cep}%")).all()
    if employee_cep is None:
        raise HTTPException(status_code=404, detail="Employee not found")   
    return employee_cep 

def get_employee_by_name_db(name: str, db: Session):
    employee = db.query(Employee).filter(Employee.name == name).all()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

def create_employee_db(employee: EmployeeSchema, db: Session):
    db_employee=db.query(Employee).filter(Employee.cpf==employee.cpf).first()
    if db_employee is not None:
        raise HTTPException(status_code=400,detail="Employee already exists")
    
    new_employee=Employee(
        name=employee.name,
        email=employee.email,
        admin_login=employee.admin_login,
        admin_password=employee.admin_password,
        phone=employee.phone,
        cpf=employee.cpf,
        cep=employee.cep
    )
    db.add(new_employee)
    db.commit()
    return new_employee 

def update_employee_by_id(employee_id: int, employee_data: EmployeeSchema,db: Session):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for field, value in employee_data.dict().items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)
    return employee

def delete_employee_by_id(employee_id: int, db: Session):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return employee

def employee_report(db: Session):
    quantity_employee = db.query(Employee).all()
    relatorio = "-----Employee report-----" + "\nAtualmente existem " +str(len(quantity_employee)) + " funcionarios cadastrados\n\n"
    return relatorio
