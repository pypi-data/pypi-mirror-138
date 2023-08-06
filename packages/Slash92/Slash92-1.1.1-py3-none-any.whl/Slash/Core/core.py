from typing import final
import logging
import string
import time
import sys
import re
import os
import psycopg2

from .exceptions_ import (
    SlashBadColumnNameError, SlashLenMismatch,
    SlashOneTableColumn, SlashTypeError,
    SlashBadAction, SlashPatternMismatch,
    SlashNoResultToFetch, SlashUnexpectedError,
    SlashNotTheSame
)
from ..types_ import (
    QueryQueue, BasicTypes,
    BasicTypes, Column
)


class Connection:
    def __init__(self, dbname, user, password, host, port, *, logger=False):
        self._dbname = dbname
        self._user = user
        self._password = password
        self._host = host
        self._port = port

        self.__connection = psycopg2.connect(
            dbname=self._dbname,
            user=self._user,
            password=self._password,
            host=self._host,
            port=self._port
        )
        self.__cursor = self.__connection.cursor()

        self.__query_queue = QueryQueue(self)

        self.__logger = logger

    @property
    def queue(self):
        return self.__query_queue

    @property
    def cursor(self):
        return self.__cursor

    def execute(self, request, message="", data=None):
        try:
            self.__cursor.execute(request, data)
            self.__connection.commit()
        except Exception as e:
            if self.__logger is not False:
                if os.environ.get("redirect_error") != "True":
                    print(e)
                self.__logger.info(
                    "Unsuccessful commit: \n\t<< {} >>\n\t{}\n\n{}".format(request, message, e)
                )
        else:
            if self.__logger is not False:
                self.__logger.info("Successful commit: {}".format(message))

    def close(self):
        self.__connection.close()
        if self.__logger is not False:
            self.__logger.info("Session closed")

    def fetchall(self):
        try:
            return self.__cursor.fetchall()
        except psycopg2.ProgrammingError:
            raise SlashNoResultToFetch("\n\tNo results to fetch")
        except:
            raise SlashUnexpectedError("\n\t\"\_(-_-)_/\"")

    def create(self, table, operation_obj=None):
        Create(table, BasicTypes.TYPES_LIST, self, operation_obj)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.__connection.close()


class Create:
    def __init__(self, table, types_list, conn: Connection, operation_obj):
        self.connection = conn
        self.table = table
        if self.__validate(types_list):
            self.__create(table, operation_obj)

    def __validate(self, types_list):
        CheckDatas.check_str(self.table.name)

        for column in self.table.columns:
            if column.type not in types_list:
                raise SlashTypeError(f"{type(column.type)} is not available type for data base")

            CheckDatas.check_str(column.name)

        return True

    def __create(self, table, operation_obj):
        if operation_obj:
            table.op = operation_obj(self.connection, table)

        request = "CREATE TABLE IF NOT EXISTS {} (rowID SERIAL PRIMARY KEY, {})".format(
            table.name,
            ", ".join([f"{col.name} {col.sql_type}" for col in table.columns])
        )
        self.connection.execute(
            CheckDatas.check_sql(request, "create"),
            "create operation"
        )


