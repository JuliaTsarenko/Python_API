import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

@pytest.mark.usefixtures('_sci_fee', '_personal_exchange_fee')
class TestSciRefundCreate:
    """ Create refund sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='USD', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='RUB', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='BTC', is_out=True, is_active=True,
                      tech_min=bl(0.000001), tech_max=bl(3))

    def test_sci_refund_create_1(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_create_2(self):
        """ Calc for sci_pay from PAYEER 1.02 USD by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(0.5), tech_max=bl(100))
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'contact': 'P14812343',
                               'm_lid': user1.merchant1.lid,  'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '0.52', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.52))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.52'
        assert user1.resp_delegate['in_amount'] == '0.52'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.52'
        assert user1.resp_delegate['out_amount'] == '0.52'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_create_3(self):
        """ Calc for sci_pay from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        # print('\n', 'user1.merchant1.id', user1.merchant1.id)
        # admin.create_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d',  'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.01))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.02999))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.02999'
        assert user1.resp_delegate['in_amount'] == '0.02999'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.02999'
        assert user1.resp_delegate['out_amount'] == '0.02999'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_create_4(self):
        """ Calc for sci_pay from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_wallet_amount(balance=bl(0), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(3), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['privat24'], is_active=True)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '3',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(3))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '9',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(12))
        user1.merchant1.balance(curr='UAH')
        # pprint.pprint(user1.merchant1.resp_balance)
        assert user1.merchant1.resp_balance['UAH'] == '8.5'
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_create_5(self):
        """ Calc for sci_pay from LTC 0.5 BTC by OWNER with common absolute fee 0.001 BTC. """
        admin.set_wallet_amount(balance=bl(0), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.5', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.4',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.4))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.1',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=100, amount_paid=bl(0.5))
        user1.merchant1.balance(curr='BTC')
        assert user1.merchant1.resp_balance['BTC'] == '0.499'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32002
        assert user1.resp_delegate['data']['value'] == f'{sci_pay_token}'
        assert user1.resp_delegate['data']['reason'] == 'Unable to complete: unavailable refund'
        assert user1.resp_delegate['message'] == 'EParamInvalid'

    def test_sci_refund_create_6(self):
        """ SCI payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1))
        admin.set_fee(currency_id=admin.currency['UAH'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'],
                      mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.05), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': None, 'payway': 'qiwi', 'externalid': user1.ex_id(), 'amount': '10',
                               'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'qiwi', 'amount': '4', 'in_curr': 'UAH', 'contact': '+123@gmail.com',
                               'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(4))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '2.78'
        assert user1.resp_delegate['in_amount'] == '4'
        assert user1.resp_delegate['in_fee_amount'] == '1.22'
        assert user1.resp_delegate['orig_amount'] == '4'
        assert user1.resp_delegate['out_amount'] == '2.78'
        assert user1.resp_delegate['out_fee_amount'] == '1.22'

    def test_sci_refund_create_7(self, _custom_fee, _set_fee):
        """ SCI payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'])
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, mult=pers(5.5), add=bl(1),
                      merchant_id=user1.merchant1.id, payway_id=admin.payway_id['anycash'])
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '10',
                                        'in_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '20',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(20))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['tp'] == 'sci_refund'
        # assert user1.merchant1.balance('USD') == '10.45'

    def test_sci_refund_create_8(self, _custom_fee, _set_fee):
        """ SCI payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'USD', 'expiry': '7d',  'externalid': user1.ex_id(), 'payway': 'cash_kiev',
                               'amount': '20', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD', 'contact': '@Bobik19'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(10))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '8.45'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['status'] == 'started'
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False,
                      merchant_id=user1.merchant1.id)

    def test_sci_refund_create_9(self):
        """ SCI payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_wallet_amount(balance=bl(100), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'UAH', 'expiry': '7d', 'externalid': user1.ex_id(), 'payway': 'qiwi',
                               'amount': '50', 'in_curr': 'RUB'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'qiwi', 'amount': '20',
                               'in_curr': 'RUB', 'contact': '@Bobik19', 'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(20))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '20'
        assert user1.resp_delegate['in_amount'] == '20'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['in_curr'] == 'RUB'
        assert user1.resp_delegate['orig_amount'] == '20'
        assert user1.resp_delegate['out_amount'] == '20'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == None

    def test_sci_refund_create_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '8.33',
                                        'in_curr': 'USD', 'out_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '16.66',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(16.66))
        # pprint.pprint(admin.resp_order_status)
        assert user1.merchant1.balance('UAH') == '231.26'
        # pprint.pprint(user1.merchant1.resp_balance)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'

    def test_sci_refund_create_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(120), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(120))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.01), tech_max=bl(120))
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '120',
                                        'in_curr': 'UAH', 'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '115',
                                           'in_curr': 'UAH', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(115))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '6.03'

    def test_sci_refund_create_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC',
                               'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.006',
                               'in_curr': 'BTC', 'contact': '+380661111111'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.006))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.00579'
        assert user1.resp_delegate['in_amount'] == '0.006'
        assert user1.resp_delegate['in_fee_amount'] == '0.00021'
        assert user1.resp_delegate['orig_amount'] == '0.006'
        assert user1.resp_delegate['out_amount'] == '0.00579'
        assert user1.resp_delegate['out_fee_amount'] == '0.00021'
        assert user1.resp_delegate['payway_name'] == 'anycash'

    def test_sci_refund_create_13(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=120, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

class TestWrongSciRefundCreate:
    """ Testing bad sci refund create request. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_wrong_sci_refund_create_1(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create',
                                params={'payway': 'visamc', 'amount': '0.99', 'in_curr': 'UAH',
                                        'externalid': user1.merchant1._id(), 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token, 'externalid': user1.ex_id(),
                                           'payway': 'visamc', 'amount': '0.09', 'in_curr': 'UAH',
                                           'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.09))
        user1.merchant1.sci_pay(method='get', params={'pay_token': str(user1.merchant1.sci_pay_token)})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['code'] == -32074
        assert user1.merchant1.resp_sci_refund['data']['field'] == 'amount'
        assert user1.merchant1.resp_sci_refund['data']['reason'] == 'Amount is too small'
        assert user1.merchant1.resp_sci_refund['data']['value'] == '0.09'
        assert user1.merchant1.resp_sci_refund['message'] == 'EParamAmountTooSmall'

    def test_wrong_sci_refund_create_2(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'payway': 'visamc', 'amount': '100', 'in_curr': 'UAH',
                                        'externalid': user1.merchant1._id(), 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token, 'externalid': user1.ex_id(),
                                           'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH',
                                           'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(50))
        user1.merchant1.sci_pay(method='get', params={'pay_token': str(user1.merchant1.sci_pay_token)})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(1), tech_max=bl(40))
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['code'] == -32073
        assert user1.merchant1.resp_sci_refund['data']['field'] == 'amount'
        assert user1.merchant1.resp_sci_refund['data']['reason'] == 'Amount is too big'
        assert user1.merchant1.resp_sci_refund['data']['value'] == '50'
        assert user1.merchant1.resp_sci_refund['message'] == 'EParamAmountTooBig'

    def test_wrong_sci_refund_create_3(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(4), tech_max=bl(100),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.sci_pay(method='create',
                                params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'USD',
                                        'externalid': user1.merchant1._id(), 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token, 'externalid': user1.ex_id(),
                                           'payway': 'visamc', 'amount': '54.99', 'in_curr': 'UAH',
                                           'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(4.99))
        user1.merchant1.sci_pay(method='get', params={'pay_token': str(user1.merchant1.sci_pay_token)})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['code'] == -32002
        assert user1.merchant1.resp_sci_refund['data']['field'] == 'pay_token'
        assert user1.merchant1.resp_sci_refund['data']['reason'] == 'Invalid pay_token value'
        assert user1.merchant1.resp_sci_refund['data']['value'] == f'{user1.merchant1.sci_pay_token}'
        assert user1.merchant1.resp_sci_refund['message'] == 'EParamInvalid'

    def test_wrong_sci_refund_create_4(self, _activate_pwcurrency):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=False,
                      tech_min=bl(0.01), tech_max=bl(3000))
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['code'] == -32033
        assert user1.merchant1.resp_sci_refund['data']['field'] == 'currency'
        assert user1.merchant1.resp_sci_refund['data']['reason'] == 'Inactive'
        assert user1.merchant1.resp_sci_refund['message'] == 'EStateCurrencyInactive'

    def test_wrong_sci_refund_create_5(self):
        """ Payin with wrong merchant. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        data = {'method': 'sci_refund.create',
                'params': {'sci_pay_token': user1.merchant1.sci_pay_token},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.content).
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['code'] == -32031
        assert loads(r.text)['error']['message'] == 'EStateMerchantInactive'
        assert loads(r.text)['error']['data']['field'] == 'x-merchant'
        assert loads(r.text)['error']['data']['reason'] == 'Merchant inactive'

    def test_wrong_sci_refund_create_6(self):
        """ Payin without merchant. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        data = {'method': 'sci_refund.create', 'params': {'sci_pay_token': user1.merchant1.sci_pay_token},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['code'] == -32012
        assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
        assert loads(r.text)['error']['data']['field'] == 'x-merchant'
        assert loads(r.text)['error']['data']['reason'] == 'Not present'

    def test_wrong_sci_refund_create_7(self):
        """ Payin with wrong sign. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        data = {'method': 'sci_refund.create', 'params': {'sci_pay_token': user1.merchant1.sci_pay_token},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['code'] == -32010
        assert loads(r.text)['error']['message'] == 'EParamSignInvalid'
        assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'

    def test_wrong_sci_refund_create_8(self):
        """ Payin without sign. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        data = {'method': 'sci_refund.create', 'params': {'sci_pay_token': user1.merchant1.sci_pay_token},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['code'] == -32012
        assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
        assert loads(r.text)['error']['data']['field'] == 'x-signature'
        assert loads(r.text)['error']['data']['reason'] == 'Not present'

    def test_wrong_sci_refund_create_9(self):
        """ Payin without utc_time. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        data = {'method': 'sci_refund.create', 'params': {'sci_pay_token': user1.merchant1.sci_pay_token},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['code'] == -32012
        assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
        assert loads(r.text)['error']['data']['field'] == 'x-utc-now-ms'
        assert loads(r.text)['error']['data']['reason'] == 'Not present'

@pytest.mark.usefixtures('_sci_fee', '_personal_exchange_fee')
class TestSciRefundCalc:
    """ Create refund sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='USD', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='BTC', is_out=True, is_active=True,
                      tech_min=bl(0.000001), tech_max=bl(3))

    def test_sci_refund_calc_1(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_calc_2(self):
        """ Refund for sci_pay from PAYEER 0.52 of 1.02 USD by OWNER. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(0.5), tech_max=bl(100))
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'contact': 'P14812343',
                               'm_lid': user1.merchant1.lid,  'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '0.52', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.52))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.52'
        assert user1.resp_delegate['in_amount'] == '0.52'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.52'
        assert user1.resp_delegate['out_amount'] == '0.52'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_calc_3(self):
        """ Calc for sci_pay from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        # print('\n', 'user1.merchant1.id', user1.merchant1.id)
        # admin.create_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d',  'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.01))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.02999))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.02999'
        assert user1.resp_delegate['in_amount'] == '0.02999'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.02999'
        assert user1.resp_delegate['out_amount'] == '0.02999'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_calc_4(self):
        """ Calc for sci_pay from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_wallet_amount(balance=bl(0), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=pers(15), add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_fee(mult=pers(15), add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_fee(mult=pers(15), add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(3), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['privat24'], is_active=True)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '3',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(3))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '9',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(12))
        user1.merchant1.balance(curr='UAH')
        # pprint.pprint(user1.merchant1.resp_balance)
        assert user1.merchant1.resp_balance['UAH'] == '8.5'
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '1.7'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0.3'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '1.7'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0.3'

    def test_sci_refund_calc_5(self):
        """ Calc for sci_pay from LTC 0.5 BTC by OWNER with common absolute fee 0.001 BTC. """
        admin.set_wallet_amount(balance=bl(0), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.5', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.4',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.4))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.1',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=100, amount_paid=bl(0.5))
        user1.merchant1.balance(curr='BTC')
        assert user1.merchant1.resp_balance['BTC'] == '0.499'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32002
        assert user1.resp_delegate['data']['reason'] == 'Unable to complete: unavailable refund'
        assert user1.resp_delegate['data']['value'] == f'{sci_pay_token}'
        assert user1.resp_delegate['message'] == 'EParamInvalid'

    def test_sci_refund_calc_6(self):
        """ SCI payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=pers(5.5), add=bl(1), _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_fee(mult=pers(5.5), add=bl(1), _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_fee(mult=pers(5.5), add=bl(1), _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.05), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': None, 'payway': 'qiwi', 'externalid': user1.ex_id(), 'amount': '10',
                               'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'qiwi', 'amount': '4', 'in_curr': 'UAH', 'contact': '+123@gmail.com',
                               'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(4))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '2.78'
        assert user1.resp_delegate['in_amount'] == '4'
        assert user1.resp_delegate['in_fee_amount'] == '1.22'
        assert user1.resp_delegate['orig_amount'] == '4'
        assert user1.resp_delegate['out_amount'] == '2.78'
        assert user1.resp_delegate['out_fee_amount'] == '1.22'

    def test_sci_refund_calc_7(self, _custom_fee, _set_fee):
        """ SCI payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'])
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, mult=pers(5.5), add=bl(1),
                      merchant_id=user1.merchant1.id, payway_id=admin.payway_id['anycash'])
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '10',
                                        'in_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '20',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(20))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '1.55'
        assert user1.merchant1.balance('USD') == '10.45'

    def test_sci_refund_calc_8(self, _custom_fee, _set_fee):
        """ SCI payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'USD', 'expiry': '7d',  'externalid': user1.ex_id(), 'payway': 'cash_kiev',
                               'amount': '20', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD', 'contact': '@Bobik19'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(10))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '8.45'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False,
                      merchant_id=user1.merchant1.id)

    def test_sci_refund_calc_9(self):
        """ SCI payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_wallet_amount(balance=bl(100), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'UAH', 'expiry': '7d', 'externalid': user1.ex_id(), 'payway': 'qiwi',
                               'amount': '50', 'in_curr': 'RUB'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'qiwi', 'amount': '20',
                               'in_curr': 'RUB', 'contact': '@Bobik19', 'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(20))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '20'
        assert user1.resp_delegate['in_amount'] == '20'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '20'
        assert user1.resp_delegate['out_amount'] == '20'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_calc_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '8.33',
                                        'in_curr': 'USD', 'out_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '16.66',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(16.66))
        # pprint.pprint(admin.resp_order_status)
        assert user1.merchant1.balance('UAH') == '231.26'
        # pprint.pprint(user1.merchant1.resp_balance)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_calc_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(120), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(120))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.01), tech_max=bl(120))
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '120',
                                        'in_curr': 'UAH', 'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '115',
                                           'in_curr': 'UAH', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(115))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '6.03'

    def test_sci_refund_calc_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC',
                               'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.006',
                               'in_curr': 'BTC', 'contact': '+380661111111'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.006))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'calc',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.00579'
        assert user1.resp_delegate['in_amount'] == '0.006'
        assert user1.resp_delegate['in_fee_amount'] == '0.00021'
        assert user1.resp_delegate['orig_amount'] == '0.006'
        assert user1.resp_delegate['out_amount'] == '0.00579'
        assert user1.resp_delegate['out_fee_amount'] == '0.00021'

    def test_sci_refund_calc_13(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=120, amount_paid=bl(0.5))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='calc', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

