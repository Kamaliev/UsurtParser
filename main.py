import datetime
import logging
import time
from typing import NamedTuple
from bs4 import BeautifulSoup
import requests
import logging

from database import Database, Schedule
from excel_reader import get_task

logger = logging.getLogger('__main__')


class File(NamedTuple):
    name: str
    link: str
    change: datetime.datetime = None


domain = 'https://bb.usurt.ru'


def _get_links(url: str, session: requests.Session):
    try:
        r = session.get(url)
    except Exception as e:
        logger.error(e)
        return []
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find(id='listContainer_databody')
    rows = table.findAll('tr')
    folders = []
    for row in rows:
        date = datetime.datetime.strptime(row.findAll('td')[2].findAll('span')[-1].text, '%d.%m.%Y %H:%M:%S')
        link = row.find('th').find('a')
        folders.append(File(
            name=link.text.strip(),
            link=link['href'],
            change=date
        ))

    return folders


def _get_files(session: requests.Session):
    all_files = []
    folders = []
    for i in ['https://bb.usurt.ru/webapps/cmsmain/webui/institution/Расписание/Очная форма обучения/Нечетная неделя',
              'https://bb.usurt.ru/webapps/cmsmain/webui/institution/Расписание/Очная форма обучения/Четная неделя']:
        folders += _get_links(i, session)
    for folder in folders:
        all_files += _get_links(domain + folder.link, session)

    return all_files


def download(session: requests.Session):
    files = _get_files(session)
    data = []
    for file in files:
        r = session.get(file.link)
        filename = file.name[:file.name.rfind('xls') + 3]
        with open(f'tmp/{filename}', 'wb') as f:
            f.write(r.content)
        logger.debug(f'file {filename} downloaded success')
        data.append(f'tmp/{filename}')
    return data


def main():
    while True:
        s = requests.session()
        files = download(s)
        Schedule().delete_all()
        for file in files:
            get_task(file)

        time.sleep(3600 * 3)


if __name__ == '__main__':
    print('Start')
    main()
