# bs4_parser_pep

Парсер документации Python и документов PEP.

## Возможности

Проект позволяет:

- получать список изменений Python из раздела What's New
- получать список доступных версий Python и их статусы
- скачивать архив HTML-документации Python
- собирать данные обо всех PEP
- сравнивать статус PEP из общей таблицы со статусом на странице документа
- подсчитывать количество PEP по каждому статусу
- сохранять результаты парсинга в CSV
- выводить результаты в терминал или в формате PrettyTable
- использовать кеширование HTTP-запросов
- логировать работу парсера и найденные несовпадения статусов

## Технологии

- Python 3.12
- BeautifulSoup4
- Requests
- Requests Cache
- lxml
- PrettyTable
- tqdm
- pytest
- Flake8

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone git@github.com:SV-Miki/bs4_parser_pep.git
cd bs4_parser_pep
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
```

### 3. Активировать виртуальное окружение

Linux/macOS:

```bash
source venv/bin/activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### 4. Установить зависимости

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Режимы работы

### `whats-new`

Парсит раздел What's New документации Python и выводит ссылки на статьи, заголовки и информацию об авторах или редакторах.

```bash
python src/main.py whats-new
```

### `latest-versions`

Выводит список доступных версий Python и их статусы.

```bash
python src/main.py latest-versions
```

### `download`

Скачивает ZIP-архив HTML-документации Python в директорию `src/downloads`.

```bash
python src/main.py download
```

### `pep`

Парсит документы PEP, собирает статистику по статусам и проверяет несовпадения между общей таблицей и страницами отдельных PEP.

```bash
python src/main.py pep
```

## Дополнительные аргументы

Очистить HTTP-кеш перед запуском:

```bash
python src/main.py pep -c
```

Вывести результат в формате PrettyTable:

```bash
python src/main.py pep -o pretty
```

Сохранить результат в CSV:

```bash
python src/main.py pep -o file
```

Доступные параметры можно посмотреть через:

```bash
python src/main.py --help
```

## Пример результата PEP-парсера

```text
Статус Количество
Active 38
Withdrawn 71
Superseded 25
Final 374
Rejected 131
Deferred 36
April Fool! 1
Accepted 11
Draft 50
Total 737
```

При несовпадении статуса в общей таблице и на странице PEP информация сохраняется в лог. Для подсчёта используется фактический статус со страницы документа.

## Результаты

CSV-файлы PEP-парсера сохраняются в директорию:

```text
src/results/
```

Пример структуры файла:

```csv
"Статус","Количество"
"Active","38"
"Withdrawn","71"
"Superseded","25"
"Final","374"
"Rejected","131"
"Deferred","36"
"April Fool!","1"
"Accepted","11"
"Draft","50"
"Total","737"
```

## Проверка проекта

Запуск тестов:

```bash
pytest
```

Проверка стиля кода:

```bash
flake8 src
```

## Автор

Владислав Шилов
