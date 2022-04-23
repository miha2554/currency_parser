from threading import Thread, active_count
from time import sleep
from my_parser import *


def reparse():
    """
        Парсим данные в отдельном потоке (чтоб не крашнулось приложение)
    """
    check_db_available()
    Thread(target=update_data, args=(parse, )).start()
    print('Добро пожаловать.\n'
          'В данный момент происходит парсинг, подождите несколько секунд ..', end='.')
    while active_count() > 1:   # ждем пока закончится парс
        sleep(1)
        print(end='.')
    print('\nСпаршено.')


def menu():
    while True:
        result: str = input('Выберите нужный пункт меню:\n'
                            '1) Вывести курс по определенной дате;\n'
                            '2) Вывести курсы иностранных валют по определенной дате;\n'
                            '0) Выход;\n'
                            'Ваш выбор: ')
        if result == '1':
            check_input(method=output_course)
        elif result == '2':
            check_input(method=cross_course)
        elif result == '0':
            return


if __name__ == '__main__':
    reparse()
    menu()
