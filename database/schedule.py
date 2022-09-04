import datetime
import logging

from database import Database

logger = logging.getLogger(__name__)


class Schedule(Database):
    table = 'Schedule'

    def add(self, day, time, desc, facultative_id, group_name, odd):
        if self.check(day, time, desc, facultative_id, group_name, odd):
            logger.error(f"Record in db {','.join([day, time, desc, facultative_id, group_name, odd])}")
            return
        self._insert(self.table, day=day, time=time, desc=desc, facultative_id=facultative_id, group_name=group_name,
                     odd=odd, dt=datetime.datetime.now())

    def check(self, day, time, desc, facultative_id, group_name, odd):
        q = 'select count(*) from Schedule where day = ? and time = ?  and desc = ? and facultative_id = ? and group_name = ? and odd = ?'
        return self._get_result(q, day, time, desc, facultative_id, group_name, odd)[0] > 0

    def delete_all(self):
        q = 'delete from Schedule where id > 0'
        self._execute(q)
