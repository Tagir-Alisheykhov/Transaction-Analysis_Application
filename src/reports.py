import json
import logging
import datetime
import pandas as pd
from os import path
from typing import Optional


path_to_xlsx_file = path.join(path.dirname(path.dirname(__file__)), 'data/operations.csv')


def spending_by_category(transactions: pd.DataFrame, category: str,
                         choice_date: Optional[str] = None) -> pd.DataFrame:
    """
    :return: DataFrame с суммами транзакций по выбранным категориям
    """
    finish_date = []
    # Обработка даты:
    date = datetime.datetime.now() \
        if not choice_date else datetime.datetime.strptime(choice_date, '%d %m %Y')
    start_date = date - pd.DateOffset(months=3)
    end_date = date

    transactions = transactions[transactions['Категория'] == category]  # Отфильтрованный DF по категории
    for index, row in transactions.iterrows():
        date_tr = row.loc[' Дата операции']      # ОБЯЗАТЕЛЬНО НУЖНО ИЗБАВИТЬСЯ ОТ ЛИШНИХ ПРОБЕЛОВ
        sum_operations = row.loc['Сумма операции']
        date_tr = datetime.datetime.strptime(date_tr, '%d.%m.%Y %H:%M:%S')
        if end_date >= date_tr >= start_date:
            finish_date.append(sum_operations)
    df = pd.DataFrame({'Суммы операций': finish_date})
    return df


def average_weekly_expenses(transactions: pd.DataFrame,
                            choice_date: Optional[str] = None) -> pd.DataFrame:
    """
    :return: DataFrame
    """
    # ОБЯЗАТЕЛЬНО НУЖНО ИЗБАВИТЬСЯ ОТ ЛИШНИХ ПРОБЕЛОВ

    filtered_date_transacts_list = []
    filtered_sum_transacts_list = []
    # Обработка опционального значения выбора даты:
    date = datetime.datetime.now() if not choice_date \
        else datetime.datetime.strptime(choice_date, '%d %m %Y')
    start_date = date - pd.DateOffset(months=3)
    end_date = date

    # Итерация по объекту с определением диапазона
    for index, transact in transactions.iterrows():
        transact_date = pd.to_datetime(transact[' Дата операции'], dayfirst=True)
        start = pd.to_datetime(start_date, dayfirst=True).floor('s')
        end = pd.to_datetime(end_date, dayfirst=True).floor('s')
        if end >= transact_date >= start:
            filtered_date_transacts_list.append(transact[' Дата операции'])
            filtered_sum_transacts_list.append(transact['Сумма операции с округлением'])

    filtered_date_transacts = pd.DataFrame({'Дата операции': filtered_date_transacts_list})
    transactions_datetime = pd.to_datetime(filtered_date_transacts['Дата операции'], dayfirst=True)

    filtered_sum_transacts_list = [float(summ.replace(',', '.')) for summ in filtered_sum_transacts_list]
    transactions['Сумма операции с округлением'] = pd.Series(filtered_sum_transacts_list)
    transactions['Сумма операции с округлением'] = pd.to_numeric(
        transactions['Сумма операции с округлением'], errors='coerce'
    )
    transactions.dropna(subset=['Сумма операции с округлением'], inplace=True)
    transactions['День'] = transactions_datetime.dt.isocalendar().day
    transactions['Номер недели'] = transactions_datetime.dt.isocalendar().week
    transactions['Год'] = transactions_datetime.dt.isocalendar().year
    weekly_transactions = (transactions.groupby(['Год', 'Номер недели', 'День'])
                           .agg(count_transacts=('Сумма операции с округлением', 'size'),
                                average_amount=('Сумма операции с округлением', 'mean'))
                           .reset_index())
    return weekly_transactions['average_amount']


if __name__ == '__main__':
    file_transacts = pd.read_csv(path_to_xlsx_file)
    cycle_true = True
    choice_category = input('Введите необходимую категорию транзакций: \n')
    # while cycle_true:
    # В ОБЩЕМ ЧТОБЫ ПРОВЕРИТЬ НУЖЕН ЦИКЛ
    #     choice_category = input('Введите необходимую категорию транзакций: \n').lower()
    #     if (choice_category == file_transacts['Категория']) is True:
    #         cycle_true = False
    #     else:
    #         print('Такой категории не существует: \n')

    # Здесь тоже можно сделать цикл и регулярное выражение
    date_choice = input('Введите дату через пробел в формате \'ДД_ММ_ГГГГ\': ')

    # ФУНКЦИЯ - 1
    # read_xlsx_func_1 = spending_by_category(file_transacts, choice_category, date_choice)

    # ФУНКЦИЯ - 2
    read_xlsx_func_2 = average_weekly_expenses(file_transacts, date_choice)
    print(read_xlsx_func_2)

# --- 2 ---
# Функция Траты по дням недели:
# ТЕГИ #json #pandas #logging #pytest #datetime
# принимает на вход:
# датафрейм с транзакциями,
# опциональную дату.
# Если дата не передана, то берется текущая дата.
# Функция возвращает средние траты в каждый
# из дней недели за последние три месяца (от переданной даты).
# ИНТЕРФЕЙС:
# def spending_by_weekday(transactions: pd.DataFrame,
#                         date: Optional[str] = None) -> pd.DataFrame:


# --- 3 ---
# Функция Траты в рабочий/выходной день:
# ТЕГИ #json #pandas #logging #pytest #datetime
# принимает на вход:
# датафрейм с транзакциями,
# опциональную дату.
# Если дата не передана, то берется текущая дата.
# Функция выводит средние траты в рабочий и в
# выходной день за последние три месяца (от переданной даты).
# ИНТЕРФЕЙС:
# def spending_by_workday(transactions: pd.DataFrame,
#                         date: Optional[str] = None) -> pd.DataFrame:



# --- 4 ---
# Декоратор без параметра —
# записывает данные отчета в файл с названием по умолчанию
# (формат имени файла придумайте самостоятельно).
# --- 5 ---
# Декоратор с параметром —
# принимает имя файла в качестве параметра.






# --- 1 ---
# Функций Траты по категории:
# ТЕГИ #json #pandas #logging #pytest #datetime
# принимает на вход:
# датафрейм с транзакциями,
# название категории,
# опциональную дату.
# Если дата не передана, то берется текущая дата.
# Функция возвращает траты по заданной категории
# за последние три месяца (от переданной даты).
# ИНТЕРФЕЙС:
# def spending_by_category(transactions: pd.DataFrame,
#                          category: str,
#                          date: Optional[str] = None) -> pd.DataFrame:

