import json
import logging
from os import path
import pandas as pd


path_to_data = path.join(path.dirname(path.dirname(__file__)), "data/")
csv_file = pd.read_csv(path_to_data + "operations.csv")


def simple_search(choice_word: str):
    file_csv = csv_file.copy()
    file_csv.columns.str.strip()
    gen_filename = path_to_data + "file_by_simple_search.json"
    filter_by_key = file_csv[
        (file_csv["Категория"].str.contains(choice_word, na=False, case=False)) |
        (file_csv["Описание"].str.contains(choice_word, na=False, case=False))
    ]
    filter_by_key.to_json(gen_filename, orient="records", indent=2)
    with open(gen_filename) as js_file:
        res = json.load(js_file)
        return json.dumps(res, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    choice_key_word = input("Простой поиск: ")
    print(simple_search(choice_key_word))
