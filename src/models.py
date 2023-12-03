from sqlalchemy import CHAR, DECIMAL, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator

from src.db import Base


class Money(TypeDecorator):
    # Create custom type of money, which have only two decimal places
    impl = DECIMAL(precision=10, scale=2)

    cache_ok = True


class Product(Base):
    # Define table name
    __tablename__ = "Product"

    # Define table columns with types
    maker = Column(String(10), nullable=False)
    model = Column(String(50), primary_key=True)
    type = Column(String(50))


class Laptop(Base):
    # Define table name
    __tablename__ = "Laptop"

    # Define table columns with types
    code = Column(Integer, primary_key=True)
    model = Column(String(50), ForeignKey("Product.model"), nullable=False)
    speed = Column(Integer)
    ram = Column(Integer)
    hd = Column(Integer)
    price = Column(Money)
    screen = Column(Integer)

    # Define the relationship with the Product table
    product = relationship("Product", backref="laptops")


class PC(Base):
    # Define table name
    __tablename__ = "PC"

    # Define table columns with types
    code = Column(Integer, primary_key=True)
    model = Column(String(50), ForeignKey("Product.model"), nullable=False)
    speed = Column(Integer)
    ram = Column(Integer)
    hd = Column(Integer)
    cd = Column(Integer)
    price = Column(Money)

    # Define the relationship with the Product table
    product = relationship("Product", backref="pcs")


class Printer(Base):
    # Define table name
    __tablename__ = "Printer"

    # Define table columns with types
    code = Column(Integer, primary_key=True)
    model = Column(String(50), ForeignKey("Product.model"), nullable=False)
    color = Column(CHAR(1))
    type = Column(String(10))
    price = Column(Money)

    # Define the relationship with the Product table
    product = relationship("Product", backref="printers")
