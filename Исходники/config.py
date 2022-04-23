from collections import namedtuple

FILE_NAME_CONFIG = 'config.txt'

URL = 'https://old.cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=&UniDbQuery.FromDate=01.01.2000&UniDbQuery.ToDate=28.03.2020'

DATA = {'UniDbQuery.Posted': 'True',
        'UniDbQuery.mode': '1',
        'UniDbQuery.VAL_NM_RQ': 'R01720',
        'UniDbQuery.FromDate': '01.01.2000',
        'UniDbQuery.ToDate': '28.03.2020',}

HEADERS = {
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'cross-site',
           'sec-fetch-user': '?1',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
}

CURRENCY = {
            'Доллар': 'R01235',
            'Евро': 'R01239',
            'Гривна': 'R01720',
            'Швейцарский франк': 'R01775',
            'Белорусский рубль': 'R01090'
}

Course: namedtuple = namedtuple('Course', ('Date', 'for_value', 'ruble_value'))

AMOUNT_EQUELS = 50
