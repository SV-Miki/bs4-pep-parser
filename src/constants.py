"""Константы проекта парсера документации Python."""

from pathlib import Path


# URL-адреса документации Python и PEP.
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
PEP_NUMERICAL_INDEX_URL = 'https://peps.python.org/numerical/'


# Базовые пути проекта.
BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = 'results'
DOWNLOADS_DIR = 'downloads'


# Форматы даты и логирования.
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'


# Пути для логирования.
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'


# Режимы вывода результатов.
PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'


# Кодировка по умолчанию.
DEFAULT_ENCODING = 'utf-8'


# Ожидаемые статусы PEP.
EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}


# Заголовки и служебные значения для вывода статистики PEP.
PEP_STATUS_OUTPUT = ('Статус', 'Количество')
TOTAL_STATUS = 'Total'
