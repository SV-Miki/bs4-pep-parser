"""Основной модуль запуска парсеров документации Python."""

import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (
    BASE_DIR,
    EXPECTED_STATUS,
    MAIN_DOC_URL,
    PEP_NUMERICAL_INDEX_URL,
    PEP_STATUS_OUTPUT,
    PEP_URL,
    TOTAL_STATUS,
)
from outputs import control_output
from utils import find_tag, get_response


def whats_new(session):
    """Парсит раздел What's New документации Python."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, whats_new_url)

    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    main_div = find_tag(
        soup,
        'section',
        attrs={'id': 'what-s-new-in-python'},
    )
    div_with_ul = find_tag(
        main_div,
        'div',
        attrs={'class': 'toctree-wrapper'},
    )
    sections_by_python = div_with_ul.find_all(
        'li',
        attrs={'class': 'toctree-l1'},
    )

    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]

    for section in tqdm(sections_by_python):
        version_a_tag = find_tag(section, 'a')
        version_link = urljoin(whats_new_url, version_a_tag['href'])
        response = get_response(session, version_link)

        if response is None:
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        h1 = find_tag(soup, 'h1')
        dl = find_tag(soup, 'dl')
        dl_text = dl.get_text(' ', strip=True)

        results.append((version_link, h1.text, dl_text))

    return results


def latest_versions(session):
    """Парсит список версий Python и их статусов."""
    response = get_response(session, MAIN_DOC_URL)

    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(
        soup,
        'div',
        attrs={'class': 'sphinxsidebarwrapper'},
    )
    ul_tags = sidebar.find_all('ul')

    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise Exception('Не найден список c версиями Python')

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)

        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''

        results.append((link, version, status))

    return results


def download(session):
    """Скачивает архив документации Python."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, downloads_url)

    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(
        soup,
        'div',
        attrs={'role': 'main'},
    )
    table_tag = find_tag(
        main_tag,
        'table',
        attrs={'class': 'docutils'},
    )
    archive_tag = find_tag(
        table_tag,
        'a',
        attrs={'href': re.compile(r'.+docs-html\.zip$')},
    )

    archive_link = archive_tag['href']
    archive_url = urljoin(downloads_url, archive_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)

    archive_path = downloads_dir / filename
    response = get_response(session, archive_url)

    if response is None:
        return

    with open(archive_path, 'wb') as file:
        file.write(response.content)

    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def get_pep_status(pep_soup, pep_link):
    """Получает статус со страницы PEP."""
    status_dt = None

    for dt_tag in pep_soup.find_all('dt'):
        if dt_tag.get_text(strip=True).rstrip(':') == 'Status':
            status_dt = dt_tag
            break

    if status_dt is None:
        logging.error(f'Не найден статус на странице {pep_link}')
        return None

    status_dd = status_dt.find_next_sibling('dd')

    if status_dd is None:
        logging.error(f'Не найдено значение статуса на странице {pep_link}')
        return None

    return status_dd.get_text(strip=True)


def log_status_mismatch(pep_link, real_status, expected_statuses):
    """Логирует несовпадение статусов PEP."""
    if real_status not in expected_statuses:
        logging.info(
            'Несовпадающие статусы:\n'
            f'{pep_link}\n'
            f'Статус в карточке: {real_status}\n'
            f'Ожидаемые статусы: {list(expected_statuses)}'
        )


def parse_pep_row(row):
    """Извлекает статус и ссылку из строки таблицы PEP."""
    columns = row.find_all('td')

    if not columns:
        return None

    first_column_tag = columns[0]
    preview_status = first_column_tag.get_text(strip=True)[1:]

    pep_number_tag = find_tag(row, 'a')
    pep_number = pep_number_tag.get_text(strip=True)

    if pep_number == '0':
        return None

    pep_link = urljoin(PEP_URL, pep_number_tag['href'])

    return preview_status, pep_link


def build_pep_results(status_counter):
    """Формирует итоговую таблицу статусов PEP."""
    results = [PEP_STATUS_OUTPUT]

    for status, count in status_counter.items():
        results.append((status, count))

    total = sum(status_counter.values())
    results.append((TOTAL_STATUS, total))

    return results


def pep(session):
    """Парсит статусы документов PEP."""
    response = get_response(session, PEP_NUMERICAL_INDEX_URL)

    if response is None:
        return

    soup = BeautifulSoup(response.text, 'lxml')

    table_tag = find_tag(
        soup,
        'table',
        attrs={'class': 'pep-zero-table docutils align-default'},
    )

    status_counter = Counter()

    for row in tqdm(table_tag.find_all('tr')[1:]):
        pep_data = parse_pep_row(row)

        if pep_data is None:
            continue

        preview_status, pep_link = pep_data

        response = get_response(session, pep_link)

        if response is None:
            continue

        pep_soup = BeautifulSoup(response.text, 'lxml')

        real_status = get_pep_status(
            pep_soup,
            pep_link,
        )

        if real_status is None:
            continue

        expected_statuses = EXPECTED_STATUS[preview_status]

        log_status_mismatch(
            pep_link,
            real_status,
            expected_statuses,
        )

        status_counter[real_status] += 1

    return build_pep_results(status_counter)


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    """Запускает парсер в выбранном режиме."""
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')

    session = requests_cache.CachedSession()

    if args.clear_cache:
        session.cache.clear()

    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results is not None:
        control_output(results, args)

    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
