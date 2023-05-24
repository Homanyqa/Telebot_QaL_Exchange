import requests
import json
from config import keys

class APIException(Exception):
    pass


class Curr_Exchange:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        # quote_ticker, base_ticker = keys[quote], keys[base]
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Я не знаю такую валюту: "{base}". Попробуем еще раз?')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Я не знаю такую валюту: "{quote}". Попробуем еще раз?')

        if quote == base:
            raise APIException(f'Необходимо ввести различные валюты: "{base}". Попробуем еще раз?')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты: {amount}')

        if amount < 0:
            raise APIException(f'Количество валюты не может быть отрицательным. Попробуем еще раз?')

        if amount == 0:
            raise APIException(f'Ты вводишь количество валюты = {amount}. Так ничего не получится. Попробуем еще раз?')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]
        total_base *= amount
        return round(total_base, 2)