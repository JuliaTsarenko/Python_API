import pytest
import requests
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_fee')
class TestPayin:
    """ Payin currency. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payin_1(self):
        """ Payin from VISAMC 0.01 UAH by OWNER. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency='UAH', payway=admin.payway['visamc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency=admin.currency['UAH'], is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.01', 'in_curr': 'UAH',
                               'out_curr': 'UAH'})
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=0)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        assert user1.balance['UAH'] == '0.01'


    def test_payin_2(self):
        """ Payin from PAYEER 1.02 USD by MERCHANT. """
        admin.set_fee(currency='USD', payway=admin.payway['payeer']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency=admin.currency['UAH'], is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='payeer', amount='1.02', in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_create['account_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['out_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '0'

    def test_payin_3(self):
        """ Payin from BTC 0.99999 BTC by MERCHANT. """
        admin.set_fee(currency='BTC', payway=admin.payway['btc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['btc']['id'], currency=admin.currency['BTC'], is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        user1.merchant1.payin_create(payway='btc', amount='0.99999', in_curr='BTC', out_curr='BTC')
        assert user1.merchant1.resp_payin_create['account_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['in_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['out_amount'] == '0.99999'

    def test_payin_4(self):
        """ Payin from PRIVAT24 10 UAH by OWNER with common percent fee 15%. """
        admin.set_fee(currency='UAH', payway=admin.payway['privat24']['id'], tp=0, is_active=True, mult=pers(15))
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency=admin.currency['UAH'], is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(200))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10', 'in_curr': 'UAH',
                               'out_curr': 'UAH'})
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['in_fee_amount'] == '1.5'
        assert user1.resp_delegate['out_fee_amount'] == '1.5'

    def test_payin_5(self):
        """ Payin from LTC 0.5 LTC by MERCHANT with common absolute fee 0.001 LTC. """
        admin.set_fee(currency='LTC', payway=admin.payway['ltc']['id'], tp=0, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway['ltc']['id'], currency=admin.currency['LTC'], is_out=False, is_active=True,
                      tech_min=bl(0.4), tech_max=bl(200))
        user1.merchant1.payin_create(payway='ltc', amount='0.5', in_curr='LTC', out_curr='LTC')
        assert user1.merchant1.resp_payin_create['account_amount'] == '0.499'
        assert user1.merchant1.resp_payin_create['in_amount'] == '0.5'
        assert user1.merchant1.resp_payin_create['out_amount'] == '0.5'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '0.001'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '0.001'

    def test_payin_6(self):
        """ Payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency='RUB', payway=admin.payway['qiwi']['id'], tp=0, is_active=True, mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency=admin.currency['RUB'], is_out=False, is_active=True,
                      tech_min=bl(8.45), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'qiwi', 'amount': 10, 'in_curr': 'RUB',
                               'out_curr': 'RUB', 'userdata': {'payee': '', 'contact': '', 'payer': ''}})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=0)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        user1.merchant1.balance(curr='RUB')
        assert user1.merchant1.resp_balance['result']['RUB'] == '8.45'

    def test_payin_7(self, _custom_fee, _set_fee):
        """ Payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency='USD', payway=admin.payway['perfect']['id'], tp=0, is_active=True)
        admin.set_fee(currency='USD', payway=admin.payway['perfect']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency=admin.currency['USD'], is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.payin_create(payway='perfect', amount=10, in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_create['account_amount'] == '8.45'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=100)
        user1.merchant1.balance(curr='USD')
        assert user1.merchant1.resp_balance['result']['USD'] == '10.45'

    def test_payin_8(self, _custom_fee, _set_fee):
        """ Payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_fee(currency='USD', payway=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(10),
                      add=bl(2))
        admin.set_fee(currency='USD', payway=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'cash_kiev', 'amount': 10, 'in_curr': 'USD',
                               'out_curr': 'USD', 'userdata': {'payee': '', 'contact': '', 'payer': ''}})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'

    def test_payin_9(self):
        """ Payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'qiwi', 'amount': 50, 'in_curr': 'RUB',
                               'out_curr': 'UAH', 'userdata': {'payee': '', 'contact': '', 'payer': ''}})
        assert user1.resp_delegate['account_amount'] == '50'
        assert user1.resp_delegate['in_amount'] == '18.75'
        assert user1.resp_delegate['out_amount'] == '18.75'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_payin_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.id)
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_currency='USD', out_currency='UAH', merchant_id=user1.merchant1.id)
        user1.merchant1.payin_create(payway='payeer', amount=8.33, in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_payin_create['account_amount'] == '231.26'
        assert user1.merchant1.resp_payin_create['rate'] == ['1', '27.7628']
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.payin_lid, status=0)
        admin.set_order_status(lid=user1.payin_lid, status=100)
        user1.merchant1.balance(curr='RUB')
        assert user1.merchant1.resp_balance['result']['RUB'] == '231.26'

    def test_payin_11(self):
        pass


