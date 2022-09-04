import contextlib
import logging
from utils import Singleton
import psycopg2.pool
import psycopg2.extensions

logger = logging.getLogger(__name__)


class Connect:
    def __init__(self, poll: psycopg2.pool.SimpleConnectionPool):
        self.pool = poll

    def __enter__(self) -> psycopg2.extensions.connection:
        self.con = self.pool.getconn()
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con:
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
            password='123456',
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

    @contextlib.contextmanager
    def transaction(self) -> psycopg2.extensions.cursor:
        con = None
        try:
            with Connect(self.pool) as con:
                con.autocommit = False
                with Cursor(con) as cur:
                    yield cur
        except psycopg2.Error as e:
            logger.error(e)
            con.rollback()
        else:
            con.commit()


if __name__ == '__main__':
    db = Database()

    with db.transaction() as cur:
        cur.execute('select * from "Schedule"')
