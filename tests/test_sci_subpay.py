import requests
import pytest
from json import loads
from users.tools import *
from users.sign import create_sign


class TestSciSubPayCreate:
    """ Checking calc sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_subpay_create_1(self):
        """ Creating SCI_SUBPAY with amount equal SCI_PAY amount. Payin 10 UAH from VISAMC. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'visamc',
                                                            'in_curr': 'UAH', 'amount': '10', 'externalid': user1.merchant1._id()})
        assert admin.get_model(model='order', _filter='lid', value=user1.merchant1.resp_sci_pay['lid'])[0]['status'] == 20
        assert user1.merchant1.resp_sci_subpay['account_amount'] == '10'
        assert user1.merchant1.resp_sci_subpay['in_amount'] == '10'
        assert user1.merchant1.resp_sci_subpay['out_amount'] == '10'

    def test_sci_subpay_create_2(self):
        """ Creating SCI_SUBPAY with amount more then SCI_PAY amount. Payin 10.01 UAH from VISAMC. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'RUB', 'out_curr': 'RUB',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_subpay', 'merch_method': 'create', 'in_curr': 'RUB',
                               'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'payeer', 'amount': '10.01',
                               'externalid': user1.merchant1._id()})
        assert user1.resp_delegate['account_amount'] == '10.01'
        assert user1.resp_delegate['in_amount'] == '10.01'
        assert user1.resp_delegate['out_amount'] == '10.01'
        assert user1.resp_delegate['tp'] == 'sci_subpay'

    def test_sci_subpay_create_3(self):
        """ Creating two SCI_SUBPAY from one SCI_PAY. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '11.66', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'visamc',
                                                            'in_curr': 'UAH', 'amount': '7.33'})
        sub_pay_order = admin.get_model(model='order', _filter='lid', value=user1.merhant1.resp_sci_sub_pay['lid'])
        assert user1.merchant1.resp_sci_subpay['account_amount'] == '7.33'
        assert sub_pay_order['tp'] == 45
        assert sub_pay_order['account_amount'] == bl(7.33)
        admin.set_order(lid=user1.merchant1.resp_sci_subpay['lid'], data={'status': 100})
        admin.set_order(lid=user1.merchant1.resp_sci_pay['lid'], data={'status': 0})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'privat24',
                                                            'in_curr': 'UAH', 'amount': '4.33'})
        assert user1.merchant1.resp_sci_subpay['in_amount'] == '4.33'
        assert user1.merchant1.resp_sci_subpay['out_amount'] == '4.33'

    def test_sci_subpay_create_4(self):
        """ Creating two SCI_SUBPAY from one SCI_PAY. """
        admin.set_wallet_amount(balance=0, currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.003), tech_max=bl(1))
        user1.merchant1.sci_pay(method='create', params={'payway': 'btc', 'amount': '0.5', 'in_curr': 'BTC', 'out_curr': 'BTC',
                                                         'externalid': user1.merchant1._id(), 'expiry': '100s'})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'btc',
                                                            'in_curr': 'BTC', 'amount': '0.33', 'contact': '@bobik19',
                                                            'externalid': user1.merchant1._id(), 'cheque': None, 'secret': None})
        assert user1.merchant1.resp_sci_subpay['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_subpay['out_fee_amount'] == '0'
        admin.set_order(lid=user1.merchant1.resp_sci_subpay['lid'], data={'status': 100})
        admin.set_order(lid=user1.merchant1.resp_sci_pay['lid'], data={'status': 0})
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'in_curr': 'BTC',
                               'sci_pay_token': user1.merchant1.resp_sci_pay['token'], 'payway': 'btc', 'amount': '0.1701',
                               'externalid': user1.merchant1._id()})
        assert user1.resp_delegate['account_amount'] == '0.1701'
        assert user1.resp_delegate['origin_amount'] == '0.1701'

    '''
    def test_sci_subpay_create_5(self):
        """ """
    '''





