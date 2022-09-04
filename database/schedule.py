import logging
from typing import NamedTuple
from database import Database

logger = logging.getLogger(__name__)


class Values(NamedTuple):
    time: str
    weekday: str
    desc: str
    group: str
    odd: int


class Schedule:
    table = 'Schedule'

    def __init__(self):
        self.__db = Database()

    def add(self, data: list[Values]):
        q = f'''insert into "Schedule"(time, "weekday", "desc", "group", odd) VALUES (%s, %s, %s, %s, %s)'''
        with self.__db.transaction() as cursor:
            cursor.execute('''delete from "Schedule" where id > 0''')
            for row in data:
                cursor.execute(q, row)

