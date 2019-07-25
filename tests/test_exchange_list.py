import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

class TestExchangeList:
    """ ExchangeList """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_ExchangeList_1(self):
        """ Exchange List. """
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43))
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(278907.43607), fee=0, in_currency='BTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(0.35851), is_active=False)
        admin.set_rate_exchange(rate=bl(6683.841), fee=0, in_currency='ETH', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(24.50656), fee=0, in_currency='USDT', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(4084.3), is_active=False)
        admin.set_rate_exchange(rate=bl(2542.69187), fee=0, in_currency='LTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04))
        admin.set_rate_exchange(rate=bl(724715.12064), fee=0, in_currency='BTC', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(0.13794), is_active=False)
        admin.set_rate_exchange(rate=bl(17065.28255), fee=0, in_currency='ETH', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(5.85537), is_active=False)
        admin.set_rate_exchange(rate=bl(62.65277), fee=0, in_currency='USDT', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(1596.89), is_active=False)
        admin.set_rate_exchange(rate=bl(6516.86546), fee=0, in_currency='LTC', out_currency='RUB',
                                tech_min=bl(0.002), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.04), in_currency='RUB', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.03), in_currency='BTC', out_currency='USD',
                                tech_min=0, tech_max=bl(3), is_active=False)
        admin.set_rate_exchange(rate=bl(273.49892), fee=0, in_currency='ETH', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(1.005), fee=0, in_currency='USDT', out_currency='USD',
                                tech_min=bl(0.02), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(104.01284), fee=0, in_currency='LTC', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.0005), in_currency='USD', out_currency='BTC',
                                tech_min=bl(1), tech_max=bl(2000), is_active=False)
        admin.set_rate_exchange(rate=bl(732822.1641), fee=0, in_currency='RUB', out_currency='BTC',
                                tech_min=bl(769.46), tech_max=bl(3869.63), is_active=False)
        admin.set_rate_exchange(rate=bl(280305.46835), fee=0, in_currency='UAH', out_currency='BTC',
                                tech_min=bl(294.32), tech_max=bl(1630.07), is_active=False)
        admin.set_rate_exchange(rate=bl(42.51193), fee=0, in_currency='ETH', out_currency='BTC',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(11580.45087), fee=0, in_currency='USDT', out_currency='BTC',
                                tech_min=bl(12.15), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(111.57669), fee=0, in_currency='LTC', out_currency='BTC',
                                tech_min=bl(0.0105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(104.8214), fee=0, in_currency='USD', out_currency='LTC',
                                tech_min=bl(0.11), tech_max=bl(61.45), is_active=False)
        admin.set_rate_exchange(rate=bl(6588.8146), fee=0, in_currency='RUB', out_currency='LTC',
                                tech_min=bl(13.2), tech_max=bl(65982.96), is_active=False)
        admin.set_rate_exchange(rate=bl(2784.58981), fee=0, in_currency='UAH', out_currency='LTC',
                                tech_min=bl(2.92), tech_max=bl(1631.31), is_active=False)
        admin.set_rate_exchange(rate=bl(110.86209), fee=0, in_currency='BTC', out_currency='LTC',
                                tech_min=bl(0.00009), tech_max=bl(0.09018), is_active=False)
        admin.set_rate_exchange(rate=bl(2.61242), fee=0, in_currency='ETH', out_currency='LTC',
                                tech_min=bl(0.0105), tech_max=bl(3.82964), is_active=False)
        admin.set_rate_exchange(rate=bl(120.41), fee=0, in_currency='USDT', out_currency='LTC',
                                tech_min=bl(0.12), tech_max=bl(35.75), is_active=False)
        assert user1.merchant1.exchange_list()['result'] == \
               {'RUB-UAH': {'fee': '0',
                            'i_rate': ['2.48757', '1'],
                            'in_curr': 'RUB',
                            'in_max': '100000',
                            'in_min': '0.03',
                            'out_curr': 'UAH',
                            'out_max': '40199.87',
                            'out_min': '0.01',
                            'rate': ['2.48757', '1'],
                            'ratesource': 'minfin'},
                'UAH-RUB': {'fee': '0',
                            'i_rate': ['1', '2.46305'],
                            'in_curr': 'UAH',
                            'in_max': '40700.04',
                            'in_min': '0.01',
                            'out_curr': 'RUB',
                            'out_max': '100246.23',
                            'out_min': '0.02',
                            'rate': ['1', '2.46305'],
                            'ratesource': 'minfin'},
                'UAH-USD': {'fee': '0.04',
                            'i_rate': ['25.91463', '1'],
                            'in_curr': 'UAH',
                            'in_max': '100000',
                            'in_min': '0.26',
                            'out_curr': 'USD',
                            'out_max': '3858.82',
                            'out_min': '0.01',
                            'rate': ['26.95122', '1'],
                            'ratesource': 'minfin'},
                'USD-UAH': {'fee': '0.03',
                            'i_rate': ['1', '25.7355'],
                            'in_curr': 'USD',
                            'in_max': '3886.43',
                            'in_min': '0.01',
                            'out_curr': 'UAH',
                            'out_max': '100019.21',
                            'out_min': '0.25',
                            'rate': ['1', '24.96343'],
                            'ratesource': 'minfin'}}

    def test_ExchangeList_2(self, _enable_exchange_operation_UAH_RUB, _enable_exchange_operation_UAH_USD,
                            _enable_exchange_operation_RUB_UAH, _enable_exchange_operation_USD_UAH):
        """ Exchange List. """
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43), is_active=False)
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000), is_active=False)
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04), is_active=False)
        user1.merchant1.exchange_list()
        # pprint.pprint(user1.merchant1.resp_exchange_list)
        assert user1.merchant1.resp_exchange_list['error']['message'] == 'NotFound'
        assert user1.merchant1.resp_exchange_list['error']['data']['reason'] == 'No exchange available'
