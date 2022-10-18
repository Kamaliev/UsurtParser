import contextlib
import logging
from utils import Singleton
import psycopg2.pool
import psycopg2.extensions
import psycopg2.extras

logger = logging.getLogger('__main__')


class Connect:
    def __init__(self, poll: psycopg2.pool.SimpleConnectionPool):
        self.pool = poll

    def __enter__(self) -> psycopg2.extensions.connection:
        self.con: psycopg2.extensions.connection = self.pool.getconn()
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con:
            if not self.con.autocommit:
                if exc_val:
                    self.con.rollback()
                else:
                    self.con.commit()
            self.pool.putconn(self.con)


class Cursor:
    def __init__(self, con):
        self.con = con

    def __enter__(self) -> psycopg2.extensions.cursor:
        self.cursor = self.con.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('EXIT')
        if self.cursor:
            self.cursor.close()


class Database(metaclass=Singleton):
    def __init__(self):
        logger.info('Init db')
        self.__db_credits = dict(
            host='usurt.site',
            port=5432,
            user='postgres',
            password='117b8d835769d60f6dc76e4852c91f03',
            database='main'
        )
        self.pool = psycopg2.pool.SimpleConnectionPool(
            minconn=5,
            maxconn=10,
            **self.__db_credits
        )

    def execute(self, query, *args):
        with Connect(self.pool) as con:
            with Cursor(con) as cur:
                try:
                    cur.execute(query, args)
                except psycopg2.Error as e:
                    logger.error(e)

    @staticmethod
    def execute_many(cursor, q, data):
        psycopg2.extras.execute_values(cursor, q, data)

    @contextlib.contextmanager
    def transaction(self) -> psycopg2.extensions.cursor:
        with Connect(self.pool) as con:
            con.autocommit = False
            with Cursor(con) as cur:
                yield cur



if __name__ == '__main__':
    db = Database()

    with db.transaction() as cur:
        cur.execute('select * from "Schedule"')
