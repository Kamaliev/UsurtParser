import logging

from database import Database

logger = logging.getLogger(__name__)


class Facultative(Database):
    table_name = 'Facultative'

    def get_id(self, name, course):
        q = f"select id from {self.table_name} where name = ? and course = ?"

        result = self._get_result(q, name, course)

        if result is None:
            logger.error(f'name = {name}, course = {course}, result = {result}')
            return
        return result[0]

    # def get_count_curses(self, name):
    #     q = f"select course from {self.table_name} where name = ?"
    #     return await self.__db.get_results(q, name)

if __name__ == '__main__':
    a = Facultative().get_id('asdasd', 3)