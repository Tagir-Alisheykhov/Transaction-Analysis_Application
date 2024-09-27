# Страница «Главная»
import json
import logging
from os import path
import datetime
import pandas as pd

from src.utils import (user_greeting, cashback_and_cart_numb,
                       top_five_sum_transacts, currency_conversion, data_sp500)

path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), "data/operations.csv")

# Остались логгеры
# Шифруем ключи
#
#


def home_page(file_csv: pd.DataFrame):
    """
    :param
    file_csv: DataFrame csv-файла
    :return:
    """
    file_csv = file_csv.copy()
    file_csv.columns = file_csv.columns.str.strip()
    greeting = user_greeting()
    cards = cashback_and_cart_numb(file_csv)
    top_transacts = top_five_sum_transacts(file_csv)
    currency_rates = currency_conversion()
    stock_prices = data_sp500()
    dict_ = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transacts,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }
    result = json.dumps(dict_, ensure_ascii=False, indent=2)
    return result


if __name__ == '__main__':
    csv_file = pd.read_csv(path_to_xlsx_file)
    print(home_page(csv_file))
