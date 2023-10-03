from database import Base
from typing import Optional, List
from sqlalchemy import String, Boolean, Integer, Column, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime


class Client(Base):
    __tablename__ = 'client'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String[12], nullable=False, unique=True) 
    cpf: Mapped[str] = mapped_column(String[11], nullable=False, unique=True)
    cep: Mapped[str] = mapped_column(String[8], nullable=False, unique=False)
    
    sales = relationship("Sale", back_populates="client")
    
    
class Employee(Base):
    __tablename__ = 'employee'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(55), nullable=False)
    email: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    admin_login: Mapped[str] = mapped_column(String[55], nullable=False, unique=True)
    admin_password: Mapped[str] = mapped_column(String[55], nullable=False, unique=False)
    phone: Mapped[str] = mapped_column(String[12], nullable=False, unique=True) 
    cpf: Mapped[str] = mapped_column(String[11], nullable=False, unique=True)
    cep: Mapped[str] = mapped_column(String[8], nullable=False, unique=False)
    
    sales = relationship("Sale", back_populates="employee")
    
class Product(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    price_cost: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity_max: Mapped[int] = mapped_column(Integer, nullable=False)
    
    sales = relationship("Sale", back_populates="product")
    
class Sale(Base):
    __tablename__ = 'sale'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey('client.id'), nullable=False)
    employee_id: Mapped[int] = mapped_column(Integer, ForeignKey('employee.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('product.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


    client = relationship("Client", back_populates="sales")
    employee = relationship("Employee", back_populates="sales")
    product = relationship("Product", back_populates="sales")  