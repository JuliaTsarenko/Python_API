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
        assert user1.merchant1.balance(curr='UAH') == '11.5'

    def test_MerchantBalance_4(self, _enable_currency):
        """ Balance RUB сurrency is inactive. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
        assert user1.merchant1.balance(curr='RUB') == '1.02'

    def test_MerchantBalance_5(self, _enable_currency):
        """ Balance BCHABC сurrency off. """
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='BCHABC', is_disabled=True, is_active=True)
        assert user1.merchant1.balance(curr='BCHABC') == '250'

    def test_MerchantBalance_6(self):
        """ Balance non-existent currency. """
        assert user1.merchant1.balance(curr='TST')['error']['message'] == 'InvalidCurrency'


class TestIbillHistory:
    """ ibill_history """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Ibill count comparison. """
        admin_count = admin.get_ibill(merchant_id=user1.merchant1.id)['count']
        assert admin_count == user1.merchant1.ibill_history()['total']

    def test_2(self):
        """ Ibill [0] comparison. """
        ibill = user1.merchant1.ibill_history()['data'][0]
        assert admin.get_ibill(merchant_id=user1.merchant1.id, id=ibill['oid']) \
               != 'No ibills for this query.'

    def test_3(self):
        """ Begin filter test. Begin = ibill ctime """
        ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][0]
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(ibill['ctime']))['data'][0]
        assert test_ibill['ctime'] == ibill['ctime']

    def test_4(self):
        """ Begin filter test. Begin = ibill ctime -1 """
        ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][0]
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(ibill['ctime']-1))['data'][0]
        assert test_ibill['ctime'] >= ibill['ctime']

    # def test_5(self):
    #     """ Begin filter test. Begin = ibill ctime +1 """
    #     ibill = user1.merchant1.ibill_history(ord_by='ctime', curr='BTC', ord_dir=True, count='2')
    #     print('ib', ibill)
    #     ibill2 = user1.merchant1.ibill_history(ord_by='amount', ord_dir=False, count='2')['data']
    #     print('ib2', ibill2)
    #     print('\n')
    #     test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(ibill['ctime']+1))['data'][0]
    #     assert test_ibill['ctime'] >= ibill['ctime']

    def test_6(self):
        """ Success curr filter test. """
        curr = 'USD'
        ibill = user1.merchant1.ibill_history(curr=curr)['data'][0]
        assert ibill['curr'] == curr

    def test_7(self):
        """ Unknown curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.ibill_history(curr=curr)
        assert ibill['error'] == {'code': -32076, 'message': 'InvalidCurrency', 'data': curr}

    def test_8(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history()['data'][1]
        test_ibill = user1.merchant1.ibill_history(first='1')['data'][0]
        assert ibill == test_ibill

    def test_9(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first=1)
        assert ibill['error'] == {'code': -32070, 'message': 'InvalidParam', 'data':
            {'reason': "Key 'first' must not be of 'int' type"}}

    def test_10(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first='one')
        assert ibill['error'] == {'code': -32070, 'message': 'InvalidParam'}

    # def test_11(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first='9999999')['data']
        assert not ibill

    def test_12(self):
        """ Count filter test. """
        count = 10
        ibill = user1.merchant1.ibill_history(count=str(count))
        len = ibill['data'].__len__()
        assert len == count or len == ibill['total']
#
#     def test_13(self):
#         """ Count filter test. """ BBBBBBBBBUG
#         count = 0
#         ibill = user1.merchant1.ibill_history(count='0')
#         print(ibill)
#         # len = ibill['data'].__len__()
#         # assert len == count or len == ibill['total']



class TestOrderGet:
    """Order_get"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        print(admin.get_order(merchant_id=user1.merchant1.id))