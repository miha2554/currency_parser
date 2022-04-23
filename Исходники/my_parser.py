from util import *
from typing import Dict
from requests import get


def get_request(currency_code: str) -> str:
    """
        Настраиваем хедеры и данные на отправку, получаем со всеми обработками (есть инет или нет, и так далее)
    """
    data: dict = DATA.copy()
    data.update({'UniDbQuery.VAL_NM_RQ': currency_code})
    url = URL[:149] + currency_code + URL[149:]
    try:
        request = get(url=url,
                      headers=HEADERS,
                      data=DATA)
    except:
        return ''
    else:
        return request.text if request.ok else ''


def parse() -> List[Dict[str, List[Course]]]:
    """
        Получаем данные с црб страницы, и пускаем их в обработку
    """
    currencies = []     # список в будущем со словарями где ключ название купюры значение - все курсы
    for title_curr, code_curr in CURRENCY.items():
        # sleep(1)
        html_code: str = get_request(currency_code=code_curr)
        if not html_code:
            print('Нет подключения или какие-то проблемы с доступом на сайт.')
        else:
            currencies.append({title_curr: cut_course(html_code=html_code)})
    return currencies


if __name__ == '__main__':
    parse()
