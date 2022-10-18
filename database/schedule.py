import logging
from typing import NamedTuple, Union
from database import Database

logger = logging.getLogger('__main__')


class Values(NamedTuple):
    time: Union[str, None]
    weekday: Union[str, None]
    desc: Union[str, None]
    group: Union[str, None]
    odd: Union[int, None]
    facultative: Union[str, None]
    course: Union[int, None]


class Schedule:
    table = 'Schedule'

    def __init__(self):
        self.__db = Database()

    def add(self, data: list[Values]):
        logger.info('start add records')
        q = f'''insert into "Schedule"("time", "weekday", "desc", "group", odd, facultative, course) VALUES %s on conflict("time", "weekday", "desc", "group") do nothing'''
        with self.__db.transaction() as cursor:
            cursor.execute('''delete from "Schedule" where id > 0''')
            self.__db.execute_many(cursor, q, data)


