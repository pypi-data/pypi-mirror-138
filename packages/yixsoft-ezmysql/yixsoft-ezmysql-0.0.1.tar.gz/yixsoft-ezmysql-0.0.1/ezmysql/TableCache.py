from datetime import datetime, timedelta
from .operation.SqlOperation import DescTableOperation


class TableStructureCache:
    __cache = None
    __cache_timeout = None

    def __init__(self, timeout: timedelta):
        self.__cache = {}
        self.__cache_timeout = timeout

    def cache_structure(self, table: str, columns: (set, list)):
        structure = TableStructure(table, columns)
        self.__cache[table] = structure
        return structure

    def find_structure(self, table: str, cursor):
        structure = self.__cache.get(table)
        if structure is not None and not structure.expired(self.__cache_timeout):
            return structure
        op = DescTableOperation(table)
        structure = op.operate(cursor)
        columns = set([field['field'] for field in structure])
        structure = self.cache_structure(table, columns)
        return structure


class TableStructure:
    table_name = None
    __columns = None
    __init_time = None

    def __init__(self, table_name: str, columns: (set, list)):
        self.table_name = table_name
        self.__columns = set(columns)
        self.__init_time = datetime.now()

    def exists_columns(self, obj: dict):
        return list(self.__columns & set(obj.keys()))

    def expired(self, timeout: timedelta):
        return self.__init_time + timeout < datetime.now()
