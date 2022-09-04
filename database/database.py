import logging
import os.path
import sqlite3

from utils import Config, get_sql_commands, Singleton

logger = logging.getLogger(__name__)


class Database(metaclass=Singleton):
    def __init__(self):
        if os.path.isfile(Config.database):
            self.__con = sqlite3.connect(Config.database, isolation_level=None, check_same_thread=False)
        else:
            self._create_database()

    def _create_database(self):
        logger.info(f'Database create in {Config.database}')
        self.__con = sqlite3.connect(Config.database, isolation_level=None, check_same_thread=False)
        queries = get_sql_commands()
        for query in queries:
            logger.debug("DO IT:")
            logger.debug(query)
            self._execute(query)
        logger.info('Database created')

        for f in ['МФ', 'ЭТФ', 'ФУПП', 'ФЭУ', 'ЭМФ', 'УТС', 'СФ']:
            for c in range(1, 5):
                self._insert('Facultative', name=f, course=c)

    def _execute(self, query: str, *args):
        cursor = self.__con.cursor()

        try:
            cursor.execute(query, args)
        except sqlite3.Error as e:
            logger.error(e)
        finally:
            cursor.close()

    def _get_result(self, query: str, *args):
        cursor = self.__con.cursor()

        try:
            cursor.execute(query, args)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            logger.error(e)
        finally:
            cursor.close()

    def _get_results(self, query: str, *args):
        cursor = self.__con.cursor()

        try:
            cursor.execute(query, args)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(e)
        finally:
            cursor.close()

        return result

    def _insert(self, table, **kwargs):
        q = f"insert into {table} ({','.join([i for i in kwargs.keys()])}) VALUES ({','.join(['?' for i in range(len((kwargs.values())))])})"
        self._execute(q, *tuple(kwargs.values()))
