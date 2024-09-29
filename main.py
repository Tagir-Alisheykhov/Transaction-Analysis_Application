import logging
import pandas as pd
from os import path
from typing import Any

from src.services import simple_search
from src.views import home_page
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday

path_to_data = path.join(path.dirname(__file__), "data/")
path_to_logs = path.join(path.dirname(__file__), "logs/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(path_to_logs + "main.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_data_from_services(data: pd.DataFrame) -> Any:
    """Получение данных для страницы Сервисы"""
    logger.info("Введите ключевое слово/слова для поиска транзакций")
    choice_key_word = input("Простой поиск: ")
    logger.debug("Вызов функции simple_search()")
    res = simple_search(data, choice_key_word)
    logger.debug("Вывод результата работы функции get_data_from_services")
    return res


def get_data_from_views(data: pd.DataFrame) -> Any:
    """Получение данных для страницы Главная"""
    logger.debug("Вызов функции home_page()")
    res = home_page(data)
    logger.debug("Вывод результата работы функции get_data_from_views")
    return res


def get_data_from_reports(data: pd.DataFrame, category: str, choice_date: str) -> Any:
    """Форматирование и создание отформатированных csv-файлов с Отчетами"""
    logger.debug("Вызов функций spending_by_category")
    func_1 = spending_by_category(data, category, choice_date)
    logger.debug("Вызов функций spending_by_weekday")
    func_2 = spending_by_weekday(data, choice_date)
    logger.debug("Вызов функций spending_by_workday")
    func_3 = spending_by_workday(data, choice_date)
    return func_1, func_2, func_3


if __name__ == "__main__":
    logger.debug("Форматируем файл csv в DataFrame")
    file_transacts = pd.read_csv(path_to_data + "operations.csv")

    logger.info("\nЗапуск программы для получения данных из сервисов")
    print(get_data_from_services(file_transacts))
    logger.debug("Конец работы программы для получения данных из сервисов")

    logger.info("\nЗапуск программы для получения данных для страницы Главная")
    print(get_data_from_views(file_transacts))
    logger.debug("Конец работы программы для получения данных для страницы Главная")

    logger.info("\nЗапуск программы для создания отсчетов по транзакциям в формате .csv")
    cycle_true = True
    choice_category = ""
    logger.debug("Запуск цикла проверки ввода категории")
    while cycle_true:
        names_category = file_transacts.loc[:, "Категория"]
        user_choice_category = input("Введите необходимую категорию транзакций: \n").strip()
        if user_choice_category in names_category.values:
            choice_category = user_choice_category
            cycle_true = False
        else:
            logger.warning("\nТакой категории не существует\n")
    logger.debug("Ввод названия категории пользователем")
    date_choice = input("Введите дату через пробел в формате 'ДД_ММ_ГГГГ': ")
    reports = get_data_from_reports(file_transacts, choice_category, date_choice)
    logger.info("Файлы с отчётами успешно созданы")
    logger.info("\nКонец работы программы для создания отсчетов по транзакциям в формате .csv")
