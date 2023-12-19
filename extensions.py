import json  
import requests 
from config import keys  

class APIException(Exception):  
    pass


class CurrencyConverter: 
    @staticmethod  
    def get_price(quote: str, base: str, amount: str):
        if quote == base:  
            raise APIException(f'Нельзя конвертировать одинаковую валюту {base}.')
        try:
            quote_ticker = keys[quote]  
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {quote}. Доступны следующие валюты: {", ".join(keys.keys())}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(
                f'Не удалось обработать валюту {base}. Доступны следующие валюты: {", ".join(keys.keys())}')
        try:
            amount = float(amount)  
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}! Количество должно быть числом.')

        try:
            response = requests.get(  
                f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}', timeout=15)
            print(response.status_code)  
            if response.status_code != 200:  
                raise Exception(
                    f'Ошибка при запросе к серверу. Код ошибки: {response.status_code}. \nПожалуйста, попробуйте позже')
            try:
                total_base = json.loads(response.content)[keys[base]]  
            except (json.JSONDecodeError, ValueError): 
                raise Exception(f'Не удалось обработать ответ от сервера.')
        except requests.exceptions.ReadTimeout:  
            raise Exception('Ошибка: превышено время ожидания ответа от сервера. Повторяем запрос...')
            return CriptoConverter.get_price(quote, base, amount) 
        return total_base * round(amount, 2)  