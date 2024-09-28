import json
import logging
from os import path
import pandas as pd

path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")
path_to_logs = path.join(path.dirname(path.dirname(__file__)), "logs/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler(path_to_logs + "services.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(file_formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def simple_search(file_csv: pd.DataFrame, choice_word: str) -> str:
    """
    - Функция выполняет простой поиск в DataFrame
    по столбцам с названиями: 'Категория' и 'Описание'.
    :param-1
    file_csv: Транзакции в формате DataFrame
    :param-2
    choice_word: Ключевое слово (слово, подстрока или фраза),
    которое ввел пользователь
    :return:
    - Запись данных в файл, в формате json
    - Вывод результата работы функции в консоль
    """
    logger.debug("\nЗапуск функции simple_search")
    logger.debug("Копируем файл с транзакциями")
    file_csv = file_csv.copy()
    logger.debug("Удаляем лишние пробелы с названий колонок")
    file_csv.columns.str.strip()
    logger.debug("Генерируем имя файла для чтения данных")
    gen_filename = path_to_data + "file_by_simple_search.json"
    logger.debug("Поиск совпадений введенного значения в DataFrame")
    check_column_1 = file_csv.columns == "Категория"
    check_column_2 = file_csv.columns == "Описание"
    if True not in check_column_1 and True not in check_column_2:
        raise KeyError("Нет обязательного ключа")
    filter_by_key = file_csv[
        (file_csv["Категория"].str.contains(choice_word, na=False, case=False)) |
        (file_csv["Описание"].str.contains(choice_word, na=False, case=False))
    ]
    logger.debug("Запись отфильтрованных данных в файл")
    filter_by_key.to_json(gen_filename, orient="records", indent=2)
    logger.debug("Чтение записанных данных")
    with open(gen_filename) as js_file:
        res = json.load(js_file)
        logger.debug("Вывод данных")
        result = json.dumps(res, ensure_ascii=False, indent=2)
        return result
