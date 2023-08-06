import logging

import psycopg2

logger = logging.getLogger(__name__)

from .abstract import Abstract_DB
from soft_collect.config import settings as s


class Postgres(Abstract_DB):
    def select(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            c.execute(sql)
            row = c.fetchone()
            while row:
                yield row
                row = c.fetchone()

    def fetch_all(self, sql):
        with self.set_up_connection() as conn:
            c = conn.cursor()
            return c.execute(sql).fetchall()

    def set_up_connection(self, _retry=2):
        logger.info(f"Creating connection to SQL Server in")

        try:
            connection = psycopg2.connect(
                host=s.ip, database=s.base, user=s.user, password=s.password,
            )
        except (Exception, psycopg2.DatabaseError) as e:
            logger.error(f"Can't set up a connection with #{s.ip}/{s.base}, {e}")
            if _retry:
                return self.set_up_connection(_retry - 1)
            raise e
        return connection
