import sqlite3
from dataclasses import dataclass


@dataclass
class DBDataTypes:
    """Этот класс сделан для удобства, чтобы потом не писать много раз TEXT или INTEGER или другой тип данных в
    экземплярах DBColumns"""
    TEXT: str = "TEXT"
    INTEGER: str = "INTEGER"


@dataclass
class DBColumns:
    """Датакласс, для хранения данных о названии колонок и о типе данных в этих колонках"""
    name: str = None  # Название колонки
    data_type: str = None  # Для удобства можно использовать атрибуты из DBDataTypes, либо писать TEXT или INTEGER


@dataclass
class Region:
    """К примеру у тебя есть таблица в бд, которая называется Regions, вот ниже - названия ее(таблицы) колонок.
    Далее будем создавать экземпляры этого класса и наполнять атрибуты значениями"""
    id: int = None
    region_name: str = None


class SQLiteDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self._connection = None

    def create_connect(self) -> None:
        """Создает соединение с БД"""
        self._connection = sqlite3.connect(database=self.db_name)
        print("Соединение установлено")

    def close_connect(self) -> None:
        """Закрывает соединение с БД"""
        self._connection.close()
        print("Соединение закрыто")

    def add_table(self, table_name: str, columns: list) -> None:
        """
        Добавление таблицы в бд.
        :param table_name: Название таблицы
        :param columns: Список экземпляров класса DBColumns
        :return: None
        """
        cursor = self._connection.cursor()
        column_s = []
        for column in columns:
            column_s.append(column.name)
            column_s.append(column.data_type)
        column_s = ", ".join(column_s)
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}({column_s})""")
        cursor.close()
        self._connection.commit()

    def del_table(self, table_name: str) -> None:
        """
        Удаление таблицы из БД.
        :param table_name: Название таблицы, которую нужно удалить.
        :return: None
        """
        cursor = self._connection.cursor()
        cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
        cursor.close()
        self._connection.commit()
        print(f"Таблица {table_name} удалена!")

    def check_value_exists(self, table_name, column_name, value) -> bool:
        """
        Проверка значения на присутствие в базе данных.
        :param table_name: Название таблицы, где ищем значение.
        :param column_name: Название колонки, где ищем значение.
        :param value: Значение, которое проверяем.
        :return: True - значение присутствует, False - значение отсутствует.
        """
        check_result = False
        cursor = self._connection.cursor()
        cursor.execute(f"""SELECT {column_name} FROM {table_name} WHERE {column_name} = "{value}" """)
        response = cursor.fetchone()
        cursor.close()
        if response:
            check_result = True
        return check_result

    def insert_item(self, table_name: str, item) -> None:
        """
        Вставка значения в БД.
        :param table_name: Название таблицы.
        :param item: Экземпляр датакласса.
        :return: None
        """
        cursor = self._connection.cursor()
        vopr = []
        keys = []
        values = []
        for key, value in item.__dict__.items():
            keys.append(key)
            values.append(value)
            vopr.append("?")
        keys_str = ", ".join(keys)
        vopr_str = ", ".join(vopr)

        check_exists = self.check_value_exists(table_name=table_name, column_name=keys[0], value=values[0])
        if not check_exists:
            command = f"""INSERT INTO {table_name}({keys_str}) VALUES ({vopr_str})"""
            cursor.execute(command, values)
            print(f"Запись {item} вставлена в таблицу {table_name}")
        else:
            print(f"Запись {item} уже имеется в таблице {table_name}")
        cursor.close()
        self._connection.commit()

    def insert_items(self, table_name: str, items: list):
        """
        Вставка значений в БД.
        :param table_name: Название таблицы.
        :param items: Список экземпляров датакласса.
        :return: None
        """
        for item in items:
            self.insert_item(table_name=table_name, item=item)

    def read_item(self, table_name: str, columns: list):
        pass


if __name__ == '__main__':
    db = SQLiteDB(db_name="magnit_Test2.db")
    db.create_connect()
    db.add_table(table_name="Regions",
                 columns=[DBColumns(name="id", data_type=DBDataTypes.INTEGER),
                          DBColumns(name="reion_name", data_type=DBDataTypes.TEXT)])
    regions = [Region(id=1), Region(id=2, name="Ставропольский край"),
               Region(id=3, name="Ростовская область")]
    db.insert_items(table_name="Regions", items=regions)
    # db.del_table(table_name="Regions")
    db.close_connect()

