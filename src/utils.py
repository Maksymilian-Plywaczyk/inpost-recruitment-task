import csv
import logging
import os
from pathlib import Path
from typing import List, Tuple, Type

import pandas as pd
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from src.db import get_db
from src.models import PC, Laptop, Printer, Product


def insert_data_into_table(
    session: Session, table_name: Type[Laptop | PC | Printer | Product], **kwargs
) -> None:
    """
    Insert data into table from database (Laptop, PC, Printer, Product)
    :param session: Define session
    :param table_name: Table name from database, which will be filled
    :param kwargs: values to insert
    :return: None
    """
    statement = insert(table_name).values(**kwargs)
    session.execute(statement)
    session.commit()


def insert_data_from_csv(
    session: Session, table_name: Type[Laptop | PC | Printer | Product], csv_file: str
) -> None:
    """
    Insert data from csv into database table
    :param session: Define session
    :param table_name: Table name from database, which will be filled
    :param csv_file: CSV file with data
    :return: None
    """
    root_path = Path(__file__).parent.parent
    csv_path = os.path.join(root_path, "csv", csv_file)
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_data_into_table(session, table_name, **row)


def create_csv_with_profitability_ratio(session: Session, filename: str) -> None:
    """
    Create csv file with model name and profitability ratio
    :param session: Define session
    :param filename: Name of filename where data will be stored
    :return: None
    """
    root_path = Path(__file__).parent.parent
    file_path = os.path.join(root_path, "output", filename)
    products = get_all_object_from_product_table(session)

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["model", "ratio"])
        writer.writeheader()
        for product in products:
            data = calculate_profitability_ratio(session, product.model)
            if data is None:
                continue
            writer.writerow(data)


def create_csv_promo_set(
    session: Session,
    products: Tuple[Type[PC | Printer | Laptop], Type[PC | Printer | Laptop]],
    filename: str,
) -> None:
    """
    Create csv files with promo set
    :param session: Define sesion
    :param products: Tuple of products
    :param filename: filename where save resutls
    :return: None
    """
    root_path = Path(__file__).parent.parent
    file_path = os.path.join(root_path, "output", filename)
    data = create_promo_set(session, products)

    first_product_df = pd.DataFrame([data[products[0].__tablename__]])
    second_product_df = pd.DataFrame([data[products[1].__tablename__]])
    promo_price_df = pd.DataFrame([{"promo_price": data["promo_price"]}])

    dataframes_to_add = [first_product_df, second_product_df, promo_price_df]

    with open(file_path, "w", newline="") as csvfile:
        for dataframe in dataframes_to_add:
            dataframe.to_csv(csvfile, index=False)


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
        raise error


def get_one_object_from_table_by_model(
    session: Session, table_name: Type[Laptop | PC | Printer | Product], model: str
) -> Laptop | PC | Printer | None:
    """
    Get one object from given table by model name
    :param session: Define session
    :param table_name: Table name which you would like to search on
    :param model: Model name of object
    :return: Return object by model name or if object is not in table return None
    """
    statement = select(table_name).filter_by(model=model)
    obj = session.scalars(statement).one_or_none()
    return obj


def get_random_object_from_table(
    session: Session, table_name: Type[Laptop | PC | Printer | Product]
) -> Laptop | PC | Printer:
    """
    Get random object from given table
    :param session: Define session
    :param table_name: Table name which you would like search on
    :return:  Return random object
    """
    statement = select(table_name).order_by(func.random())
    obj = session.scalars(statement).first()
    return obj


def get_all_object_from_product_table(session: Session) -> List[Type[Product]]:
    """
    :param session: Define session
    :return: List of products
    """
    return session.query(Product).all()


def calculate_profitability_ratio(session: Session, model: str) -> dict | None:
    """
    Calculate profitability ratio and return results as a dict
    :param session: Define session
    :param model: Model name which you search
    :return: Return dict of result or None if something goes wrong
    """
    product = get_one_object_from_table_by_model(session, Product, model)
    if product is None:
        logging.error("Cannot find product with that model")
        return None
    elif product.type == "Laptop":
        laptop = get_one_object_from_table_by_model(session, Laptop, model)
        return {
            "model": laptop.model,
            "ratio": get_profitability_ratio(
                laptop.ram, laptop.hd, laptop.price, laptop.speed
            ),
        }
    elif product.type == "PC":
        pc = get_one_object_from_table_by_model(session, PC, model)
        return {
            "model": pc.model,
            "ratio": get_profitability_ratio(pc.ram, pc.hd, pc.price, pc.speed),
        }

    else:
        logging.warning("Your product is not PC or Laptop")
        return None


def create_promo_set(
    session: Session,
    promo_set_products: Tuple[Type[Laptop | PC | Printer], Type[PC | Printer | Laptop]],
) -> dict | None:
    """
    Create promo set with products like: (Laptop, PC), (Laptop, Printer)
    :param session: Define session
    :param promo_set_products: Tuple with two elements which are a products of Laptop, PC or Printer
    :return: Dict with products of promo set and promo price of products price sum
    """
    first_product = get_random_object_from_table(session, promo_set_products[0])
    first_product_type = first_product.__tablename__
    second_product = get_random_object_from_table(session, promo_set_products[1])
    second_product_type = second_product.__tablename__
    if first_product is not None and second_product is not None:
        promo_price = round(
            (float(first_product.price) + float(second_product.price)) * 0.9, 2
        )

        promo_set = {
            first_product_type: first_product._asdict(),
            second_product_type: second_product._asdict(),
            "promo_price": promo_price,
        }

        return promo_set
    else:
        logging.error("Cannot create promo set")
        return None
