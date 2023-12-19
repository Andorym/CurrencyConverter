import json  
import requests 
from config import keys  

class APIException(Exception):  
    pass


class CurrencyConverter: 
    @staticmethod  
    def get_price(quote: str, base: str, amount: str):
        if quote == base:  
            raise APIException(f'������ �������������� ���������� ������ {base}.')
        try:
            quote_ticker = keys[quote]  
        except KeyError:
            raise APIException(
                f'�� ������� ���������� ������ {quote}. �������� ��������� ������: {", ".join(keys.keys())}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(
                f'�� ������� ���������� ������ {base}. �������� ��������� ������: {", ".join(keys.keys())}')
        try:
            amount = float(amount)  
        except ValueError:
            raise APIException(f'�� ������� ���������� ���������� {amount}! ���������� ������ ���� ������.')

        try:
            response = requests.get(  
                f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}', timeout=15)
            print(response.status_code)  
            if response.status_code != 200:  
                raise Exception(
                    f'������ ��� ������� � �������. ��� ������: {response.status_code}. \n����������, ���������� �����')
            try:
                total_base = json.loads(response.content)[keys[base]]  
            except (json.JSONDecodeError, ValueError): 
                raise Exception(f'�� ������� ���������� ����� �� �������.')
        except requests.exceptions.ReadTimeout:  
            raise Exception('������: ��������� ����� �������� ������ �� �������. ��������� ������...')
            return CriptoConverter.get_price(quote, base, amount) 
        return total_base * round(amount, 2)  