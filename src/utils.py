import json
import logging
from os import path
import pandas as pd
import datetime
import requests

API_KEY_CURRENCY_1 = "a7121c2b37d9593d2f34219401e63e50"
API_KEY_CURRENCY = "fca_live_IMOWBSuqWt4WwoknvjNvX4YpszDU6s5nInJsjVbT"  # Для курса валют
API_KEY_SP500 = "0a11003114bb4f08a0b2497302068255"

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")
csv_file = pd.read_csv(path_to_data + "operations.csv")


def user_greeting(file_df: pd.DataFrame) -> str:
    """ Приветствие пользователя в зависимости от времени суток """
    date_now = datetime.datetime.now()
    date_without_second = date_now.replace(microsecond=0)
    if 12 > date_without_second.hour > 6:
        return "Доброе утро"
    elif 18 > date_without_second.hour >= 12:
        return "Добрый день"
    elif 24 > date_without_second.hour >= 18:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def cashback_and_cart_numb(file_df: pd.DataFrame):
    """
    :return:
    """
    file = csv_file.copy()
    cart_list = []
    sums_by_card = {}
    file.loc[:, "Сумма операции с округлением"] = [
        (float(sum_operation.replace(",", "."))) for sum_operation in file["Сумма операции с округлением"]
    ]
    file.loc[:, "Номер карты"] = file.loc[:, "Номер карты"].fillna("No numb")
    list_unique_cart_number = file["Номер карты"].unique()
    for unique_cart_number in list_unique_cart_number:
        total_spent = file[file["Номер карты"] ==
                           unique_cart_number]["Сумма операции с округлением"].sum()
        sums_by_card[unique_cart_number] = round(total_spent, 2)
    for card, total in sums_by_card.items():
        cashback = total // 100
        cart_list.append({
            "last_digits": card,
            "total_spent": total,
            "cashback": cashback
        })
    return cart_list


def top_five_sum_transacts(file_df: pd.DataFrame):
    """"""
    formatted_top_transacts = []
    file_csv = csv_file.copy()
    file_csv.loc[:, "Сумма операции с округлением"] = [
        (float(sum_operation.replace(",", ".")))
        for sum_operation in file_csv["Сумма операции с округлением"]
    ]
    file_csv["Сумма операции с округлением"] = (
        pd.to_numeric(file_csv["Сумма операции с округлением"], errors='coerce'))
    top_5_transacts = file_csv.nlargest(5, "Сумма операции с округлением")
    for idx, transact in top_5_transacts.iterrows():
        dict_ = {
            "date": transact["Дата платежа"],
            "amount": transact["Сумма операции с округлением"],
            "category": transact["Категория"],
            "description": transact["Описание"]
        }
        formatted_top_transacts.append(dict_)
    return formatted_top_transacts


def currency_conversion():
    """
    Сервис предоставляющий данные: https://currencylayer.com/
    :return:
    """
    converse_currencies = []
    with open(path_to_data + "user_settings.json") as file:
        js_file_with_currencies = json.load(file)
    for currency in js_file_with_currencies["user_currencies"]:
        # Уменьшаем количество валют до 1, т.к. мы превышаем
        # скорость получения данных по подписке сервиса и ставим "break"
        currency = "USD"
        response = requests.get(f"http://api.currencylayer.com/convert?"
                                f"access_key={API_KEY_CURRENCY_1}&"
                                f"from={currency}&"
                                f"to=RUB"
                                f"&amount=1")
        rate = response.json()["result"]
        dict_ = {
            "currency": currency,
            "rate": round(rate, 2)
        }
        converse_currencies.append(dict_)
        break
    return converse_currencies


def data_sp500():
    """
    Сервис предоставляющий API: twelvedata.com
    https://twelvedata.com/account/manage-plan
    """
    stock_prices = []
    with open(path_to_data + "user_settings.json") as file:
        js_file_with_currencies = json.load(file)
    for stock in js_file_with_currencies["user_stocks"]:
        response = requests.get(f"https://api.twelvedata.com/time_series?"
                                f"apikey={API_KEY_SP500}"
                                f"&symbol={stock}&"
                                f"interval=1min&"
                                f"format=JSON")
        price = response.json()["values"][0]["open"]
        dict_ = {
            "stock": stock,
            "price": round(float(price), 2)
        }
        stock_prices.append(dict_)
    return stock_prices


# if __name__ == '__main__':
    # print(user_greeting()

    # print(cashback_and_cart_numb())

    # print(top_five_sum_transacts())

    # print(currency_conversion())

    # print(data_sp500())


    # ll = [{"A": "AAA", "B": "BBB", "C": [{"1": 11111, "2": 2222, "3": 3333, "4": 4444}, {"1": 11111, "2": 2222, "3": 3333, "4": 4444}]}]
    #
    # for i in ll:
    #     print(i["C"][0]["2"])




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
