"""Константы проекта парсера документации Python."""

from pathlib import Path


MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_URL = 'https://peps.python.org/'
PEP_NUMERICAL_INDEX_URL = 'https://peps.python.org/numerical/'

BASE_DIR = Path(__file__).parent

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

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

PEP_STATUS_OUTPUT = ('Статус', 'Количество')

TOTAL_STATUS = 'Total'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

PRETTY_OUTPUT = 'pretty'
FILE_OUTPUT = 'file'

LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'

RESULTS_DIR = 'results'
DOWNLOADS_DIR = 'downloads'

DEFAULT_ENCODING = 'utf-8'
