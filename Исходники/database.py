from cx_Oracle import connect
from config import *
from enum import Enum
from typing import Tuple, Dict, List
from os.path import exists


class Table(Enum):
    """
        Класс для констант названий таблиц
    """
    courses = 'courses'


class Database:
    """
        Класс для работы с базой данных, он "прокладка" между программой и БД
    """
    def __init__(self):
        """
            Конструктор класса, тут подключаемся к БД
        """
        if not exists(FILE_NAME_CONFIG):
            print('\n\nФайл конфига не найден, нажмите Enter чтобы выйти.')
            input()
            quit()
        with open(FILE_NAME_CONFIG) as f:
            HOST = f.readline()
        HOST = HOST[:-1] if '\n' in HOST else HOST
        try:
            self._connect = connect(HOST, encoding="UTF-8")
        except:
            print('\n\nПри подключении к базе данных произошла ошибка, проверьте файл;\nДля выхода нажмите Enter.')
            input()
            quit()
        else:
            self._cursor = self._connect.cursor()

    def drop_table(self):
        try:
            self._cursor.execute('DROP TABLE COURSES ')
        except:
            ...
        self.commit('CREATE TABLE COURSES '
                    '( ID varchar (50), '
                    '  DATE1 varchar(50), '
                    '  AMOUNT_FOREIGN_VALUE number(30), '
                    '  AMOUNT_RUBLE_VALUE number(30))')

    def __enter__(self):
        """
            Создаем метод для работы с базой данных через with as
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
            Также метод для работы с with as

        """
        self._cursor.close()
        self._connect.close()

    def commit(self, queries=None):
        """
            Сохранение изменений в базе, с попутным приминением запросов если их передали
        """
        if isinstance(queries, str):    # если запрос один (т.к. цикл пройдется посимвольно мы создаем кортеж и кладем в него запрос)
            queries = (queries, )
        for query in queries:
            self._cursor.execute(query)
        self._connect.commit()

    def truncate_all(self):
        """
            Чистим бд перед очередным парсингом
        """
        query = (f'TRUNCATE TABLE {table.name}' for table in Table)
        try:
            self.commit(query)
        except:
            ...

    def add_new_currency(self, data: Dict[str, List[Course]]):
        """
            Добавление в бд записи
			Cловарь имеющий структуру КЛЮЧ : СПИСОК КУРСОВ ЗА ВСЁ ВРЕМЯ

        """
        title, courses = data.popitem()
        queries = []
        for course in courses:
            need_string = f"'{course[0]}', {course[1]}, {course[2].replace(',', '.')}"
            queries.append('INSERT INTO courses (ID, DATE1, AMOUNT_FOREIGN_VALUE, AMOUNT_RUBLE_VALUE) '
                           f'    VALUES (\'{title}\', {need_string})')
        self.commit(queries=queries)

    def get_course(self, date: str) -> List[tuple]:
        """
            Получение курса по определенной дате
        """
        query = 'SELECT ID,' \
                '       AMOUNT_FOREIGN_VALUE, ' \
                '       AMOUNT_RUBLE_VALUE ' \
                f'FROM {Table.courses.name} ' \
                f'WHERE DATE1 = \'{date}\''
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def get_cross_course(self, date: str) -> Tuple[tuple]:
        """
            Получение всех курсов по каждой валюте к рублю, после, сравнение их между собой
        """
        query = "SELECT new_courses.ID || ' - ' || courses.ID || ': 1 к ' || ROUND(AMOUNT_RUBLE_VALUE / AMOUNT_FOREIGN_VALUE / course_to_ruble2, 4)  " \
                 f'FROM courses ' \
                 f"INNER JOIN (SELECT ID, AMOUNT_RUBLE_VALUE / AMOUNT_FOREIGN_VALUE AS course_to_ruble2 FROM courses WHERE DATE1 = '{date}') new_courses ON new_courses.ID != courses.ID " \
                 f"WHERE DATE1 = '{date}' AND course_to_ruble2 != AMOUNT_RUBLE_VALUE / AMOUNT_FOREIGN_VALUE"
        self._cursor.execute(query)
        return self._cursor.fetchall()


if __name__ == '__main__':
    pass