@pytest.mark.usefixtures('_sci_fee', '_personal_exchange_fee')
class TestSciRefundGet:
    """ Create refund sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='USD', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='BTC', is_out=True, is_active=True,
                      tech_min=bl(0.000001), tech_max=bl(3))

    def test_sci_refund_get_1(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_get_2(self):
        """ Calc for sci_pay from PAYEER 1.02 USD by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(0.5), tech_max=bl(100))
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'contact': 'P14812343',
                               'm_lid': user1.merchant1.lid,  'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '0.52', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.52))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        refund_token = user1.resp_delegate['token']
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.52'
        assert user1.resp_delegate['in_amount'] == '0.52'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.52'
        assert user1.resp_delegate['out_amount'] == '0.52'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': refund_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.52'
        assert user1.resp_delegate['in_amount'] == '0.52'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.52'
        assert user1.resp_delegate['out_amount'] == '0.52'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_get_3(self):
        """ Calc for sci_pay from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        # print('\n', 'user1.merchant1.id', user1.merchant1.id)
        # admin.create_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d',  'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.01))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.02999))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        refund_token = user1.resp_delegate['token']
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.02999'
        assert user1.resp_delegate['in_amount'] == '0.02999'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.02999'
        assert user1.resp_delegate['out_amount'] == '0.02999'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': refund_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.02999'
        assert user1.resp_delegate['in_amount'] == '0.02999'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.02999'
        assert user1.resp_delegate['out_amount'] == '0.02999'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_get_4(self):
        """ Calc for sci_pay from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_wallet_amount(balance=bl(0), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(3), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['privat24'], is_active=True)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '3',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(3))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '9',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(11))
        user1.merchant1.balance(curr='UAH')
        # pprint.pprint(user1.merchant1.resp_balance)
        assert user1.merchant1.resp_balance['UAH'] == '8.5'
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '1'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_get_5(self):
        """ Calc for sci_pay from LTC 0.5 BTC by OWNER with common absolute fee 0.001 BTC. """
        admin.set_wallet_amount(balance=bl(0), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.5', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.4',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.4))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.1',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=100, amount_paid=bl(0.5))
        user1.merchant1.balance(curr='BTC')
        assert user1.merchant1.resp_balance['BTC'] == '0.499'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        # print('\n', 'sci_pay_token', sci_pay_token)
        assert user1.resp_delegate['code'] == -32090
        assert user1.resp_delegate['message'] == 'EParamNotFound'
        assert user1.resp_delegate['data']['field'] == 'sci_pay_token'
        assert user1.resp_delegate['data']['reason'] == 'Not found'

    def test_sci_refund_get_6(self):
        """ SCI payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.05), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': None, 'payway': 'qiwi', 'externalid': user1.ex_id(), 'amount': '10',
                               'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'qiwi', 'amount': '4', 'in_curr': 'UAH', 'contact': '+123@gmail.com',
                               'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(4))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        refund_token = user1.resp_delegate['token']
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '4'
        assert user1.resp_delegate['in_amount'] == '4'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '4'
        assert user1.resp_delegate['out_amount'] == '4'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': refund_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '4'
        assert user1.resp_delegate['in_amount'] == '4'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '4'
        assert user1.resp_delegate['out_amount'] == '4'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_get_7(self, _custom_fee, _set_fee):
        """ SCI payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'])
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, mult=pers(5.5), add=bl(1),
                      merchant_id=user1.merchant1.id, payway_id=admin.payway_id['anycash'])
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '10',
                                        'in_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '20',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(20))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '1.55'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '1.55'

    def test_sci_refund_get_8(self, _custom_fee, _set_fee):
        """ SCI payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'USD', 'expiry': '7d',  'externalid': user1.ex_id(), 'payway': 'cash_kiev',
                               'amount': '20', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD', 'contact': '@Bobik19'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(10))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '8.45'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['status'] == 'started'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': user1.resp_delegate['token']})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '8.45'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['status'] == 'started'
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False,
                      merchant_id=user1.merchant1.id)

    def test_sci_refund_get_9(self):
        """ SCI payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_wallet_amount(balance=bl(100), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'UAH', 'expiry': '7d', 'externalid': user1.ex_id(), 'payway': 'qiwi',
                               'amount': '50', 'in_curr': 'RUB'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'qiwi', 'amount': '20',
                               'in_curr': 'RUB', 'contact': '@Bobik19', 'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(20))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '20'
        assert user1.resp_delegate['in_amount'] == '20'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['in_curr'] == 'RUB'
        assert user1.resp_delegate['orig_amount'] == '20'
        assert user1.resp_delegate['out_amount'] == '20'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == None
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': user1.resp_delegate['token']})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '20'
        assert user1.resp_delegate['in_amount'] == '20'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['in_curr'] == 'RUB'
        assert user1.resp_delegate['orig_amount'] == '20'
        assert user1.resp_delegate['out_amount'] == '20'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == None

    def test_sci_refund_get_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '8.33',
                                        'in_curr': 'USD', 'out_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '16.66',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(16.66))
        # pprint.pprint(admin.resp_order_status)
        assert user1.merchant1.balance('UAH') == '231.26'
        # pprint.pprint(user1.merchant1.resp_balance)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'

    def test_sci_refund_get_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(120), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(120))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.01), tech_max=bl(120))
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '120',
                                        'in_curr': 'UAH', 'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '115',
                                           'in_curr': 'UAH', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(115))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '6.03'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '6.03'

    def test_sci_refund_get_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC',
                               'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.006',
                               'in_curr': 'BTC', 'contact': '+380661111111'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.006))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_refund', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.00579'
        assert user1.resp_delegate['in_amount'] == '0.006'
        assert user1.resp_delegate['in_fee_amount'] == '0.00021'
        assert user1.resp_delegate['orig_amount'] == '0.006'
        assert user1.resp_delegate['out_amount'] == '0.00579'
        assert user1.resp_delegate['out_fee_amount'] == '0.00021'
        assert user1.resp_delegate['payway_name'] == 'anycash'
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_refund', 'merch_method': 'get',
                               'refund_token': user1.resp_delegate['token']})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.00579'
        assert user1.resp_delegate['in_amount'] == '0.006'
        assert user1.resp_delegate['in_fee_amount'] == '0.00021'
        assert user1.resp_delegate['orig_amount'] == '0.006'
        assert user1.resp_delegate['out_amount'] == '0.00579'
        assert user1.resp_delegate['out_fee_amount'] == '0.00021'
        assert user1.resp_delegate['payway_name'] == 'anycash'

    def test_sci_refund_get_13(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True,
                      mult=0, add=0, _min=0, _max=0)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True,
                      mult=0, add=0, _min=0, _max=0, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=0, add=0, _min=0, _max=0)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=0, add=0, _min=0, _max=0, merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=120, amount_paid=bl(0.5))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(user1.merchant1.sci_pay_lid)})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        user1.merchant1.sci_refund(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        user1.merchant1.sci_refund(method='get', params={'refund_token': user1.merchant1.resp_sci_refund['token']})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

@pytest.mark.usefixtures('_sci_fee', '_personal_exchange_fee')
class TestSciRefundParams:
    """ Create refund sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='USD', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='RUB', is_out=True, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='BTC', is_out=True, is_active=True,
                      tech_min=bl(0.000001), tech_max=bl(3))

    def test_sci_refund_params_1(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='params', params={'curr': 'UAH'})
        pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_create_2(self):
        """ Calc for sci_pay from PAYEER 1.02 USD by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(0.5), tech_max=bl(100))
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'contact': 'P14812343',
                               'm_lid': user1.merchant1.lid,  'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'payeer', 'amount': '0.52', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.52))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.52'
        assert user1.resp_delegate['in_amount'] == '0.52'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.52'
        assert user1.resp_delegate['out_amount'] == '0.52'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_create_3(self):
        """ Calc for sci_pay from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        # print('\n', 'user1.merchant1.id', user1.merchant1.id)
        # admin.create_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d',  'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01999', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.01))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx',
                               'payway': 'btc', 'amount': '0.01', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.02999))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.02999'
        assert user1.resp_delegate['in_amount'] == '0.02999'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.02999'
        assert user1.resp_delegate['out_amount'] == '0.02999'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_refund_create_4(self):
        """ Calc for sci_pay from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_wallet_amount(balance=bl(0), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(3), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['privat24'], is_active=True)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '3',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.resp_sci_subpay['token']})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(3))
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '9',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(12))
        user1.merchant1.balance(curr='UAH')
        # pprint.pprint(user1.merchant1.resp_balance)
        assert user1.merchant1.resp_balance['UAH'] == '8.5'
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '2'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'

    def test_sci_refund_create_5(self):
        """ Calc for sci_pay from LTC 0.5 BTC by OWNER with common absolute fee 0.001 BTC. """
        admin.set_wallet_amount(balance=bl(0), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(200))
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['btc'], is_active=True)
        user1.delegate(params={'externalid': user1.ex_id(), 'expiry': '7d', 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_pay', 'merch_method': 'create',
                               'payway': 'btc', 'amount': '0.5', 'in_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.4',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.4))
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.1',
                               'in_curr': 'BTC', 'contact': '32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=100, amount_paid=bl(0.5))
        user1.merchant1.balance(curr='BTC')
        assert user1.merchant1.resp_balance['BTC'] == '0.499'
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32002
        assert user1.resp_delegate['data']['value'] == f'{sci_pay_token}'
        assert user1.resp_delegate['data']['reason'] == 'Unable to complete: unavailable refund'
        assert user1.resp_delegate['message'] == 'EParamInvalid'

    def test_sci_refund_create_6(self):
        """ SCI payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1))
        admin.set_fee(currency_id=admin.currency['UAH'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'],
                      mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.05), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': None, 'payway': 'qiwi', 'externalid': user1.ex_id(), 'amount': '10',
                               'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'qiwi', 'amount': '4', 'in_curr': 'UAH', 'contact': '+123@gmail.com',
                               'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(4))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '2.78'
        assert user1.resp_delegate['in_amount'] == '4'
        assert user1.resp_delegate['in_fee_amount'] == '1.22'
        assert user1.resp_delegate['orig_amount'] == '4'
        assert user1.resp_delegate['out_amount'] == '2.78'
        assert user1.resp_delegate['out_fee_amount'] == '1.22'

    def test_sci_refund_create_7(self, _custom_fee, _set_fee):
        """ SCI payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, payway_id=admin.payway_id['anycash'])
        admin.set_fee(currency_id=admin.currency['USD'], tp=46, is_active=True, mult=pers(5.5), add=bl(1),
                      merchant_id=user1.merchant1.id, payway_id=admin.payway_id['anycash'])
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '10',
                                        'in_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'perfect', 'amount': '20',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(20))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '10'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.45'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_refund['tp'] == 'sci_refund'
        # assert user1.merchant1.balance('USD') == '10.45'

    def test_sci_refund_create_8(self, _custom_fee, _set_fee):
        """ SCI payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5.5), add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'USD', 'expiry': '7d',  'externalid': user1.ex_id(), 'payway': 'cash_kiev',
                               'amount': '20', 'in_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create',
                               'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD', 'contact': '@Bobik19'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(10))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '8.45'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['status'] == 'started'
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['anycash'], tp=46, is_active=False,
                      merchant_id=user1.merchant1.id)

    def test_sci_refund_create_9(self):
        """ SCI payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_wallet_amount(balance=bl(100), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'out_curr': 'UAH', 'expiry': '7d', 'externalid': user1.ex_id(), 'payway': 'qiwi',
                               'amount': '50', 'in_curr': 'RUB'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'qiwi', 'amount': '20',
                               'in_curr': 'RUB', 'contact': '@Bobik19', 'payer': '+380663319145'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(20))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '20'
        assert user1.resp_delegate['in_amount'] == '20'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['in_curr'] == 'RUB'
        assert user1.resp_delegate['orig_amount'] == '20'
        assert user1.resp_delegate['out_amount'] == '20'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == None

    def test_sci_refund_create_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '8.33',
                                        'in_curr': 'USD', 'out_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'payeer', 'amount': '16.66',
                                           'in_curr': 'USD', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=100, amount_paid=bl(16.66))
        # pprint.pprint(admin.resp_order_status)
        assert user1.merchant1.balance('UAH') == '231.26'
        # pprint.pprint(user1.merchant1.resp_balance)
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '8.33'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'USD'

    def test_sci_refund_create_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(120), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(120))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.01), tech_max=bl(120))
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '120',
                                        'in_curr': 'UAH', 'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '115',
                                           'in_curr': 'UAH', 'contact': '+380661111111'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=0, amount_paid=bl(115))
        user1.merchant1.sci_pay(method='get', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '115'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '108.97'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '6.03'

    def test_sci_refund_create_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['anycash'], tp=46, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC',
                               'out_curr': 'USD', 'expiry': '7d'})
        # pprint.pprint(user1.resp_delegate)
        sci_pay_lid = user1.resp_delegate['lid']
        sci_pay_token = user1.resp_delegate['token']
        user1.delegate(params={'sci_pay_token': sci_pay_token, 'externalid': user1.ex_id(), 'm_lid': user1.merchant1.lid,
                               'merch_model': 'sci_subpay', 'merch_method': 'create', 'payway': 'btc', 'amount': '0.006',
                               'in_curr': 'BTC', 'contact': '+380661111111'})
        # pprint.pprint(user1.resp_delegate)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        admin.set_order_status(lid=sci_pay_lid, status=0, amount_paid=bl(0.006))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_refund', 'merch_method': 'create',
                               'sci_pay_token': sci_pay_token})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.00579'
        assert user1.resp_delegate['in_amount'] == '0.006'
        assert user1.resp_delegate['in_fee_amount'] == '0.00021'
        assert user1.resp_delegate['orig_amount'] == '0.006'
        assert user1.resp_delegate['out_amount'] == '0.00579'
        assert user1.resp_delegate['out_fee_amount'] == '0.00021'
        assert user1.resp_delegate['payway_name'] == 'anycash'

    def test_sci_refund_create_13(self):
        """ Refund for sci_pay from VISAMC 0.5 of 1 UAH by MERCHANT. """
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=40, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=45, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=46, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['anycash']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01),
                      tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',
                                params={'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '1',
                                        'in_curr': 'UAH', 'expiry': '7d'})
        # pprint.pprint(user1.merchant1.resp_sci_pay)
        user1.merchant1.sci_subpay(method='create',
                                   params={'sci_pay_token': user1.merchant1.sci_pay_token,
                                           'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.5',
                                           'in_curr': 'UAH', 'contact': '4731185613244273'})
        # pprint.pprint(user1.merchant1.resp_sci_subpay)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.sci_subpay_lid, status=100)
        user1.merchant1.sci_subpay(method='get', params={'sci_subpay_token': user1.merchant1.sci_subpay_token})
        # print('\n', 'sci_subpay status', user1.merchant1.resp_sci_subpay['status'])
        admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=120, amount_paid=bl(0.5))
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        # admin.set_order_status(lid=user1.merchant1.sci_pay_lid, status=30, amount_paid=0.5)
        user1.merchant1.sci_pay(method='get', params={'pay_token': user1.merchant1.sci_pay_token})
        # print('\n', 'sci_pay status', user1.merchant1.resp_sci_pay['status'])
        user1.merchant1.sci_refund(method='create', params={'sci_pay_token': user1.merchant1.sci_pay_token})
        # pprint.pprint(user1.merchant1.resp_sci_refund)
        assert user1.merchant1.resp_sci_refund['account_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_refund['orig_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_refund['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_refund['out_fee_amount'] == '0'







