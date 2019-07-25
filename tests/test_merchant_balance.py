import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

class TestMerchantBalance:
    """ Balance """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_MerchantBalance_1(self):
        """ Balance all. """
        admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='ETH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0), currency='USDT', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
        assert user1.merchant1.balance() == \
               {'USD': '1600', 'UAH': '11.5', 'RUB': '1.02', 'BCHABC': '250', 'ETH': '1', 'BTC': '0.99999', 'USDT': '0', 'LTC': '1'}

    def test_MerchantBalance_2(self):
        """ Balance USD. """
        admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
        # print(user1.merchant1.resp_balance)
        assert user1.merchant1.balance(curr='USD') == '1600'

    def test_MerchantBalance_3(self):
        """ Balance UAH. """
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.balance(curr='UAH') == '11.5'

    def test_MerchantBalance_4(self, _enable_currency):
        """ Balance RUB сurrency is inactive. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
        user1.merchant1.balance(curr='RUB') == '1.02'

    def test_MerchantBalance_5(self, _enable_currency):
        """ Balance BCHABC сurrency off. """
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='BCHABC', is_disabled=True, is_active=True)
        user1.merchant1.balance(curr='BCHABC') == '250'

    def test_MerchantBalance_6(self):
        """ Balance non-existent currency. """
        assert user1.merchant1.balance(curr='TST')['error']['message'] == 'InvalidCurrency'
