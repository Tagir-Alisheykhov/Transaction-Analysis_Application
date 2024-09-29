import json
import pytest
import pandas as pd
from os import path

from src.services import simple_search

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")


@pytest.fixture
def data_with_transacts() -> pd.DataFrame:
    """Файл с транзакциями в формате DataFrame"""
    csv_file = pd.read_csv(path_to_data + "operations.csv")
    csv_file = csv_file.copy()
    return csv_file


def test_simple_search_no_example(data_with_transacts):
    """Проверка на отсутствие результата"""
    assert simple_search(data_with_transacts, "Abrakadabra") == "[]"


def test_simple_search(data_with_transacts):
    """Проверка корректности работы функции simple_search"""
    with open(path_to_data + "data_out_for_tests_3.json") as file:
        res = json.load(file)
    assert simple_search(data_with_transacts, "ИКЕА") == res


def test_invalid_simple_search():
    """Ошибка при отсутствии обязательной колонки в DataFrame"""
    value_for_error_1 = pd.DataFrame({"No column1": ["No value1, No value1"],
                                      "No column2": ["No value2, No value2"]})
    with pytest.raises(KeyError):
        assert simple_search(value_for_error_1, "Переводы")

