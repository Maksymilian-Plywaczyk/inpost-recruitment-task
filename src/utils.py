from typing import Type, Tuple, List
from src.models import Product, Laptop, PC, Printer
from src.db import get_db
import csv
import os
from pathlib import Path
from sqlalchemy import select, insert
from sqlalchemy.sql import func
import logging


def insert_data_into_table(
    table_name: Type[Laptop | PC | Printer | Product], **kwargs
) -> None:
    """
    Insert data into table from database (Laptop, PC, Printer, Product)
    :param table_name: Table name from database, which will be filled
    :param kwargs: values to insert
    :return: None
    """
    statement = insert(table_name).values(**kwargs)
    with get_db() as session:
        session.execute(statement)
        session.commit()


def insert_data_from_csv(
    table_name: Type[Laptop | PC | Printer], csv_file: str
) -> None:
    """
    Insert data from csv into database table
    :param table_name: Table name from database, which will be filled
    :param csv_file: CSV file with data
    :return: None
    """
    root_path = Path(__file__).parent.parent
    csv_path = os.path.join(root_path, "csv", csv_file)
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_data_into_table(table_name, **row)


def create_csv_with_profitability_ratio(filename: str) -> None:
    """
    Create csv file with model name and profitability ratio
    :param filename: Name of filename where data will be stored
    :return: None
    """
    root_path = Path(__file__).parent.parent
    filename_path = os.path.join(root_path, "output", filename)
    products = get_all_object_from_product_table()

    with open(filename_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["model", "ratio"])
        writer.writeheader()
        for product in products:
            data = calculate_profitability_ratio(product.model)
            if data is None:
                continue
            writer.writerow(data)


def get_profitability_ratio(ram: int, hd: int, price: float, speed: int) -> float:
    """
    Function with return profitability ratio of product, if something goes wrong return 0.0
    :param ram: ram of product
    :param hd:  hd of product
    :param price: price of product
    :param speed: speed of product
    :return: If correct return calculated ratio or 0.0 if something goes wrong
    """
    try:
        ratio = ((ram + hd) / price) * speed
        rounded_ratio = round(ratio, 2)
        return rounded_ratio
    except (ZeroDivisionError, TypeError) as error:
        logging.error(f"Cannot get profitability ratio, error info: {error}")
        return 0.0


def get_one_object_from_table_by_model(
    table_name: Type[Laptop | PC | Printer], model: str
) -> Laptop | PC | Printer | None:
    """
    Get one object from given table by model name
    :param table_name: Table name which you would like to search on
    :param model: Model name of object
    :return: Return object by model name or if object is not in table return None
    """
    statement = select(table_name).filter_by(model=model)
    with get_db() as session:
        obj = session.scalars(statement).one_or_none()
    return obj


def get_random_object_from_table(
    table_name: Type[Laptop | PC | Printer]
) -> Laptop | PC | Printer:
    """
    Get random object from given table
    :param table_name: Table name which you would like search on
    :return:  Return random object
    """
    statement = select(table_name).order_by(func.random())
    with get_db() as session:
        obj = session.scalars(statement).first()

    return obj


def get_all_object_from_product_table() -> List[Type[Product]]:
    with get_db() as session:
        return session.query(Product).all()


def calculate_profitability_ratio(model: str) -> dict | None:
    """
    Calculate profitability ratio and return results as a dict
    :param model: Model name which you search
    :return: Return dict of result or None if something goes wrong
    """
    product = get_one_object_from_table_by_model(Product, model)
    if product is None:
        logging.error("Cannot find product with that model")
        return None
    elif product.type == "Laptop":
        laptop = get_one_object_from_table_by_model(Laptop, model)
        return {
            "model": laptop.model,
            "ratio": get_profitability_ratio(
                laptop.ram, laptop.hd, laptop.price, laptop.speed
            ),
        }
    elif product.type == "PC":
        pc = get_one_object_from_table_by_model(PC, model)
        return {
            "model": pc.model,
            "ratio": get_profitability_ratio(pc.ram, pc.hd, pc.price, pc.speed),
        }

    else:
        logging.warning("Your product is not PC or Laptop")
        return None


def create_promo_set(
    promo_set_products: Tuple[Type[Laptop | PC | Printer]]
) -> dict | None:
    """
    Create promo set with products like: (Laptop, PC), (Laptop, Printer)
    :param promo_set_products: Tuple with two elements which are a products of Laptop, PC or Printer
    :return: Dict with products of promo set and promo price of products price sum
    """
    first_product = get_random_object_from_table(promo_set_products[0])
    second_product = get_random_object_from_table(promo_set_products[1])
    if first_product is not None and second_product is not None:
        promo_price = (first_product.price + second_product.price) * 0.9

        promo_set = {
            "first_product": first_product.__dict__,
            "second_product": second_product.__dict__,
            "promo_price": promo_price,
        }

        return promo_set
    else:
        logging.error("Cannot create promo set")
        return None
