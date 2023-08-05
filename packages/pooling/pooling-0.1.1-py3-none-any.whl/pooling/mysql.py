import time
import typing
import MySQLdb
from MySQLdb.cursors import DictCursor

from .base import PoolBase
from .base import Session

class MysqlConnectionPool(PoolBase):
    MAX_RECONNECT_SLEEP_TIME = 5
    RECONNECT_SLEEP_TIME_DELTA = 0.1

    def do_session_create(self, *args, **kwargs) -> MySQLdb.Connection:
        kwargs.setdefault("cursorclass", DictCursor)
        kwargs.setdefault("autocommit", True)
        kwargs.setdefault("charset", "utf8mb4")
        return MySQLdb.connect(*args, **kwargs)

    def do_session_destory(self, real_session:MySQLdb.Connection):
        real_session.close()

    def get_session(self, timeout:typing.Optional[float]=None) -> Session:
        last_error = Exception("Too short time to get a connection...")
        stime = time.time()
        sleep_time = 0.0
        while True:
            ntime = time.time()
            if (not timeout is None) and (ntime - stime > timeout):
                break
            if sleep_time:
                sleep_time = self.get_session_sleep(sleep_time)
            try:
                session = super().get_session(timeout=timeout)
            except Exception as error:
                last_error = error
                continue
            try:
                session.ping()
            except Exception as error:
                last_error = error
                session._pooling_destory_session()
                continue
            return session
        raise last_error

    def get_session_sleep(self, sleep_time:float) -> float:
        time.sleep(sleep_time)
        sleep_time += self.RECONNECT_SLEEP_TIME_DELTA
        if sleep_time >= self.MAX_RECONNECT_SLEEP_TIME:
            sleep_time = 0.0
        return sleep_time
