import pytest
import requests
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_operation_fee', '_personal_exchange_fee')
class TestPayin:
    """ Checking success payin . """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


    def test_payin_1(self):
        """ Payin from VISAMC 0.01 UAH by OWNER. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
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
        assert user1.merchant1.balance('UAH') == '0.01'


    def test_payin_2(self):
        """ Payin from PAYEER 1.02 USD by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='payeer', amount='1.02', in_curr='USD', out_curr=None)
        assert user1.merchant1.resp_payin_create['account_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['out_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '0'


    def test_payin_3(self):
        """ Payin from BTC 0.99999 BTC by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway['btc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['btc']['id'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        user1.merchant1.payin_create(payway='btc', amount='0.99999', in_curr='BTC', out_curr='BTC')
        assert user1.merchant1.resp_payin_create['account_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['in_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['out_amount'] == '0.99999'


    def test_payin_4(self):
        """ Payin from PRIVAT24 10 UAH by OWNER with common percent fee 15%. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(200))
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
        admin.set_fee(currency_id=admin.currency['LTC'], payway_id=admin.payway['ltc']['id'], tp=0, is_active=True,
                      add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway['ltc']['id'], currency='LTC', is_out=False, is_active=True,
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
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway['qiwi']['id'], tp=0, is_active=True,
                      mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(8.45), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'qiwi', 'amount': 10, 'in_curr': 'RUB',
                               'out_curr': None, 'contact': '123@gmail.com', 'payer': '+380663319145'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=0)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        assert user1.merchant1.balance('RUB') == '8.45'


    def test_payin_7(self, _custom_fee, _set_fee):
        """ Payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.payin_create(payway='perfect', amount='10', in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_create['account_amount'] == '8.45'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=100)
        assert user1.merchant1.balance('USD') == '10.45'


    def test_payin_8(self, _custom_fee, _set_fee):
        """ Payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway['cash_kiev']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(10),
                      add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'cash_kiev', 'amount': 10, 'in_curr': 'USD',
                               'out_curr': 'USD', 'contact': '@Bobik19'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'


    def test_payin_9(self):
        """ Payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'qiwi', 'amount': 50, 'in_curr': 'RUB',
                               'out_curr': 'UAH', 'contact': '123@gmail.com', 'payer': '+380663319145'})
        assert user1.resp_delegate['account_amount'] == '18.75'
        assert user1.resp_delegate['in_amount'] == '50'
        assert user1.resp_delegate['out_amount'] == '18.75'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_fee_amount'] == '0'


    def test_payin_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='USD', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.payin_create(payway='payeer', amount='8.33', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_payin_create['account_amount'] == '231.26'
        assert user1.merchant1.resp_payin_create['rate'] == ['1', '27.7628']
        assert user1.merchant1.resp_payin_create['in_amount'] == '8.33'
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=100)
        assert user1.merchant1.balance('UAH') == '231.26'


    def test_payin_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(115))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.payin_create(payway='privat24', amount='115', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_payin_create['account_amount'] == '3.78'
        assert user1.merchant1.resp_payin_create['rate'] == ['28.7639', '1']
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '0.21'
        assert user1.merchant1.resp_payin_create['in_amount'] == '115'
        assert user1.merchant1.resp_payin_create['out_amount'] == '3.99'
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=0)
        admin.set_order_status(lid=user1.merchant1.payin_lid, status=100)
        assert user1.merchant1.balance('USD') == '4.78'

    def test_payin_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway['btc']['id'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway['btc']['id'], tp=0, is_active=True,
                      mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway['btc']['id'], tp=0, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC',
                               'out_curr': 'USD'})
        assert user1.resp_delegate['rate'] == ['1', '3526.94428']
        assert user1.resp_delegate['account_amount'] == '22.8'
        assert user1.resp_delegate['out_amount'] == '23.63'
        assert user1.resp_delegate['in_fee_amount'] == '0.0002345'
        assert user1.resp_delegate['out_fee_amount'] == '0.83'


class TestWrongPayin:
    """ Testing bad payin. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_payin_1(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='visamc', amount='0.99', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooSmall'}

    def test_wrong_payin_2(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='privat24', amount='100.99', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooBig'}

    def test_wrong_payin_3(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.payin_create(payway='visamc', amount='4.99', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32075, 'message': 'AmountTooSmall'}
        user1.merchant1.payin_create(payway='visamc', amount='100.01', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32074, 'message': 'AmountTooBig'}

    def test_wrong_payin_4(self):
        """ Payin with not real currency. """
        user1.merchant1.payin_create(payway='privat24', amount='50', in_curr='UHA', out_curr='UHA')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_payin_5(self):
        """ Payin with not real payway. """
        user1.merchant1.payin_create(payway='visam', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_payin_6(self):
        """ Payin with deactivated pair CURRENCY : PAYWAY by pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=False,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32077, 'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))

    def test_wrong_payin_7(self):
        """ Payin with deactivated PAYWAY by payway table. """
        admin.set_payways(name='visamc', is_active=False, is_public=True)
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32060, 'data': 'visamc', 'message': 'InvalidPayway'}
        admin.set_payways(name='visamc', is_active=True, is_public=True)

    def test_wrong_payin_8(self):
        """ Payin with deactivated PAYWAY by pw_merchactive table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32060, 'data': 'visamc', 'message': 'InvalidPayway'}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)

    def test_wrong_payin_9(self):
        """ Payin with convert in to not active currency. """
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='BCHABC')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_payin_10(self):
        """ Payin with convert from not active currency. """
        admin.set_pwc(pw_id=admin.payway['bchabc']['id'], currency='BCHABC', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(2))
        user1.merchant1.payin_create(payway='bchabc', amount='0.5', in_curr='BCHABC', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_payin_11(self):
        """ Payin with convert by not active exchange pair. """
        admin.set_pwc(pw_id=admin.payway['bch']['id'], currency='BCH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='bch', amount='10', in_curr='BCH', out_curr='ETH')
        assert user1.merchant1.resp_payin_create == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_payin_12(self):
        """ Payin by not real pair payway+currency. """
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='qiwi', amount='10', in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'data': {'contact': None, 'payee': None,
                                                                              'payer': None, 'region': None},
                                                     'message': 'InvalidParam'}

    def test_wrong_payin_13(self):
        """ Payin without in_curr parameter. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.create' missing 1 argument: 'in_curr'"}}

    def test_wrong_payin_14(self):
        """ Payin without payway parameter. """
        data = {'method': 'payin.create',
                'params': {'amount': '10', 'in_curr': 'UAH',  'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.create' missing 1 argument: 'payway'"}}

    def test_wrong_payin_15(self):
        """ Payin without externalid parameter. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH',  'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.create' missing 1 argument: 'externalid'"}}

    def test_wrong_payin_16(self):
        """ Payin without amount parameter. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.create' missing 1 argument: 'amount'"}}

    def test_wrong_payin_17(self):
        """ Payin with wrong format amount. """
        user1.merchant1.payin_create(payway='visamc', amount='10.999', in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                     'data': ['10.999', 'UAH']}
        user1.merchant1.payin_create(payway='visamc', amount='String', in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                     'data': ['String', 'UAH']}
        user1.merchant1.payin_create(payway='visamc', amount=10, in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'int' type"}}
        user1.merchant1.payin_create(payway='visamc', amount=[1, 2], in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'list' type"}}
        user1.merchant1.payin_create(payway='visamc', amount={'1': 1}, in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'dict' type"}}
        user1.merchant1.payin_create(payway='visamc', amount='-10', in_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooSmall'}

    def test_wrong_payin_18(self):
        """ Payin with equal external_id. """
        ex_id = user1.merchant1._id()
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'payin.create',
                'params': {'amount': '50', 'in_curr': 'UAH', 'payway': 'visamc',
                           'externalid': ex_id},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        requests.post(url=user1.merchant1.japi_url, json=data,
                      headers={'x-merchant': str(user1.merchant1.lid),
                               'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                               'x-utc-now-ms': time_sent}, verify=False)
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32033, 'data': {'reason': 'Duplicated key for externalid'},
                                          'message': 'Unique'}

    def test_wrong_payin_19(self):
        """ Payin with wrong merchant. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant',
                                          'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_payin_20(self):
        """ Payin without merchant. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_payin_21(self):
        """ Payin with wrong sign. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': 'WRONG SIGN',
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign',
                                          'data': {'reason': 'Not correct signature'}}

    def test_wrong_payin_22(self):
        """ Payin without sign. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': 'WRONG SIGN',
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_payin_23(self):
        """ Payin without utc_time. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-utc-now-ms to headers'}}


class TestPayinParams:
    """ Testing payin params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


