from src.utils import insert_data_from_csv
from src.models import Product, PC, Laptop, Printer
from src.db import create_db_and_tables
from src.utils import create_csv_with_profitability_ratio

# create_db_and_tables()
# insert_data_from_csv(Product, 'products.csv')
# insert_data_from_csv(PC, "pcs.csv")
# insert_data_from_csv(Laptop, "laptops.csv")
# insert_data_from_csv(Printer, "printers.csv")

create_csv_with_profitability_ratio("ratio.csv")
