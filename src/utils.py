import json

# from src.views import home_page
from os import path
import pandas as pd
import datetime
import freecurrencyapi
import requests


API_KEY_CURRENCY = "fca_live_IMOWBSuqWt4WwoknvjNvX4YpszDU6s5nInJsjVbT"  # Для курса валют
API_KEY_SP500 = "0a11003114bb4f08a0b2497302068255"

path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), "data/operations.csv")
csv_file = pd.read_csv(path_to_xlsx_file)


def user_greeting() -> str:
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


def cashback_and_cart_numb():
    """
    :return:
    """
    file = csv_file.copy()

    cart_list = []
    sums_by_card = {}

    # Сумма всех расходов (НУЖНО СДЕЛАТЬ ЗА ОДИН МЕСЯЦ Если дата — 20.05.2020,
    # то данные для анализа будут в диапазоне 01.05.2020-20.05.2020)
    # ВИДИМО НУЖНО ДОБАВИТЬ ОПЦИОНАЛЬНОЕ ЗНАЧЕНИЕ

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


def top_five():
    """"""
    file_csv = csv_file.copy()
    file_csv.loc[:, "Сумма операции с округлением"] = [
        (float(sum_operation.replace(",", "."))) for sum_operation in file_csv["Сумма операции с округлением"]
    ]
    sorted_file = file_csv.sort_values(by="Сумма операции с округлением", ascending=False)
    # print(sorted_file["Сумма операции с округлением"].head())


def currency_conversion():
    """
    Запрос актуальных курсов валют.
    - Сервис предоставляющий API: https://app.freecurrencyapi.com/dashboard
    - Документация для запросов по адресу: https://github.com/everapihq/freecurrencyapi-python?tab=readme-ov-file
    - Для вывода количества доступных запросов:
        1 - poetry add freecurrencyapi - Скачиваем библиотеку, которую предоставляет сервис
        2 - import freecurrencyapi (Импортируем библиотеку в необходимый модуль)
        3 - client = freecurrencyapi.Client(API_KEY) - Вставляем персональный API-ключ
        4 - print(client.status()) - Вывод данных в консоль
    """
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY_CURRENCY}"
    response = requests.get(url)
    return response.json()


def data_sp500():
    """
    Сервис предоставляющий API: twelvedata.com
    https://twelvedata.com/account/manage-plan
    """
    symbol = ""  # Здесь нужно задать необходимые акции, которые нужны пользователю и вставть переменную в ссылку/ Можно передавать их в самцу функцию по очереди
    url = (f"https://api.twelvedata.com/time_series?apikey={API_KEY_SP500}"
           f"&symbol=SPX&interval=1min&format=JSON")
    response = requests.get(url)
    print(response.status_code)
    for _dict in response.json()["values"]:
        for key, price in _dict.items():
            if key == "open":
                return price  # 5718.02979


if __name__ == '__main__':
    # print(user_greeting()

    print(cashback_and_cart_numb())

    # print(top_five())

    # print(currency_conversion())

    # print(data_sp500())





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
