import datetime
import json
import logging
import os
from os import path

import pandas as pd
import requests
from dotenv import load_dotenv

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")
path_to_logs = path.join(path.dirname(path.dirname(__file__)), "logs/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(path_to_logs + "utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

load_dotenv()
logger.debug("Получение ключей доступа для внешних API")
API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_SP500 = os.getenv("API_KEY_SP500")


def user_greeting() -> str:
    """
    Приветствие пользователя в зависимости от времени суток.
    :return
    string: Строка приветствия
    """
    logger.debug("\nЗапуск функции user_greeting")
    logger.debug("Получаем текущую дату и время")
    date_now = datetime.datetime.now()
    logger.debug("Форматируем полученную дату и время")
    date_without_second = date_now.replace(microsecond=0)
    logger.debug("Выполнение блока условий для определения времени суток")
    if 12 > date_without_second.hour > 6:
        logger.debug("Вывод результата и конец работы функции user_greeting")
        return "Доброе утро"
    elif 18 > date_without_second.hour >= 12:
        logger.debug("Вывод результата и конец работы функции user_greeting")
        return "Добрый день"
    elif 24 > date_without_second.hour >= 18:
        logger.debug("Вывод результата и конец работы функции user_greeting")
        return "Добрый вечер"
    else:
        logger.debug("Вывод результата и конец работы функции user_greeting")
        return "Доброй ночи"


def cashback_and_cart_numb(file_df: pd.DataFrame) -> list[dict]:
    """
    Функция обрабатывает DataFrame для получения данных по каждой карте:
    номера карты, суммы карте с транзакций за весь период, кеш-бек.
    :param
    file_df: со всеми транзакциями
    :return:
    Список словарей, где каждый словарь - это одна транзакция с данными
    """
    logger.debug("\nЗапуск функции cashback_and_cart_numb")
    cart_list = []
    sums_by_card = {}
    logger.debug("Копируем полученные данные")
    file = file_df.copy()
    logger.debug("Проверка наличия обязательных колонок в DataFrame")
    check_column_1 = file.columns == "Сумма операции с округлением"
    check_column_2 = file.columns == "Номер карты"
    if True not in check_column_1 and True not in check_column_2:
        logger.error("В полученном файле DataFrame отсутствуют обязательная колонка")
        raise KeyError("Required key missing")
    else:
        logger.debug("Меняем формат числовых данных - сумм операций")
        file.loc[:, "Сумма операции с округлением"] = [
            (float(sum_operation.replace(",", "."))) for sum_operation in file["Сумма операции с округлением"]
        ]
        logger.debug("Обработка NaN значений в столбце 'Номер карты'")
        file.loc[:, "Номер карты"] = file.loc[:, "Номер карты"].fillna("No numb")
        logger.debug("Создаем список уникальных номеров карт по всем транзакциям")
        list_unique_cart_number = file["Номер карты"].unique()
        logger.debug("Запуск цикла суммирования транзакций по каждому номеру карты")
        for unique_cart_number in list_unique_cart_number:
            logger.debug(f"Итерация по номеру карты: {unique_cart_number}")
            total_spent = file[file["Номер карты"] == unique_cart_number]["Сумма операции с округлением"].sum()
            logger.debug("Запись номера карты и суммы транзакций в словарь")
            sums_by_card[unique_cart_number] = round(total_spent, 2)
        logger.debug("Запуск цикла форматирования данных для вывода")
        for card, total in sums_by_card.items():
            logger.debug(f"Итерация по номеру карты: {card}")
            cashback = total // 100
            cart_list.append({"last_digits": card, "total_spent": total, "cashback": cashback})
        logger.debug("Вывод результата")
        logger.debug("Конец работы функции cashback_and_cart_numb")
        return cart_list


def top_five_sum_transacts(file_df: pd.DataFrame) -> list[dict]:
    """
    Функция обрабатывает DataFrame для получения топ-5 транзакций по
    сумме операции.
    :param
    file_df: со всеми транзакциями
    :return:
    Список словарей, где каждый словарь - это одна транзакция с данными
    """
    logger.debug("\nЗапуск функции top_five_sum_transacts")
    formatted_top_transacts = []
    logger.debug("Копируем полученные данные")
    file_csv = file_df.copy()
    logger.debug("Обработка NaN значений")
    file_csv = file_csv.fillna("Unknown")
    logger.debug("Проверка наличия обязательных колонок в DataFrame")
    check_column_1 = file_csv.columns == "Сумма операции с округлением"
    check_column_2 = file_csv.columns == "Дата платежа"
    check_column_3 = file_csv.columns == "Категория"
    check_column_4 = file_csv.columns == "Описание"
    if (
        True not in check_column_1
        and True not in check_column_2
        and True not in check_column_3
        and True not in check_column_4
    ):
        logger.error("В полученном файле DataFrame отсутствуют обязательная колонка")
        raise KeyError("Нет обязательного ключа")
    else:
        logger.debug("Меняем формат числовых данных - сумм операций")
        file_csv.loc[:, "Сумма операции с округлением"] = [
            (float(sum_operation.replace(",", "."))) for sum_operation in file_csv["Сумма операции с округлением"]
        ]
        logger.debug("Преобразование аргументов в числовой тип")
        file_csv["Сумма операции с округлением"] = pd.to_numeric(
            file_csv["Сумма операции с округлением"], errors="coerce"
        )
        logger.debug("Определение топ-5 транзакций")
        top_5_transacts = file_csv.nlargest(5, "Сумма операции с округлением")
        logger.debug("Запуск цикла для группировки данных в словарь")
        for idx, transact in top_5_transacts.iterrows():
            logger.debug(f"Индекс итерируемой транзакции {idx}")
            dict_ = {
                "date": transact["Дата платежа"],
                "amount": transact["Сумма операции с округлением"],
                "category": transact["Категория"],
                "description": transact["Описание"],
            }
            logger.debug("Запись данных словарей список")
            formatted_top_transacts.append(dict_)
        logger.debug("Вывод результата")
        logger.debug("Конец работы функции top_five_sum_transacts")
        return formatted_top_transacts


def currency_conversion() -> list[dict]:
    """
    - Функция для получения актуальных данных по курсу валют из внешнего API.
    - Валюты, которые необходимо конвертировать берутся из файла
    расположенного в данном проекте: '/data/user_settings.json'
    - Сервис предоставляющий данные: https://currencylayer.com/
    :return
    - Список словарей, где в каждом словаре - название валюты и актуальный курс
    """
    logger.debug("\nЗапуск функции currency_conversion")
    converse_currencies = []
    logger.debug("Получение названий валют для конвертации")
    with open(path_to_data + "user_settings.json") as file:
        js_file_with_currencies = json.load(file)
    logger.debug("Запуск цикла для обращения к API")
    for currency in js_file_with_currencies["user_currencies"]:
        # Установлен 'break' в конце цикла для уменьшения
        # количества валют до 1, т.к. мы превышаем
        # скорость получения данных по подписке сервиса.
        logger.debug(f"Обращение к API для валюты: {currency}")
        response = requests.get(
            f"http://api.currencylayer.com/convert?"
            f"access_key={API_KEY_CURRENCY}&"
            f"from={currency}&"
            f"to=RUB"
            f"&amount=1"
        )
        logger.debug("Вывод данных в формате json")
        rate = response.json()["result"]
        logger.debug("Запись данных по валюте в словарь")
        dict_ = {"currency": currency, "rate": round(rate, 2)}
        logger.debug("Передача словаря с данными в список")
        converse_currencies.append(dict_)
        break
    logger.debug("Вывод результата")
    logger.debug("Конец работы функции currency_conversion")
    return converse_currencies


def data_sp500() -> list[dict]:
    """
    - Функция для получения актуальных данных по акциям SP&500 из внешнего API.
    - Название акций, цены которые необходимо получить, берутся из файла
    расположенного в данном проекте: '/data/user_settings.json'
    - Сервис предоставляющий API: twelvedata.com
    - Адрес: https://twelvedata.com/account/manage-plan
    """
    logger.debug("\nЗапуск функции data_sp500")
    stock_prices = []
    logger.debug("Получение названий компаний")
    with open(path_to_data + "user_settings.json") as file:
        js_file_with_currencies = json.load(file)
    logger.debug("Запуск цикла для обращения к API")
    for stock in js_file_with_currencies["user_stocks"]:
        logger.debug(f"Обращение к API для акции: {stock}")
        response = requests.get(
            f"https://api.twelvedata.com/time_series?"
            f"apikey={API_KEY_SP500}"
            f"&symbol={stock}&"
            f"interval=1min&"
            f"format=JSON"
        )
        logger.debug("Вывод данных в формате json")
        price = response.json()["values"][0]["open"]
        logger.debug("Запись данных об акции в словарь")
        dict_ = {"stock": stock, "price": round(float(price), 2)}
        logger.debug("Передача словаря с данными в список")
        stock_prices.append(dict_)
    logger.debug("Вывод результата")
    logger.debug("Конец работы функции data_sp500")
    return stock_prices
