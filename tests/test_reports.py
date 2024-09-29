from os import path
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from src.reports import spending_by_category, spending_by_weekday, spending_by_workday, log_to_file

path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), "data/operations.csv")


@pytest.fixture
def transacts_for_tests() -> Any:
    """Данные для всех Mock - тестов"""
    transacts_ = pd.DataFrame(
        {
            "Категория": [
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Супермаркеты",
                "Различные товары",
                "Переводы",
                "Переводы",
                "Каршеринг",
                "Каршеринг",
                "Пополнения",
                "Пополнения",
                "Канцтовары",
            ],
            "Дата операции": [
                "31-12-2021 16:44:00",
                "31-12-2021 16:42:04",
                "31-12-2021 16:39:04",
                "31-12-2021 15:44:39",
                "31-12-2021 01:23:42",
                "31-12-2021 00:12:53",
                "30-12-2021 22:22:03",
                "30-12-2021 19:18:22",
                "30-12-2021 19:06:39",
                "30-12-2021 17:50:30",
                "30-12-2021 17:50:17",
                "30-12-2021 14:48:25",
            ],
            "Сумма операции с округлением": [
                "160,89",
                "64,00",
                "118.12",
                "78,06",
                "564,00",
                "800,00",
                "20000,00",
                "7,07",
                "1,32",
                "5046,00",
                "174000,00",
                "349,00",
            ],
        }
    )
    return transacts_


@patch("pandas.DataFrame.to_csv")
def test_spending_by_category(mock: Any, transacts_for_tests: pd.DataFrame) -> Any:
    """Имитация функции spending_by_category"""
    mock.return_value = pd.DataFrame(
        {
            "Сумма операций": [
                160.89,
                64.00,
                118.12,
                78.06,
                564.00,
                800.00,
                20000.00,
                7.07,
                1.32,
                5046.00,
                174000.00,
                349.00,
            ]
        }
    )
    spending_by_category(transacts_for_tests, category="Супермаркеты", choice_date="31 12 2021")
    mock.assert_called_once()


@patch("pandas.DataFrame.to_csv")
def test_spending_by_weekday(mock: Any, transacts_for_tests: pd.DataFrame) -> Any:
    """Имитация функции spending_by_weekday"""
    mock.return_value = pd.DataFrame({"Номер недели": [32], "average_amount": [33233.898333]})
    spending_by_weekday(transacts_for_tests, choice_date="31 12 2021")
    mock.assert_called_once()


@patch("pandas.DataFrame.to_csv")
def test_spending_by_workday(mock: Any, transacts_for_tests: pd.DataFrame) -> Any:
    """Имитация функции spending_by_workday"""
    mock.return_value = pd.DataFrame({"Дни недели": ["Friday", "Friday"], "Средние траты": [36.633333, 3527.250000]})
    spending_by_workday(transacts_for_tests, choice_date="31 12 2021")
    mock.assert_called_once()
