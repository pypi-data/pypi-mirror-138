# pooling

pooling anything.

## Install

```
pip install pooling
```

## Usage Example 1


```
import MySQLdb
from MySQLdb.cursors import DictCursor

from pooling import PoolBase

class MysqlConnectionPool(PoolBase):
    
    def do_session_create(self, *create_args, **create_kwargs):
        create_kwargs.setdefault("cursorclass", DictCursor)
        create_kwargs.setdefault("autocommit", True)
        create_kwargs.setdefault("charset", "utf8mb4")
        return MySQLdb.connect(*create_args, **create_kwargs)

    def do_session_destory(self, real_session):
        real_session.close()

if __name__ == "__main__":
    conn_info = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "test",
        "password": "test",
        "db": "test",
    }
    pool = MysqlConnectionPool(pool_size=10, kwargs=conn_info)
    connection = pool.get_session()
    cursor = connection.cursor()
    count = cursor.execute("show databases")
    data = cursor.fetchall()
    print("rows count=", count)
    print("data=", data)
    assert count == len(data)

```

## Usage Example 2

```
import MySQLdb
from MySQLdb.cursors import DictCursor

from pooling import Pool

def mysql_conn_create():
    conn_info = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "test",
        "password": "test",
        "db": "test",
    }
    conn = MySQLdb.connect(cursorclass=DictCursor, autocommit=True, **conn_info)
    return conn

def mysql_conn_close(session):
    session.close()

if __name__ == "__main__":
    pool = Pool(pool_size=10, create_factory=mysql_conn_create, destory_factory=mysql_conn_close)
    connection = pool.get_session()
    cursor = connection.cursor()
    count = cursor.execute("show databases")
    data = cursor.fetchall()
    print("rows count=", count)
    print("data=", data)
    assert count == len(data)
```

## Note

* Call pool.get_session() returns a proxied connection instance.
* The returned proxied connection instance is a proxy instance of the real connection.
* When the returned proxied connection being delete, the real connection will be returned to the pool so that the real connection can be used again.
* A simple mysql connection pool can be imported by doing `from pooling.mysql import MysqlConnectionPool`.
* The `pooling.mysql` module depends on `mysqlclient`, but `pooling` is NOT, so that `mysqlclient` is not auto installed after `pooling` installed. You should do `pip install mysqlclient` by yourself if you want to use `MysqlConnectionPool`.

## Releases

### v0.1.0

- First release.
