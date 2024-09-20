# Приложение для "Анализа банковских транзакций" 

## Описание:
Приложение будет генерировать JSON-файлы для веб-страниц, формировать Excel-отсчёты,
а также предоставлять другие сервисы

## Установка:

### Способ - 1
```
1. Скопируйте URL-адрес репозитория:
----------------------------------------------------------------
https://github.com/Tagir-Alisheykhov/Transaction-Analysis_Application.git
----------------------------------------------------------------
2. Откройте PyCharm или другой используемый вами интерпретатор
и кликните на "Get From VCS".

3. Вставьте скопированный адрес в строку "URL"
4. Далее в строке "Directory" выберите расположение репозитория на вашем ПК. Либо оставьте без изменений
5. Затем кликните на "Clone" для запуска проекта
```
### Способ - 2
```
1. Откройте "PowerShell" или "Terminal"
2. Введите команду "git clone" и добавьте ссылку на скопированный репозиторий:
--------------------------------------------------------------------------
git@github.com:Tagir-Alisheykhov/Transaction-Analysis_Application.git
--------------------------------------------------------------------------
3. Запустите свой интерпретатор
4. Кликните на "Open"  
5. Найдите проект который вы добавили с помощью "git clone URL" (он должен сохраниться в вашей корневой директории)
6. Запустите найденный проект
```

## Описание функциональности: 
### Папка src/ - содержит в себе всю основную функциональность проекта
- [ reports.py ] - Содержит в себе функции которые принимают CSV-файл и затем каждая функция
по своему обрабатывает файл, выводя в формате DataFrame и создавая новый CSV-файл с помощью декоратора  


## Список зависимостей: 
- black              24.8.0      The uncompromising code formatter.
- certifi            2024.8.30   Python package for providing Mozilla's CA Bundle.
- charset-normalizer 3.3.2       The Real First Universal Charset Detector. Open, modern and actively maintained alternative to Chardet.
- click              8.1.7       Composable command line interface toolkit
- colorama           0.4.6       Cross-platform colored terminal text.
- coverage           7.6.1       Code coverage measurement for Python
- flake8             7.1.1       the modular source code checker: pep8 pyflakes and co
- idna               3.8         Internationalized Domain Names in Applications (IDNA)
- iniconfig          2.0.0       brain-dead simple config-ini parsing
- isort              5.13.2      A Python utility / library to sort Python imports.
- mccabe             0.7.0       McCabe checker, plugin for flake8
- mypy               1.11.2      Optional static typing for Python
- mypy-extensions    1.0.0       Type system extensions for programs checked with the mypy type checker.
- numpy              2.1.1       Fundamental package for array computing in Python
- packaging          24.1        Core utilities for Python packages
- pandas             2.2.2       Powerful data structures for data analysis, time series, and statistics
- pathspec           0.12.1      Utility library for gitignore style pattern matching of file paths.
- platformdirs       4.3.2       A small Python package for determining appropriate platform-specific dirs, e.g. a `user data dir`.
- pluggy             1.5.0       plugin and hook calling mechanisms for python
- pycodestyle        2.12.1      Python style guide checker
- pyflakes           3.2.0       passive checker of Python programs
- pytest             8.3.3       pytest: simple powerful testing with Python
- pytest-cov         5.0.0       Pytest plugin for measuring coverage.
- python-dateutil    2.9.0.post0 Extensions to the standard Python datetime module
- pytz               2024.1      World timezone definitions, modern and historical
- requests           2.32.3      Python HTTP for Humans.
- six                1.16.0      Python 2 and 3 compatibility utilities
- typing-extensions  4.12.2      Backported and Experimental Type Hints for Python 3.8+
- tzdata             2024.1      Provider of IANA time zone data
- urllib3            2.2.2       HTTP library with thread-safe connection pooling, file post, and more.
- pandas-stubs       2.2.2.240909 Type annotations for pandas

## Лицензия:

Этот проект не лицензирован