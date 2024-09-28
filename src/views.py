import json
import logging
import pandas as pd
from os import path

from src.utils import (user_greeting, cashback_and_cart_numb,
                       top_five_sum_transacts, currency_conversion, data_sp500)

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")
path_to_logs = path.join(path.dirname(path.dirname(__file__)), "logs/")
path_to_xlsx_file = path_to_data + "operations.csv"

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(path_to_logs + "views.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def home_page(file_csv: pd.DataFrame) -> str:
    """
    Функция группирует отформатированные данные после
    обращения к
    функциям из модуля 'src/utils.py'
    :param
    file_csv: DataFrame csv-файла
    :return:
    json-file: Отфильтрованные данные
    """
    logger.debug("Начало работы функции home_page")
    logger.debug("Создание копии входных данных")
    file_csv = file_csv.copy()
    logger.debug("Удаление лишних пробелов")
    file_csv.columns = file_csv.columns.str.strip()
    logger.debug("Вызываем функцию 'user_greeting()'")
    greeting = user_greeting()
    logger.debug("Вызываем функцию 'cashback_and_cart_numb()'")
    cards = cashback_and_cart_numb(file_csv)
    logger.debug("Вызываем функцию 'top_five_sum_transacts()'")
    top_transacts = top_five_sum_transacts(file_csv)
    logger.debug("Вызываем функцию 'currency_conversion()'")
    currency_rates = currency_conversion()
    logger.debug("Вызываем функцию 'data_sp500()'")
    stock_prices = data_sp500()
    logger.debug("Группировка полученных данных")
    dict_ = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transacts,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    result = json.dumps(dict_, ensure_ascii=False, indent=2)
    logger.debug("Конец работы функции home_page")
    return result


if __name__ == '__main__':
    logger.debug("Чтение данных из csv файла")
    csv_file = pd.read_csv(path_to_xlsx_file)
    logger.debug("Вывод результата работы функции home_page")
    print(home_page(csv_file))
