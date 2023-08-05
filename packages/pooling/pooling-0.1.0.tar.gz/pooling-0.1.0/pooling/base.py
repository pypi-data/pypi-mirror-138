
import typing
from threading import Lock
from queue import Queue
from queue import Empty

import wrapt

SESSION_USAGE_COUNT_PROPERY = "_pooling_usage_count"
SESSION_MARK_FOR_DESTORY_PROPERTY = "_pooling_mark_for_destory"

POOL = typing.TypeVar("POOL")
REAL_SESSION = typing.TypeVar("REAL_SESSION")
POOLING_CREATE_FACTORY_TYPE = typing.Callable[[], REAL_SESSION]
POOLING_DESTORY_FACTORY_TYPE = typing.Callable[[REAL_SESSION], None]

class Session(wrapt.ObjectProxy):

    def __init__(self, real_session:REAL_SESSION, pool:POOL) -> None:
        super().__init__(real_session)
        self._pooling_real_session = real_session
        self._pooling_pool = pool
        self._pooling_pool_version = pool.version
        self._pooling_mark_for_destory_flag = False
        self._pooling_incr_usage_count()

    def __del__(self) -> None:
        if self._pooling_real_session:
            if self._pooling_pool_version != self._pooling_pool.version or self._pooling_mark_for_destory_flag:
                self._pooling_pool.destory_session(self._pooling_real_session)
            else:
                self._pooling_pool.return_session(self._pooling_real_session)

    def _pooling_incr_usage_count(self) -> None:
        setattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, getattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, 0) + 1)

    def _pooling_get_usage_count(self) -> int:
        return getattr(self._pooling_real_session, SESSION_USAGE_COUNT_PROPERY, 0)

    def _pooling_mark_for_destory(self) -> None:
        self._pooling_mark_for_destory_flag = True

    def _pooling_destory_session(self) -> None:
        self._pooling_mark_for_destory_flag = True
        self._pooling_pool.destory_session(self._pooling_real_session)
        self._pooling_real_session = None

    def _pooling_return_session(self) -> None:
        self._pooling_pool.return_session(self._pooling_real_session)
        self._pooling_real_session = None

class PoolBase(object):

    def __init__(self, pool_size:int, args:list=None, kwargs:dict=None) -> None:
        """
        pool_size: The max number of the real session will be created.
        args: args used to make a new real session.
        kwargs: kwargs used to make a new real session.
        """
        self.pool_size = pool_size
        self.create_args = args or []
        self.create_kwargs = kwargs or {}
        self.real_sessions = Queue()
        self.counter = 0
        self.make_session_lock = Lock()
        self.version = 1

    def do_session_create(self, *create_args, **create_kwargs):
        raise NotImplementedError()

    def do_session_destory(self, real_session):
        pass

    def create_session(self) -> REAL_SESSION:
        real_session = self.do_session_create(*self.create_args, **self.create_kwargs)
        session = Session(real_session, self)
        self.counter += 1
        return session

    def return_session(self, real_session:REAL_SESSION) -> None:
        self.real_sessions.put(real_session)

    def destory_session(self, real_session:REAL_SESSION) -> None:
        self.do_session_destory(real_session)
        self.counter -= 1

    def get_session(self, timeout:typing.Optional[float]=None) -> Session:
        try:
            real_session = self.real_sessions.get_nowait()
            session = Session(real_session, self)
            return session
        except Empty:
            if self.counter < self.pool_size:
                with self.make_session_lock as locked:
                    if locked and self.counter < self.pool_size:
                        session = self.create_session()
                        return session
        real_session = self.real_sessions.get(timeout=timeout)
        session = Session(real_session, self)
        return session

    def destory_all_sessions(self) -> None:
        self.version += 1
        while True:
            try:
                session = self.real_sessions.get_nowait()
            except Empty:
                break
            self.destory_session(session)

class Pool(PoolBase):
    
    def __init__(self, pool_size: int, create_factory:POOLING_CREATE_FACTORY_TYPE, destory_factory:typing.Optional[POOLING_DESTORY_FACTORY_TYPE]=None) -> None:
        super().__init__(pool_size)
        self.create_factory = create_factory
        self.destory_factory = destory_factory

    def do_session_create(self, *create_args, **create_kwargs):
        return self.create_factory()
    
    def do_session_destory(self, real_session):
        if self.destory_factory:
            self.destory_factory(real_session)
