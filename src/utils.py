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


def user_greeting() -> str:
    """
    Приветствие пользователя в зависимости от времени суток
    :return:
    """
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
    :param file_df:
    :return:
    """
    file = file_df.copy()
    check_column_1 = file.columns == "Сумма операции с округлением"
    check_column_2 = file.columns == "Номер карты"
    if True not in check_column_1 and True not in check_column_2:
        raise KeyError("Нет обязательного ключа")
    else:
        cart_list = []
        sums_by_card = {}
        file.loc[:, "Сумма операции с округлением"] = [
            (float(sum_operation.replace(",", ".")))
            for sum_operation in file["Сумма операции с округлением"]
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
    """
    :param file_df:
    :return:
    """
    file_csv = file_df.copy()
    file_csv = file_csv.fillna("Unknown")
    formatted_top_transacts = []
    check_column_1 = file_csv.columns == "Сумма операции с округлением"
    check_column_2 = file_csv.columns == "Дата платежа"
    check_column_3 = file_csv.columns == "Категория"
    check_column_4 = file_csv.columns == "Описание"
    if (True not in check_column_1
            and True not in check_column_2
            and True not in check_column_3
            and True not in check_column_4):
        raise KeyError("Нет обязательного ключа")
    else:
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
        # скорость получения данных по подписке сервиса, а затем ставим "break"
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
