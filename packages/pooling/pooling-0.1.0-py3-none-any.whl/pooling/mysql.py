import MySQLdb
from MySQLdb.cursors import DictCursor

from .base import PoolBase

class MysqlConnectionPool(PoolBase):
    
    def do_session_create(self, *create_args, **create_kwargs):
        create_kwargs.setdefault("cursorclass", DictCursor)
        create_kwargs.setdefault("autocommit", True)
        create_kwargs.setdefault("charset", "utf8mb4")
        return MySQLdb.connect(*create_args, **create_kwargs)

    def do_session_destory(self, real_session):
        real_session.close()
