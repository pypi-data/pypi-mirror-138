import logging
import os
import threading
from datetime import timedelta, datetime
from typing import List, Optional

from mysql.connector import errors
from mysql.connector.pooling import CNX_POOL_MAXSIZE
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from .operation import *
from .TableCache import TableStructureCache

CONNECTION_POOL_LOCK = threading.RLock()
logger = logging.getLogger('ezmysql')


class Pool(MySQLConnectionPool):
    __table_cache: TableStructureCache = None

    def __init__(self, cache_timeout: timedelta = timedelta(minutes=10), **kwargs):
        kwargs['pool_reset_session'] = False
        super().__init__(**kwargs)
        self.__table_cache = TableStructureCache(cache_timeout)

    @staticmethod
    def from_os_env():
        os_zone = datetime.now().astimezone().strftime('%z')
        mysql_zone = os_zone[0:-2] + ':' + os_zone[-2:]
        conn_params = dict(
            host=os.environ.get('APP_DB_HOST') or '127.0.0.1',
            port=os.environ.get('APP_DB_PORT') or 3306,
            database=os.environ.get('APP_DB_SCHEMA'),
            user=os.environ.get('APP_DB_USER'),
            password=os.environ.get('APP_DB_PWD'),
            charset='utf8mb4',
            autocommit=True,
            buffered=True,
            time_zone=os.environ.get('APP_DB_TIMEZONE') or mysql_zone,
            pool_reset_session=False
        )
        conn_params = {k: v for k, v in conn_params.items() if v is not None}
        return Pool(pool_reset_session=False, pool_name='{}_{}'.format(conn_params['database'], conn_params['user']),
                    **conn_params)

    def connect(self):
        try:
            return self.get_connection()
        except errors.PoolError:
            # Pool size should be lower or equal to CNX_POOL_MAXSIZE
            if self.pool_size < CNX_POOL_MAXSIZE:
                with threading.Lock():
                    new_pool_size = self.pool_size + 1
                    try:
                        self._set_pool_size(new_pool_size)
                        self._cnx_queue.maxsize = new_pool_size
                        self.add_connection()
                    except Exception as e:
                        logging.exception(e)
                    return self.connect()
            else:
                with CONNECTION_POOL_LOCK:
                    cnx = self._cnx_queue.get(block=True)
                    if not cnx.is_connected() or self._config_version != cnx._pool_config_version:
                        cnx.config(**self._cnx_config)
                        try:
                            cnx.reconnect()
                        except errors.InterfaceError:
                            # Failed to reconnect, give connection back to pool
                            self._queue_connection(cnx)
                            raise
                        cnx._pool_config_version = self._config_version
                    return PooledMySQLConnection(self, cnx)
        except Exception:
            raise

    def execute_with_cursor(self, operation: SqlOperation):
        cnx = cursor = None
        try:
            cnx = self.connect()
            cursor = cnx.cursor(buffered=True, dictionary=True)
            return operation.operate(cursor)
        except Exception:
            raise
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    def query(self, sql: str, params: list = None) -> List[dict]:
        """
        common select, return a list with dict
        :param sql: select sql
        :param params: args list
        :return: dict objects in array
        """
        query_operation = QuerySqlOperation(sql, params)
        return self.execute_with_cursor(query_operation)

    def query_from_table(self, table: str, columns: list = None, param: dict = None) -> List[dict]:
        """
        execute simple select on a table: select <columns> from <table> where (<key1>=<value1>) and (<key2>=<value2>)
        :param table: table name
        :param columns: select columns. None means select * from table.
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: matching results in list. result item is a dict
        """
        op = SelectTableSqlOperation(self.__table_cache, table, param, columns)
        return self.execute_with_cursor(op)

    def findone(self, sql: str, params: list = None) -> Optional[dict]:
        """
        if a select sql has one row max. can use this method. which will response the single row or None if not exists
        :param sql: select sql
        :param params: where args
        :return: single row in dict or None if not found. if exists multiple results will raise an exception
        """
        query_operation = FindOneOperation(sql, params)
        return self.execute_with_cursor(query_operation)

    def findone_from_table(self, table: str, columns: list = None, param: dict = None) -> dict:
        """
        find one in table mode
        :param table: table name
        :param columns: select columns. None means select *
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: single row in dict or None if not found. if exists multiple results will raise an exception
        """
        op = SelectOneFromTableOperation(self.__table_cache, table, param, columns)
        return self.execute_with_cursor(op)

    def query_obj(self, sql: str, params: list = None) -> Optional:
        """
        similar to findone, if select has only one column, can use this method to get value directly
        :param sql: select sql, must have only 1 column and max 1 row to response
        :param params: args list
        :return: column value or None if not found
        """
        query_operation = QueryObjOperation(sql, params)
        return self.execute_with_cursor(query_operation)

    def query_obj_from_table(self, table: str, column: str, param: dict = None) -> Optional:
        """
        select only one column from table.
        :param table: table name
        :param column: required column
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: value of determined column or None if not found
        """
        op = SelectObjectFromTableOperation(self.__table_cache, table, column, param)
        return self.execute_with_cursor(op)

    def update(self, sql: str, params: list = None) -> int:
        """
        process update sql
        :param sql: update sql
        :param params: args list
        :return: affected row count
        """
        query_operation = UpdateSqlOperation(sql, params)
        return self.execute_with_cursor(query_operation)

    def delete(self, sql: str, params: list = None) -> int:
        """
        process delete sql
        :param sql: delete sql
        :param params: args list
        :return: affected row count
        """
        del_operation = DeleteSqlOperation(sql, params)
        return self.execute_with_cursor(del_operation)

    def update_table(self, table_name: str, updates: dict, where: dict) -> int:
        """
        auto generate update sql for determined table and execute
        :param table_name: table name
        :param updates: args in set part. key=value, will ignore key if not exists in table columns
        :param where: args in where part. column=value mode. will ignore column if not exists in table
        :return: affected row count
        """
        op = UpdateTableOperation(self.__table_cache, table_name, updates, where)
        return self.execute_with_cursor(op)

    def delete_table(self, table_name: str, where: dict) -> int:
        """
        auto generate delete sql for determined table and execute
        :param table_name: table name
        :param where: args in where part. column=value mode. will ignore column if not exists in table
        :return: affected row count
        """
        op = DeleteTableOperation(self.__table_cache, table_name, where)
        return self.execute_with_cursor(op)

    def insert_table(self, table_name: str, item: dict):
        """
        insert the dict into determined table
        :param table_name: table name
        :param item: key=value in table values, will ignore columns if not exists in table
        :return: primary key value
        """
        query_operation = TableInsertOperation(self.__table_cache, table_name, item)
        return self.execute_with_cursor(query_operation)

    def insert(self, sql: str, params: list = None):
        """
        process insert sql
        :param sql: insert sql
        :param params: args list
        :return: primary key value
        """
        query_operation = CommonInsertOperation(sql, params)
        return self.execute_with_cursor(query_operation)

    def begin(self, consistent_snapshot=False, isolation_level=None, readonly=None):
        cnx = self.connect()
        cnx.start_transaction(consistent_snapshot, isolation_level, readonly)
        return Transaction(self.__table_cache, cnx)


