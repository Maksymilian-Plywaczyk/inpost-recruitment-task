import os

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.db import Base
from src.models import Laptop, Printer, Product
from src.utils import (calculate_profitability_ratio, create_promo_set,
                       get_all_object_from_product_table,
                       get_one_object_from_table_by_model,
                       get_profitability_ratio, get_random_object_from_table,
                       insert_data_into_table)


class TestUtils:
    @pytest.fixture(autouse=True)
    def db_session(self):
        engine = create_engine("sqlite:///:memory:")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(engine)
        session = SessionLocal()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        yield session

    @pytest.fixture(autouse=True)
    def product_instance_create(self, db_session):
        data = {"model": "Macbook Pro M2", "type": "Laptop", "maker": "Apple"}
        insert_data_into_table(db_session, Product, **data)

    @pytest.fixture(autouse=True)
    def laptop_instance_create(self, db_session):
        data = {
            "code": 1,
            "model": "Macbook Pro M2",
            "speed": 12312,
            "ram": 16,
            "hd": 111,
            "price": 9999.9,
            "screen": 16,
        }
        insert_data_into_table(db_session, Laptop, **data)

    @pytest.fixture(autouse=True)
    def printer_instance_create(self, db_session):
        data = {
            "code": 1,
            "model": "Fantastic printer",
            "color": "B",
            "type": "super",
            "price": 9999.9,
        }
        insert_data_into_table(db_session, Printer, **data)

    @pytest.mark.parametrize(
        "ram,hd,price,speed", [(1, 2, 3.5, 12), (33333, 12312, 999.99, 11111)]
    )
    def test_get_profitability_ratio_success(
        self, ram: int, hd: int, price: float, speed: int
    ):
        result = get_profitability_ratio(ram, hd, price, speed)
        assert result is not 0

        # assert that result has only 2 decimal places
        assert round(result, 2) == result

    @pytest.mark.parametrize(
        "ram,hd,price,speed", [(1, 2, 0.0, 1231), ("1", 2, 3, 12312)]
    )
    def test_get_profitability_ratio_failed(
        self, ram: int, hd: int, price: float, speed: int
    ):
        with pytest.raises((ZeroDivisionError, TypeError)):
            get_profitability_ratio(ram, hd, price, speed)

    def test_insert_data_into_table(self, db_session):
        data = {"model": "Macbook Pro", "type": "PC", "maker": "Apple"}
        insert_data_into_table(db_session, Product, **data)
        inserted_data = db_session.query(Product).all()
        assert inserted_data

    def test_get_random_object_from_table(self, product_instance_create, db_session):
        obj = get_random_object_from_table(db_session, Product)
        assert obj

    def test_get_one_object_from_table_by_model(
        self, product_instance_create, db_session
    ):
        obj = get_one_object_from_table_by_model(db_session, Product, "Macbook Pro M2")
        assert obj

    def test_get_all_object_from_product_table(self, db_session):
        products = get_all_object_from_product_table(db_session)

        assert len(products) == 1

    def test_calculate_profitability_ratio(self, db_session, laptop_instance_create):
        ratio_data = calculate_profitability_ratio(db_session, "Macbook Pro M2")
        assert ratio_data["model"] == "Macbook Pro M2"

    def test_create_promo_set(
        self, db_session, laptop_instance_create, printer_instance_create
    ):
        promo_set = create_promo_set(db_session, (Laptop, Printer))
        assert "Laptop" in promo_set.keys()
        assert "Printer" in promo_set.keys()
