import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

class TestCurrencyList:
    """ CurrencyList """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_CurrencyList_1(self):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='BTC', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='BCHABC', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='ETH', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='USDT', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='LTC', is_disabled=False, is_active=True)
        assert user1.merchant1.currency_list()['result'] == \
               {'BCHABC': {'admin_max': '3',
                           'admin_min': '0.000001',
                           'is_crypto': True,
                           'precision': 8},
                'BTC': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'ETH': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'LTC': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'RUB': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'UAH': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'USD': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'USDT': {'admin_max': '3',
                         'admin_min': '0.000001',
                         'is_crypto': True,
                         'precision': 8}}

    def test_CurrencyList_2(self, _enable_currency):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='BTC', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='BCHABC', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='ETH', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='USDT', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='LTC', is_disabled=False, is_active=False)
        user1.merchant1.currency_list()
        # pprint.pprint(user1.merchant1.resp_currency_list)
        assert user1.merchant1.resp_currency_list['error']['message'] == 'NotFound'
        assert user1.merchant1.resp_currency_list['error']['data']['reason'] == 'No currency available'

    def test_CurrencyList_3(self, _enable_currency):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='BTC', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='BCHABC', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='ETH', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='USDT', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='LTC', is_disabled=True, is_active=True)
        user1.merchant1.currency_list()
        # pprint.pprint(user1.merchant1.resp_currency_list)
        assert user1.merchant1.resp_currency_list['error']['message'] == 'NotFound'
        assert user1.merchant1.resp_currency_list['error']['data']['reason'] == 'No currency available'