class Transaction(object):

    def __init__(self, cache: TableStructureCache, connection):
        self.__table_cache = cache
        self.cnx = None
        if isinstance(connection, PooledMySQLConnection):
            self.cnx = connection
            self.cursor = connection.cursor(buffered=True, dictionary=True)
        else:
            raise AttributeError("connection should be a PooledMySQLConnection")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and exc_val is None and exc_tb is None:
            self.commit()
        else:
            # will raise with-body's Exception, should deal with it
            self.rollback()
        self.close()

    def query(self, sql: str, params: list = None):
        """
        common select, return a list with dict
        :param sql: select sql
        :param params: args list
        :return: dict objects in array
        """
        query_operation = QuerySqlOperation(sql, params)
        return query_operation.operate(self.cursor)

    def query_from_table(self, table: str, columns: list = None, param: dict = None):
        """
        execute simple select on a table: select <columns> from <table> where (<key1>=<value1>) and (<key2>=<value2>)
        :param table: table name
        :param columns: select columns. None means select * from table.
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: matching results in list. result item is a dict
        """
        op = SelectTableSqlOperation(self.__table_cache, table, param, columns)
        return op.operate(self.cursor)

    def findone(self, sql: str, params: list = None):
        """
        if a select sql has one row max. can use this method. which will response the single row or None if not exists
        :param sql: select sql
        :param params: where args
        :return: single row in dict or None if not found. if exists multiple results will raise an exception
        """
        query_operation = FindOneOperation(sql, params)
        return query_operation.operate(self.cursor)

    def findone_from_table(self, table: str, columns: list = None, param: dict = None):
        """
        find one in table mode
        :param table: table name
        :param columns: select columns. None means select *
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: single row in dict or None if not found. if exists multiple results will raise an exception
        """
        op = SelectOneFromTableOperation(self.__table_cache, table, param, columns)
        return op.operate(self.cursor)

    def query_obj(self, sql: str, params: list = None):
        """
        similar to findone, if select has only one column, can use this method to get value directly
        :param sql: select sql, must have only 1 column and max 1 row to response
        :param params: args list
        :return: column value or None if not found
        """
        query_operation = QueryObjOperation(sql, params)
        return query_operation.operate(self.cursor)

    def query_obj_from_table(self, table: str, column: str, param: dict = None):
        """
        select only one column from table.
        :param table: table name
        :param column: required column
        :param param: args in where part. column=value mode. will ignore column if not exists in table
        :return: value of determined column or None if not found
        """
        op = SelectObjectFromTableOperation(self.__table_cache, table, column, param)
        return op.operate(self.cursor)

    def insert_table(self, table_name: str, item: dict):
        """
        insert the dict into determined table
        :param table_name: table name
        :param item: key=value in table values, will ignore columns if not exists in table
        :return: primary key value
        """
        cursor = self.cursor
        op = TableInsertOperation(self.__table_cache, table_name, item)
        return op.operate(cursor)

    def insert(self, sql: str, params: list = None):
        """
        process insert sql
        :param sql: insert sql
        :param params: args list
        :return: primary key value
        """
        cursor = self.cursor
        op = CommonInsertOperation(sql, params)
        return op.operate(cursor)

    def update(self, sql: str, params: list = None):
        """
        process update sql
        :param sql: update sql
        :param params: args list
        :return: affected row count
        """
        cursor = self.cursor
        op = UpdateSqlOperation(sql, params)
        return op.operate(cursor)

    def delete(self, sql: str, params: list = None):
        """
        process delete sql
        :param sql: delete sql
        :param params: args list
        :return: affected row count
        """
        cursor = self.cursor
        op = DeleteSqlOperation(sql, params)
        return op.operate(cursor)

    def update_table(self, table_name: str, updates: dict, where: dict):
        """
        auto generate update sql for determined table and execute
        :param table_name: table name
        :param updates: args in set part. key=value, will ignore key if not exists in table columns
        :param where: args in where part. column=value mode. will ignore column if not exists in table
        :return: affected row count
        """
        cursor = self.cursor
        op = UpdateTableOperation(self.__table_cache, table_name, updates, where)
        return op.operate(cursor)

    def delete_table(self, table_name: str, where: dict):
        """
        auto generate delete sql for determined table and execute
        :param table_name: table name
        :param where: args in where part. column=value mode. will ignore column if not exists in table
        :return: affected row count
        """
        cursor = self.cursor
        op = DeleteTableOperation(self.__table_cache, table_name, where)
        return op.operate(cursor)

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    def close(self):
        self.cursor.close()
        self.cnx.close()
