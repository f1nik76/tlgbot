import requests
import json
from config import keys


class ConvertExeption(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values_in: str, values_out: str, mount: str):
        if values_in == values_out:
            raise ConvertExeption(f'Нельзя конвертировать одинаковые валюты {values_in}')

        try:
            keys[values_in]
        except KeyError:
            raise ConvertExeption('Нет валюты которую вы хотите конвертировать')

        try:
            keys[values_out]
        except KeyError:
            raise ConvertExeption('Нет валюты в которой вы хотите получить результат')

        try:
            mount = float(mount)
        except ValueError:
            raise ConvertExeption('Количество валюты должно быть числом')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={keys[values_in]}&tsyms={keys[values_out]}')
        total = json.loads(r.content)[keys[values_out]]

        return total * mount
