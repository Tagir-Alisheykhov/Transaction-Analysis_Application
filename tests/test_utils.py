import pytest
import json
import pandas as pd
from os import path
from typing import Any
from unittest.mock import patch

from src.utils import (user_greeting, cashback_and_cart_numb, top_five_sum_transacts,
                       currency_conversion, data_sp500)

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")


@pytest.fixture
def data_with_transacts():
    csv_file = pd.read_csv(path_to_data + "operations.csv")
    csv_file = csv_file.copy()
    return csv_file


def test_user_greeting():
    """Корректность работы функции"""
    assert user_greeting() == "Доброе утро" or "Добрый день" or "Добрый вечер" or "Доброй ночи"


def test_invalid_user_greeting():
    """Проверка на неправильный ответ функции"""
    with pytest.raises(AssertionError):
        assert user_greeting() == "Доброго времени суток"


def test_cashback_and_cart_numb(data_with_transacts):
    """Проверка на корректность работы функции"""
    with open(path_to_data + "data_output_for_tests.json") as file:
        output_js_1 = json.load(file)
    assert cashback_and_cart_numb(data_with_transacts) == output_js_1


def test_invalid_cashback_and_cart_numb():
    """Ошибка при отсутствии обязательной колонки в DataFrame"""
    value_for_error_1 = pd.DataFrame({"No column1": ["No value1, No value1"],
                                      "No column2": ["No value2, No value2"]})
    with pytest.raises(KeyError):
        assert cashback_and_cart_numb(value_for_error_1)


def test_top_five_sum_transacts(data_with_transacts):
    """Проверка корректности работы функции"""
    with open(path_to_data + "data_out_for_tests_2.json", encoding='utf-8') as file:
        output_js_2 = json.load(file)
    assert top_five_sum_transacts(data_with_transacts) == output_js_2


def test_invalid_top_five_sum_transacts():
    """Ошибка при отсутствии обязательной колонки в DataFrame"""
    value_for_error_2 = pd.DataFrame({"No column1": ["No value1, No value1"],
                                      "No column2": ["No value2, No value2"]})
    with pytest.raises(KeyError):
        assert top_five_sum_transacts(value_for_error_2)


@patch("requests.get")
def test_currency_conversion(mock_get: Any) -> Any:
    """Имитация запроса на конвертацию валюты"""
    mock_get.return_value.json.return_value = {"result": 25.555}
    assert currency_conversion() == [{'currency': 'USD', 'rate': 25.55}]
    mock_get.assert_called_once()


@patch("requests.get")
def test_data_sp500(mock_get: Any) -> Any:
    """Имитация запроса данных для компаний SP&500"""
    mock_get.return_value.json.return_value = {"values": [{"open": 11.111}, {"open": 22.222}]}
    assert data_sp500() == [
        {"stock": "AAPL", "price": 11.11},
        {"stock": "AMZN", "price": 11.11},
        {"stock": "GOOGL", "price": 11.11},
        {"stock": "MSFT", "price": 11.11},
        {"stock": "TSLA", "price": 11.11},
    ]
    mock_get.assert_called()










