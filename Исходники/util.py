from datetime import datetime
from typing import Match, List, Tuple
import re
from config import *
from database import Database


def decorate_output():
    print('=' * AMOUNT_EQUELS)


def get_rows(html_code: str) -> Tuple[Match[str]]:
    """
        Возвращает итератор со всеми рядами (tr)
    """
    return tuple(re.finditer(pattern=r'<tr((?!/tr).)*',
                             string=html_code,
                             flags=re.DOTALL))[2:]


def get_cells(row_code: str) -> Course:
    """
        Возвращает именованный кортеж значениями курса за определенное число
    """
    return Course(*re.findall(pattern=r'\d[^<]*',
                              string=row_code))


def cut_course(html_code: str) -> List[Course]:
    """
        Обрезаем полученный html code, получаем ячейки курсы из верстки
    """
    result_list = []
    for row in get_rows(html_code=html_code):
        result_list.append(get_cells(row.group()))
    return result_list


def decorate_output_course(course: List[tuple]):
    """
        Выводим красиво курс, если такой курс есть
    """
    decorate_output()
    for currency in course:
        print(f'{currency[0]}: {currency[1]} к {currency[2]}')
    decorate_output()


def output_course(date: str):
    """
        Вывод если пользователь ввёл дату верно
    """
    with Database() as db:
        course: List[tuple] = db.get_course(date=date)
        if not course:
            print('Курс по введенной дате не найден')
        else:
            decorate_output_course(course=course)


def check_date(date: str) -> bool:
    """
        Проверка введенной даты на существование
    """
    try:
        datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        return False
    else:
        return True


def check_input(method):
    """
        Поиск по дате
    """
    while True:
        date: str = input('Введите нужную дату в формате дд.мм.гггг (0 - выход): ')
        if date == '0':
            return
        elif check_date(date=date):
            method(date=date)
        else:
            print('\nВы ввели неверный формат, попробуйте ещё раз.\n')


def update_data(parse):
    """
        Обновление данных в бд (перепарсиваем и заливаем всё)
    """
    with Database() as db:
        db.truncate_all()  # чистим бд перед загрузкой в неё данных
        for currency in parse():
            db.add_new_currency(currency)


def output_cross_course(courses: Tuple[tuple]):
    """
        Красивый вывод курсов
    """
    if courses:
        decorate_output()
        for index, course in enumerate(courses, start=1):
            print(course[0].replace('к .', 'к 0.'))
            if index % 4 == 0:
                decorate_output()
    else:
        print('За введенную дату курсы не найдены.')


def cross_course(date: str):
    """
        Получение из бд обработанных данных, а именно всех курсов валют по дате
    """
    with Database() as db:
        output_cross_course(db.get_cross_course(date=date))


def check_db_available():
    """
        Проверка доступности базы данных
    """
    Database()