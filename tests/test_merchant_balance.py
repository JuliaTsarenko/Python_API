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
    """ Output """

    def MerchantBalance(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_MerchantBalance_1(self): # Перевод суммы равной сумме на счету списания
                             # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
        # print('lid', user1.merchant1.lid)
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))
