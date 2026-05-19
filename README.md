# Проект парсинга pep

## Описание проекта

bs4_parser_pep - парсер документации Python и документов PEP.

Проект позволяет:
- получать список изменений Python из раздела What's New
- получать список актуальных версий Python и их статусы
- скачивать архив документации Python
- собирать данные обо всех PEP
- сравнивать статусы PEP из общей таблицы и страницы документа
- подсчитывать количество PEP по каждому статусу
- сохранять результаты парсинга в CSV-файлы
- выводить результаты в терминал или в формате PrettyTable
- использовать кеширование HTTP-запросов
- логировать работу парсера и найденные несовпадения статусов


## Технологии

В проекте используются:

- Python 3.12
- BeautifulSoup4
- Requests
- Requests-cache
- Lxml
- PrettyTable
- Tqdm
- Pytest
- Flake8


## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <URL_репозитория>
```

```bash
cd bs4_parser_pep
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
```

#### Linux/macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
source venv/Scripts/activate
```

### 3. Установить зависимости

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## Режимы работы парсера

### whats-new

Парсит раздел What's New в документации Python.

```bash
python src/main.py whats-new
```

### latest-versions

Выводит список версий Python и их статусы.

```bash
python src/main.py latest-versions
```

### download

Скачивает архив документации Python.

```bash
python src/main.py download
```

### pep

Парсит документы PEP, собирает статистику по статусам и проверяет несовпадения статусов.

```bash
python src/main.py pep
```

## Дополнительные аргументы

### Очистка кеша

```bash
python src/main.py pep -c
```

### Вывод в формате PrettyTable

```bash
python src/main.py pep -o pretty
```

### Сохранение результатов в CSV

```bash
python src/main.py pep -o file
```

## Пример CSV-файла

| Статус   | Количество |
|----------|-----------|
| Active   | 38        |
| Final    | 354       |
| Rejected | 130       |
| Draft    | 45        |
| Total    | 726       |

## Автор

Владислав Шилов