@final
class SQLCnd:
    class EQ:
        symbol = "="
    class AND:
        symbol = "AND"
    class NE:
        symbol = "!="
    class OR:
        symbol = "OR"
    class NOT:
        symbol = "NOT"
    class GT:
        symbol = ">"
    class LT:
        symbol = "<"
    class GE:
        symbol = ">="
    class LE:
        symbol = "<="

    @staticmethod
    def where(*condition):
        condition = list(condition)

        for index, cond_item in enumerate(condition):
            if type(cond_item) is not list:
                condition[index] = cond_item.symbol
                continue

            if len(cond_item) != 3:
                raise SlashLenMismatch(
                    """Lenght of the condition item should be 3, not {}
                    """.format(
                        len(cond_item)
                    )
            )

            left_side = cond_item[0]
            cond_symbol = cond_item[1]
            right_side = cond_item[2]

            if type(left_side) is Column:
                if left_side.type is not type(right_side):
                    raise SlashNotTheSame(
                        "\n\tColumn and input types are not equal:\n\nColumn {}\nData {}".format(
                            left_side.type,
                            type(right_side)
                        )
                    )
                left_side = left_side.name
                left_side = CheckDatas.check_str(left_side)
            else:
                raise SlashTypeError(
                    """Type of the name of column should be Column, not {}""".format(
                        type(left_side)
                    )
                )
            

            if not cond_symbol.__dict__.get("symbol"):
                raise SlashTypeError("""Wrong type for condition symbol""")

            if type(right_side) not in BasicTypes.TYPES_LIST:
                raise SlashTypeError("""Wrong type for data""")

            temp_value = None
            if right_side.type_name in BasicTypes.NEED_FORMAT:
                temp_value = f"'{right_side.value}'"
            else:
                temp_value = str(right_side.value)

            cond_item[0:3] = [f"{left_side} {cond_symbol.symbol} {temp_value}"]

        condition = " ".join([i[0] if type(i) is list else i for i in condition])
        condition = CheckDatas.check_str(" WHERE " + condition)

        return condition

    @staticmethod
    def order_by(column, *, desc=""):
        return " ORDER BY {} {}".format(
            CheckDatas.check_str(column),
            CheckDatas.check_str(desc)
        )

    @staticmethod
    def group_by(): ...


class CheckDatas:
    SQL_TEMPLATES: dict = {
        "insert": r"INSERT INTO [a-zA-Z0-9_]* [()a-zA-Z,\s_0-9]* VALUES [a-zA-Z)(0-9,%\s'@._-]*",
        "create": r"CREATE TABLE IF NOT EXISTS [a-zA-Z0-9_]* [)()a-zA-Z0-9',\s_%]*",
        "update": r"UPDATE [a-zA-Z0-9_]* SET [a-zA-Z0-9\s<>!=',-_%]*",
        "delete": r"DELETE FROM [a-zA-Z0-9_]* [a-zA-Z0-9\s<>!=_.'%]*",
        "select": r"SELECT [a-zA-Z0-9(),\s'<>!=*._%]*"
    }
    def __init__(self): ...

    @staticmethod
    def check_str(str_: str):
        available_char = string.ascii_letters + string.digits + "@._-=><' "
        for char_  in str_:
            if char_ not in available_char:
                raise SlashBadColumnNameError(
                    f"Error:\n\nBad name for column of data base\nName: {str_}\nSymbol: <{char_}>"
                )
        return str_

    @staticmethod
    def check_sql(sql_request: str, action: str):
        sql_template = CheckDatas.SQL_TEMPLATES.get(action)
        if sql_template is not None:
            template = re.findall(sql_template, sql_request)
            if sql_request in template:
                return sql_request
            else:
                raise SlashPatternMismatch(
                    "\n\nPattern mismatch:\n\t{}\n\nFinded pattern: {}\n\t".format(
                        sql_request, template
                    )
                )
        else:
            raise SlashBadAction("Action is wrong")


class CheckColumns:
    @staticmethod
    def check(condition, *tables):
        temp_columns = []
        for table in tables[0]:
            for column in table.columns:
                temp_columns.append(column.name)

        for c in temp_columns:
            if temp_columns.count(c) == 1:
                if c in condition:
                    raise SlashOneTableColumn("\n\tNot global column: << {} >>".format(c))


class Logger(logging.Logger):
    def __init__(self, name: str, file: str, *, redirect_error: bool=False, level=logging.INFO) -> None:
        super().__init__(name, level=level)

        self.__redirect_error = redirect_error
        os.environ.setdefault("redirect_error", str(redirect_error))

        handler = logging.FileHandler(self.__path(file), encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s]:[%(process)d-%(levelname)s]:[%(name)s]:[%(message)s]")

        handler.setFormatter(formatter)
        self.addHandler(handler)

        with open(str(os.environ.get("logs")), "a") as file_:
            file_.write("\n")

        self.info("Start session")
        self.__start_time = time.time()

    def __path(self, file: str):
        path_ = os.path.dirname(os.path.abspath(file)) + "\\logs"

        if not os.path.exists(path_):
            os.mkdir(path_)
        path_ += "\\data.log"

        os.environ.setdefault("logs", path_)
        if self.__redirect_error:
            sys.stderr = open(str(os.environ.get("logs")), "a")

        return path_

    def __del__(self):
        self.info(f"Session closed (work time: {time.time() - self.__start_time})")
