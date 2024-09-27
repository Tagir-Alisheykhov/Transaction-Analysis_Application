# Страница «Главная»
import json
import logging
from os import path
import datetime
import pandas as pd

from src.utils import (user_greeting, cashback_and_cart_numb,
                       top_five_sum_transacts, currency_conversion, data_sp500)

path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), "data/operations.csv")


def home_page(file_csv: pd.DataFrame):
    """
    :param
    file_csv: DataFrame csv-файла
    :return:
    """
    file_csv = file_csv.copy()
    file_csv.columns = file_csv.columns.str.strip()
    greeting = user_greeting(file_csv)
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
    print(json.dumps(dict_, ensure_ascii=False, indent=2))



    # csv_date = pd.to_datetime(csv['Дата операции'], dayfirst=True)  # Вопрос. Что делает dayfirst?
    # date_conversion = list(map(lambda x: str(x), csv_date))  # Возможно эта строка не нужна вовсе
    # # return date_conversion


if __name__ == '__main__':
    csv_file = pd.read_csv(path_to_xlsx_file)

    print(home_page(csv_file))





# Реализуйте набор функций и главную функцию, принимающую на вход строку с датой и временем в формате
# YYYY-MM-DD HH:MM:SS
#  и возвращающую JSON-ответ со следующими данными:
# 1
# Приветствие в формате
# "???"
# , где
# ???
#  — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
# в зависимости от текущего времени.
# 2
# По каждой карте:
# последние 4 цифры карты;
# общая сумма расходов;
# кешбэк (1 рубль на каждые 100 рублей).
# 3
# Топ-5 транзакций по сумме платежа.
# Курс валют.
# Стоимость акций из S&P500.


# МОЙ КОММЕНТАРИЙ:
# - Сначала реализуем первую функцию (views.py)
# json requests API datetime logging pytest pandas
# - Потом реализуем вывод JSON с обработанными данными (utils.py)
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# json
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют API.
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# datetime
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# logging
# .
# Вспомогательные функции, необходимые для работы функции страницы «Главная», используют библиотеку
# pandas
# .