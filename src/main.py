from src.db import create_db_and_tables, is_database_exists
from src.models import PC, Laptop, Printer, Product
from src.utils import (
    create_csv_promo_set,
    create_csv_with_profitability_ratio,
    insert_data_from_csv,
)
import logging


def task_1() -> None:
    create_csv_with_profitability_ratio("ratio.csv")


def task_2() -> None:
    create_csv_promo_set((PC, Printer), "pc_printer.csv")
    create_csv_promo_set((Laptop, Printer), "laptop_printer.csv")


if __name__ == "__main__":
    if not is_database_exists():
        create_db_and_tables()
        insert_data_from_csv(Product, "products.csv")
        insert_data_from_csv(PC, "pcs.csv")
        insert_data_from_csv(Laptop, "laptops.csv")
        insert_data_from_csv(Printer, "printers.csv")
        logging.log("Created database with all tables. Seed table with random data")
    task_1()
    task_2()
