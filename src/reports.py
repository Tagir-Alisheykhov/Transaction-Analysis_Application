import datetime
import logging
from functools import wraps
from os import path
from typing import Any, Optional

import pandas as pd

path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), "data/operations.csv")
path_to_logs = path.join(path.dirname(path.dirname(__file__)), "logs/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_formater = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(path_to_logs + "reports.log", mode="w", encoding="utf-8")
file_handler.setFormatter(file_formater)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def log_to_file(filename: str = "recorded_file.csv") -> Any:
    """
    Принимает 'DataFrame' из функций, записывая его в 'csv' - файл
    :return: Вывод результата принимаемой функции в консоль
    """

    def decorator(func: Any) -> Any:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.debug("\nЗАПУСК ДЕКОРАТОРА [  log_to_file  ]")
            df = func(*args, **kwargs)
            try:
                df.to_csv(path_to_logs + filename, header=True, index=True)
                logger.debug("Создание отформатированного файла прошло успешно")
            except Exception as err:
                logger.error(f"\n>>> ERROR <<<\nНе удалось реализовать записать файла\n{err}\n")
            return df

        return wrapper

    return decorator


@log_to_file("func_spending_by_category.csv")
def spending_by_category(transactions: pd.DataFrame, category: str, choice_date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает на вход 'DataFrame' с транзакциями, название категории, опциональную дату.
    :return: Функция возвращает 'DataFrame' с тратами по заданной категории за последние
    три месяца (от переданной даты).
    """
    logger.debug("ЗАПУСК ФУНКЦИИ [  spending_by_category  ]")
    transactions = transactions.copy()
    transactions.columns = transactions.columns.str.strip()
    logger.debug("Копирование входного файла и устранение пустых строк")

    date = datetime.datetime.now() if not choice_date else datetime.datetime.strptime(choice_date, "%d %m %Y")
    logger.debug("Определение даты (по умолчанию/ввод пользователем)")
    start_date = pd.to_datetime((date - pd.DateOffset(months=3)), dayfirst=True)
    end_date = pd.to_datetime(date, dayfirst=True)
    logger.debug("Определение начальной и конечной точки диапазона дат")
    transactions = transactions[transactions["Категория"] == category]
    logger.debug("Фильтрация данных по введенной категории")
    date_operations = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    logger.debug("Меняем тип дат операций")

    filtered_transacts = transactions[(date_operations >= start_date) & (date_operations <= end_date)]
    logger.debug("Фильтрация по диапазону дат")
    filtered_transacts.loc[:, "Сумма операции с округлением"] = [
        float(sum_operation.replace(",", ".")) for sum_operation in filtered_transacts["Сумма операции с округлением"]
    ]
    logger.debug("Форматируем суммы операций")

    df = pd.DataFrame({"Суммы операций": filtered_transacts["Сумма операции с округлением"]})
    return df


@log_to_file("func_spending_by_weekday.csv")
def spending_by_weekday(transactions: pd.DataFrame, choice_date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает на вход 'DataFrame' с транзакциями, опциональную дату.
    :return: Функция возвращает 'DataFrame' со средними тратами в
    каждый из дней недели за последние три месяца (от переданной даты).
    """
    logger.debug("ЗАПУСК ФУНКЦИИ [  spending_by_weekday  ]")
    transactions = transactions.copy()
    transactions.columns = transactions.columns.str.strip()
    logger.debug("Копирование входного файла и устранение пустых строк")

    date = datetime.datetime.now() if not choice_date else datetime.datetime.strptime(choice_date, "%d %m %Y")
    logger.debug("Определение даты (по умолчанию/ввод пользователем)")
    start_date = pd.to_datetime((date - pd.DateOffset(months=3)), dayfirst=True)
    end_date = pd.to_datetime(date, dayfirst=True)
    logger.debug("Определение начальной и конечной точки диапазона дат")

    transactions_datetime = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    transactions = transactions[(transactions_datetime >= start_date) & (transactions_datetime <= end_date)]
    logger.debug("Фильтрация по диапазону дат")

    transactions["Сумма операции с округлением"] = [
        float(sum_operation.replace(",", ".")) for sum_operation in transactions["Сумма операции с округлением"]
    ]
    logger.debug("Форматируем суммы операций")
    transactions["Сумма операции с округлением"] = pd.to_numeric(
        transactions["Сумма операции с округлением"], errors="coerce"
    )
    logger.debug("Форматируем нечисловые значения столбца в числовые или в NaN")
    transactions.dropna(subset=["Сумма операции с округлением"], inplace=True)
    logger.debug("Удаление строк со значением NaN")

    transactions["День"] = transactions_datetime.dt.isocalendar().day
    transactions["Номер недели"] = transactions_datetime.dt.isocalendar().week
    transactions["Год"] = transactions_datetime.dt.isocalendar().year
    weekly_transactions = (
        transactions.groupby(["Год", "Номер недели", "День"])
        .agg(
            count_transacts=("Сумма операции с округлением", "size"),
            average_amount=("Сумма операции с округлением", "mean"),
        )
        .reset_index()
    )
    logger.debug("Группировка определенных столбцов DF для определения среднего значения")
    weeks = weekly_transactions["Номер недели"].tolist()
    summ = weekly_transactions["average_amount"].tolist()
    logger.debug("Подготовка отформатированных данных для создания DF")
    dframe_func2 = pd.DataFrame({"Номер недели": weeks, "average_amount": summ})
    return dframe_func2


@log_to_file("func_spending_by_workday.csv")
def spending_by_workday(transactions: pd.DataFrame, choice_date: Optional[str] = None) -> pd.DataFrame:
    """
    Принимает на вход 'DataFrame' с транзакциями, опциональную дату.
    :return: # Функция выводит средние траты в рабочий и
    в выходной день за последние три месяца (от переданной даты) в 'DataFrame'.
    """
    logger.debug("ЗАПУСК ФУНКЦИИ [  spending_by_weekday  ]")
    transactions.columns = transactions.columns.str.strip()
    logger.debug("Создание копии входного файла")

    date = datetime.datetime.now() if not choice_date else datetime.datetime.strptime(choice_date, "%d %m %Y")
    logger.debug("Определение даты (по умолчанию/ввод пользователем)")
    start_date = pd.to_datetime((date - pd.DateOffset(months=3)), dayfirst=True)
    end_date = pd.to_datetime(date, dayfirst=True)
    logger.debug("Определение начальной и конечной точки диапазона дат")
    date_transactions = pd.to_datetime(transactions["Дата операции"], dayfirst=True)
    filtered_transactions = transactions[(date_transactions >= start_date) & (date_transactions <= end_date)].copy()
    logger.debug("Фильтрация по диапазону дат")

    filtered_transactions["Сумма операции с округлением"] = [
        float(sum_operation.replace(",", "."))
        for sum_operation in filtered_transactions["Сумма операции с округлением"]
    ]
    logger.debug("Форматируем суммы операций")

    filtered_transactions["Сумма операции с округлением"] = pd.to_numeric(
        filtered_transactions["Сумма операции с округлением"], errors="coerce"
    )
    logger.debug("Форматируем нечисловые значения столбца в числовые или в NaN")
    filtered_transactions["Сумма операции с округлением"] = filtered_transactions[
        "Сумма операции с округлением"
    ].dropna()
    logger.debug("Удаление строк со значением NaN")

    filtered_transactions.loc[:, "День недели"] = date_transactions[filtered_transactions.index].dt.day_name()
    logger.debug("Определяем названия дней недель")

    filtered_transactions["Год"] = date_transactions.dt.isocalendar().year
    filtered_transactions["Номер недели"] = date_transactions.dt.isocalendar().week
    filtered_transactions["День"] = date_transactions.dt.isocalendar().day
    weekdays_and_weekends = filtered_transactions[
        filtered_transactions["День недели"].isin(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        )
    ]
    average_values_weekends = (
        weekdays_and_weekends.groupby(["День недели", "Год", "Номер недели", "День"])
        .agg(
            count_transacts=("Сумма операции с округлением", "size"),
            average_amount=("Сумма операции с округлением", "mean"),
        )
        .reset_index()
    )
    logger.debug("Группировка определенных столбцов DF для определения среднего значения")
    value1_for_df = average_values_weekends["День недели"].tolist()
    value2_for_df = average_values_weekends["average_amount"].tolist()
    dframe_func3 = pd.DataFrame(
        {
            "День недели": value1_for_df,
            "Среднее траты": value2_for_df,
        }
    )
    return dframe_func3


if __name__ == "__main__":
    cycle_true = True
    choice_category = ""
    file_transacts = pd.read_csv(path_to_xlsx_file)
    logger.debug("Запуск цикла проверки ввода категории")
    while cycle_true:
        names_category = file_transacts.loc[:, "Категория"]
        user_choice_category = input("Введите необходимую категорию транзакций: \n").strip()
        if user_choice_category in names_category.values:
            choice_category = user_choice_category
            cycle_true = False
        else:
            logger.warning("\nТакой категории не существует\n")

    date_choice = input("Введите дату через пробел в формате 'ДД_ММ_ГГГГ': ")

    read_xlsx_func_1 = spending_by_category(file_transacts, choice_category, date_choice)
    read_xlsx_func_2 = spending_by_weekday(file_transacts, date_choice)
    read_xlsx_func_3 = spending_by_workday(file_transacts, date_choice)
    print(read_xlsx_func_1)
    print(read_xlsx_func_2)
    print(read_xlsx_func_3)
