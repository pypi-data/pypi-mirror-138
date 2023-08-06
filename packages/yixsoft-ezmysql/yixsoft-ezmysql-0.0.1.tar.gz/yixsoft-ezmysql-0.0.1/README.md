# ezmysql USAGE GUIDE

## Config MySQL Connection

### Config from OS Environ

config os env below:

- APP_DB_HOST: mysql host, default 127.0.0.1
- APP_DB_PORT: mysql port, default 3306
- APP_DB_SCHEMA: database name
- APP_DB_USER: mysql username
- APP_DB_PWD: mysql passwd
- APP_DB_TIMEZONE: connect timezone default is os timezone

```python
from ezmysql import Pool

pool = Pool.from_os_env()
```

### Config by code
```python
from ezmysql import Pool

pool = Pool(host='127.0.0.1',
            port=3306,
            database='dbname',
            user='username',
            password='pwd',
            charset='utf8mb4',
            autocommit=True,
            time_zone='00:00')
```

## Process SQL

### simple use

```python
pool.query('select * from table where key=%s',['args'])
```

### auto sql use

```python
pool.query_from_table('table_name',['col1','col2'],dict(id=123))
pool.insert_table('table_name',dict(key1='foo',key2='bar'))
```

## Start Transaction

```python
with pool.begin() as trans:
    trans.insert_table('table_name', dict(key1='foo'))
```

