import pytest
import requests
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_operation_fee', '_personal_exchange_fee')
class TestPayinCalc:
    """ Checking success payin calc. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payin_calc_1(self):
        """ Calc for payin from VISAMC 0.01 UAH by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(100))
        user1.merchant1.payin_calc(payway='visamc', amount='0.01', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc['account_amount'] == '0.01'
        assert user1.merchant1.resp_payin_calc['in_amount'] == '0.01'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '0.01'

    def test_payin_calc_2(self):
        """ Calc for payin from PAYEER 1.02 USD by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD', 'out_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '1.02'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_payin_calc_3(self):
        """ Calc for payin from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway['btc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['btc']['id'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC', 'out_curr': 'BTC'})
        assert user1.resp_delegate['account_amount'] == '0.99999'
        assert user1.resp_delegate['in_amount'] == '0.99999'
        assert user1.resp_delegate['out_amount'] == '0.99999'
        assert user1.resp_delegate['orig_amount'] == '0.99999'

    def test_payin_calc_4(self):
        """ Calc for payin from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(200))
        user1.merchant1.payin_calc(payway='privat24', amount='10', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc['account_amount'] == '8.5'
        assert user1.merchant1.resp_payin_calc['in_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['in_fee_amount'] == '1.5'
        assert user1.merchant1.resp_payin_calc['out_fee_amount'] == '1.5'

    def test_payin_calc_5(self):
        """ Calc for payin from LTC 0.5 LTC by OWNER with common absolute fee 0.001 LTC. """
        admin.set_fee(currency_id=admin.currency['LTC'], payway_id=admin.payway['ltc']['id'], tp=0, is_active=True,
                      add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway['ltc']['id'], currency='LTC', is_out=False, is_active=True,
                      tech_min=bl(0.4), tech_max=bl(200))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'ltc', 'amount': '0.5', 'in_curr': 'LTC', 'out_curr': 'LTC'})
        assert user1.resp_delegate['account_amount'] == '0.499'
        assert user1.resp_delegate['in_amount'] == '0.5'
        assert user1.resp_delegate['out_amount'] == '0.5'
        assert user1.resp_delegate['in_fee_amount'] == '0.001'
        assert user1.resp_delegate['out_fee_amount'] == '0.001'

    def test_payin_calc_6(self):
        """ Calc for payin from QIWI 10 RUB by MERCHANT with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway['qiwi']['id'], tp=0, is_active=True,
                      mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(8.45), tech_max=bl(1000))
        user1.merchant1.payin_calc(payway='qiwi', amount='10', in_curr='RUB', out_curr=None)
        assert user1.merchant1.resp_payin_calc['account_amount'] == '8.45'
        assert user1.merchant1.resp_payin_calc['in_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payin_calc['out_fee_amount'] == '1.55'

    def test_payin_calc_7(self, _custom_fee, _set_fee):
        """ Calc for payin from PERFECT 10 USD by OWNER with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'perfect', 'amount': '10', 'in_curr': 'USD', 'out_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'

    def test_payin_calc_8(self, _custom_fee, _set_fee):
        """ Payin from CASH_KIEV 10 USD by MERCHANT with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway['cash_kiev']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(10),
                      add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], tp=0, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        user1.merchant1.payin_calc(payway='cash_kiev', amount='10', in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_calc['account_amount'] == '8.45'
        assert user1.merchant1.resp_payin_calc['in_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '10'
        assert user1.merchant1.resp_payin_calc['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payin_calc['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payin_calc['orig_amount'] == '10'

    def test_payin_calc_9(self):
        """ Payin from QIWI 50 RUB by MERCHANT with exchange to UAH without any fee. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.merchant1.payin_calc(payway='qiwi', amount='50', in_curr='RUB', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc['account_amount'] == '18.75'
        assert user1.merchant1.resp_payin_calc['in_amount'] == '50'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '18.75'
        assert user1.merchant1.resp_payin_calc['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payin_calc['out_fee_amount'] == '0'

    def test_payin_calc_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from PAYEER 8.33 USD by OWNER with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='USD', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'payeer', 'amount': '8.33', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.resp_delegate['account_amount'] == '231.26'
        assert user1.resp_delegate['rate'] == ['1', '27.7628']
        assert user1.resp_delegate['in_amount'] == '8.33'
        assert user1.resp_delegate['orig_amount'] == '8.33'

    def test_payin_calc_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from PRIVAT24 115 UAH by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(115))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'calc',
                               'payway': 'privat24', 'amount': '115', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '3.78'
        assert user1.resp_delegate['rate'] == ['28.7639', '1']
        assert user1.resp_delegate['in_fee_amount'] == '6.03'
        assert user1.resp_delegate['out_fee_amount'] == '0.21'
        assert user1.resp_delegate['in_amount'] == '115'
        assert user1.resp_delegate['out_amount'] == '3.99'

    def test_payin_calc_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by MERCHANT with exchange to USD with common percent operation fee 5%
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
        user1.merchant1.payin_calc(payway='btc', amount='0.0067', in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_payin_calc['rate'] == ['1', '3526.94428']
        assert user1.merchant1.resp_payin_calc['account_amount'] == '22.8'
        assert user1.merchant1.resp_payin_calc['out_amount'] == '23.63'
        assert user1.merchant1.resp_payin_calc['in_fee_amount'] == '0.0002345'
        assert user1.merchant1.resp_payin_calc['out_fee_amount'] == '0.83'


class TestWrongPayinCalc:
    """ Testing bad payin calc request. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_payin_calc_1(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_calc(payway='visamc', amount='0.99', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '0.99'}}

    def test_wrong_payin_calc_2(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_calc(payway='privat24', amount='100.01', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_payin_calc_3(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.payin_calc(payway='visamc', amount='4.99', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_payin_calc == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '4.99'}}
        user1.merchant1.payin_calc(payway='visamc', amount='100.01', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_payin_calc == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_payin_calc_4(self):
        """ Payin with not real currency. """
        user1.merchant1.payin_calc(payway='privat24', amount='50', in_curr='UHA', out_curr='UHA')
        assert user1.merchant1.resp_payin_calc == {'code': -32076, 'message': 'InvalidCurrency', 'data': {'reason': 'UHA'}}

    def test_wrong_payin_calc_5(self):
        """ Payin with not real payway. """
        user1.merchant1.payin_calc(payway='visam', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visam is unknown'}}

    def test_wrong_payin_calc_6(self):
        """ Payin with deactivated pair CURRENCY : PAYWAY by pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=False,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_calc(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32077, 'data': {'reason': 'UAH is not active currently'},
                                                   'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))

    def test_wrong_payin_calc_7(self):
        """ Payin with deactivated PAYWAY by payway table. """
        admin.set_payways(name='visamc', is_active=False, is_public=True)
        user1.merchant1.payin_calc(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visamc is inactive'}}
        admin.set_payways(name='visamc', is_active=True, is_public=True)

    def test_wrong_payin_calc_8(self):
        """ Payin with deactivated PAYWAY by pw_merchactive table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        user1.merchant1.payin_calc(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32062, 'message': 'UnavailPayway',
                                                   'data': {'reason': 'Payway visamc is inactive for merchant'}}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_payin_calc_9(self):
        """ Payin with convert in to not active currency. """
        user1.merchant1.payin_calc(payway='visamc', amount='50', in_curr='UAH', out_curr='BCHABC')
        assert user1.merchant1.resp_payin_calc == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_payin_calc_10(self):
        """ Payin with convert from not active currency. """
        admin.set_pwc(pw_id=admin.payway['bchabc']['id'], currency='BCHABC', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(2))
        user1.merchant1.payin_calc(payway='bchabc', amount='0.5', in_curr='BCHABC', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_payin_calc_11(self):
        """ Payin with convert by not active exchange pair. """
        admin.set_pwc(pw_id=admin.payway['ltc']['id'], currency='LTC', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_calc(payway='ltc', amount='3', in_curr='LTC', out_curr='ETH')
        assert user1.merchant1.resp_payin_calc == {'code': -32065, 'message': 'UnavailExchange',
                                                     'data': {'reason': 'Unavailable excange for LTC to ETH'}}
    @pytest.mark.skip(reason='Not correct work')
    def test_wrong_payin_calc_12(self):
        """ Payin by not real pair payway+currency. """
        admin.set_pwc(pw_id=admin.payway['qiwi']['id'], currency='RUB', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_calc(payway='qiwi', amount='10', in_curr='USD', out_curr='USD')
        assert user1.merchant1.resp_payin_calc == {'code': -32070, 'data': {"reason": "Invalid data", "data": {}}, 'message': 'InvalidParam'}

    def test_wrong_payin_calc_13(self):
        """ Payin without in_curr parameter. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method payin.calc' missing 1 argument: 'in_curr'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_payin_calc_14(self):
        """ Payin without payway parameter. """
        data = {'method': 'payin.calc',
                'params': {'amount': '10', 'in_curr': 'UAH',  'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.calc' missing 1 argument: 'payway'"}}

    def test_wrong_payin_calc_15(self):
        """ Payin without amount parameter. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.calc' missing 1 argument: 'amount'"}}

    def test_wrong_payin_calc_16(self):
        """ Payin with wrong format amount. """
        user1.merchant1.payin_calc(payway='visamc', amount='10.999', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                   'data': {'reason': 'Invalid format 10.999 for UAH'}}
        user1.merchant1.payin_calc(payway='visamc', amount='String', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                   'data': {'reason': 'Invalid format String for UAH'}}
        user1.merchant1.payin_calc(payway='visamc', amount=10, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32070, 'message': 'InvalidParam',
                                                   'data': {'reason': "Key 'amount' must not be of 'int' type"}}
        user1.merchant1.payin_calc(payway='visamc', amount=[1, 2], in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32070, 'message': 'InvalidParam',
                                                   'data': {'reason': "Key 'amount' must not be of 'list' type"}}
        user1.merchant1.payin_calc(payway='visamc', amount={'1': 1}, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32070, 'message': 'InvalidParam',
                                                   'data': {'reason': "Key 'amount' must not be of 'dict' type"}}
        user1.merchant1.payin_calc(payway='visamc', amount='-10', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_calc == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '-10'}}

    def test_wrong_payin_calc_17(self):
        """ Payin with wrong merchant. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant',
                                          'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_payin_calc_18(self):
        """ Payin without merchant. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_payin_calc_19(self):
        """ Payin with wrong sign. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign',
                                          'data': {'reason': 'Invalid signature'}}

    def test_wrong_payin_calc_20(self):
        """ Payin without sign. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_payin_calc_21(self):
        """ Payin without utc_time. """
        data = {'method': 'payin.calc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-utc-now-ms to headers'}}

    def test_wrong_payin_calc_22(self):
        """ Request with not correct name method. """
        data = {'method': 'payin.calcc',
                'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32601, 'message': 'Method not found'}


@pytest.mark.usefixtures('_personal_operation_fee', '_personal_exchange_fee')
class TestPayinCreate:
    """ Checking success payin . """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


    def test_payin_create_1(self):
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


    def test_payin_create_2(self):
        """ Payin from PAYEER 1.02 USD by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='payeer', amount='1.02', in_curr='USD', out_curr=None)
        assert user1.merchant1.resp_payin_create['account_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['out_amount'] == '1.02'
        assert user1.merchant1.resp_payin_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_payin_create['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payin_create['out_fee_amount'] == '0'


    def test_payin_create_3(self):
        """ Payin from BTC 0.99999 BTC by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway['btc']['id'], tp=0, is_active=True)
        admin.set_pwc(pw_id=admin.payway['btc']['id'], currency='BTC', is_out=False, is_active=True,
                      tech_min=bl(0.0008), tech_max=bl(1))
        user1.merchant1.payin_create(payway='btc', amount='0.99999', in_curr='BTC', out_curr='BTC')
        assert user1.merchant1.resp_payin_create['account_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['in_amount'] == '0.99999'
        assert user1.merchant1.resp_payin_create['out_amount'] == '0.99999'


    def test_payin_create_4(self):
        """ Payin from PRIVAT24 10 UAH by OWNER with common percent fee 15%. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(200))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10', 'in_curr': 'UAH',
                               'out_curr': 'UAH'})
        assert user1.resp_delegate['account_amount'] == '8.5'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['in_fee_amount'] == '1.5'
        assert user1.resp_delegate['out_fee_amount'] == '1.5'


    def test_payin_create_5(self):
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


    def test_payin_create_6(self):
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


    def test_payin_create_7(self, _custom_fee, _set_fee):
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


    def test_payin_create_8(self, _custom_fee, _set_fee):
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


    def test_payin_create_9(self):
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


    def test_payin_create_10(self, _custom_fee, _disable_personal_exchange_fee):
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


    def test_payin_create_11(self, _custom_fee, _disable_personal_exchange_fee):
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

    def test_payin_create_12(self, _custom_fee, _disable_personal_exchange_fee):
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


class TestWrongPayinCreate:
    """ Testing bad payin create request. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_payin_1(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='visamc', amount='0.99', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '0.99'}}

    def test_wrong_payin_2(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='privat24', amount='100.01', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_payin_3(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.payin_create(payway='visamc', amount='4.99', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '4.99'}}
        user1.merchant1.payin_create(payway='visamc', amount='100.01', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_payin_create == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_payin_4(self):
        """ Payin with not real currency. """
        user1.merchant1.payin_create(payway='privat24', amount='50', in_curr='UHA', out_curr='UHA')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'message': 'InvalidCurrency', 'data': {'reason': 'UHA'}}

    def test_wrong_payin_5(self):
        """ Payin with not real payway. """
        user1.merchant1.payin_create(payway='visam', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visam is unknown'}}

    def test_wrong_payin_6(self):
        """ Payin with deactivated pair CURRENCY : PAYWAY by pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=False,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32077, 'data': {'reason': 'UAH is not active currently'}, 'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))

    def test_wrong_payin_7(self):
        """ Payin with deactivated PAYWAY by payway table. """
        admin.set_payways(name='visamc', is_active=False, is_public=True)
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visamc'}}
        admin.set_payways(name='visamc', is_active=True, is_public=True)

    def test_wrong_payin_8(self):
        """ Payin with deactivated PAYWAY by pw_merchactive table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32062, 'message': 'UnavailPayway',
                                                     'data': {'reason': 'Payway visamc is inactive for merchant'}}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)

    # @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_payin_9(self):
        """ Payin with convert in to not active currency. """
        user1.merchant1.payin_create(payway='visamc', amount='50', in_curr='UAH', out_curr='BCHABC')
        assert user1.merchant1.resp_payin_create == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    # @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_payin_10(self):
        """ Payin with convert from not active currency. """
        admin.set_pwc(pw_id=admin.payway['bchabc']['id'], currency='BCHABC', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(2))
        user1.merchant1.payin_create(payway='bchabc', amount='0.5', in_curr='BCHABC', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_payin_11(self):
        """ Payin with convert by not active exchange pair. """
        admin.set_pwc(pw_id=admin.payway['ltc']['id'], currency='LTC', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='ltc', amount='3', in_curr='LTC', out_curr='ETH')
        assert user1.merchant1.resp_payin_create == {'code': -32065, 'message': 'UnavailExchange',
                                                     'data': {'reason': 'Unavailable excange for LTC to ETH'}}
    @pytest.mark.skip(reason='Not correct work')
    def test_wrong_payin_12(self):
        """ Payin by not real pair payway+currency. """
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_create(payway='payeer', amount='10', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32076, 'data': {'reason': None}, 'message': 'InvalidCurrency'}

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
        user1.merchant1.payin_create(payway='visamc', amount='10.999', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                     'data': {'reason': 'Invalid format 10.999 for UAH'}}
        user1.merchant1.payin_create(payway='visamc', amount='String', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                     'data': {'reason': 'Invalid format String for UAH'}}
        user1.merchant1.payin_create(payway='visamc', amount=10, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'int' type"}}
        user1.merchant1.payin_create(payway='visamc', amount=[1, 2], in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'list' type"}}
        user1.merchant1.payin_create(payway='visamc', amount={'1': 1}, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': "Key 'amount' must not be of 'dict' type"}}
        user1.merchant1.payin_create(payway='visamc', amount='-10', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_create == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '-10'}}

    def test_wrong_payin_18(self):
        """ Payin with equal external_id. """
        ex_id = user1.merchant1._id()
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'sci_pay.create',
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
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_payin_22(self):
        """ Payin without sign. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_payin_23(self):
        """ Payin without utc_time. """
        data = {'method': 'payin.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id()},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-utc-now-ms to headers'}}


class TestPayinGet:
    """ Check getting order for payin. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payin_get_1(self):
        """ Getting last order by MERCHANT. """
        order = admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1]
        user1.merchant1.payin_get(o_lid=str(order['lid']))
        assert user1.merchant1.resp_payin_get['ctime'] == order['ctime']

    def test_payin_get_2(self):
        """ Getting order by OWNER. """
        order = admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[3]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'get', 'o_lid': str(order['lid'])})
        assert user1.resp_delegate['ctime'] == order['ctime']

    def test_payin_get_3(self):
        """ Checking all keys first level in response. """
        ls_key = ['account_amount', 'ctime', 'externalid', 'ftime', 'in_amount', 'in_curr', 'in_fee_amount', 'lid', 'orig_amount',
                  'out_amount', 'out_curr', 'out_fee_amount', 'owner', 'payway_name', 'rate', 'ref', 'renumeration', 'reqdata', 'status',
                  'tgt', 'token', 'tp', 'userdata']
        ls_key.sort()
        order = admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0, 'address_id': None})[2]
        user1.merchant1.payin_get(o_lid=str(order['lid']))
        us_ls = [dct for dct in user1.merchant1.resp_payin_get]
        us_ls.sort()
        print(ls_key, us_ls)
        assert us_ls == ls_key


@pytest.mark.usefixtures('_create_other_type_order')
class TestWrongPayinGet:
    """ Checking wrong requests for payin get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_payin_get_1(self):
        """ Getting order for not payin type. """
        order = admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 20})[1]
        user1.merchant1.payin_get(o_lid=str(order['lid']))
        assert user1.merchant1.resp_payin_get == {'code': -32090, 'data': {'reason': 'Not found order with params'}, 'message': 'NotFound'}

    def test_wrong_payin_get_2(self):
        """ Getting order by not own merchant. """
        order = admin.get_order({'merchant_id': user1.merchant2.id, 'tp': 0})[1]
        user1.merchant1.payin_get(o_lid=str(order['lid']))
        assert user1.merchant1.resp_payin_get == {'code': -32090, 'data': {'reason': 'Not found order with params'}, 'message': 'NotFound'}

    def test_wrong_payin_get_3(self, _merchant_activate):
        """ Getting order for not active merchant. """
        order = admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1]
        user1.merchant1.payin_get(o_lid=str(order['lid']))
        assert user1.merchant1.resp_payin_get == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_payin_get_4(self):
        """ Getting order with None lid. """
        user1.merchant1.payin_get(o_lid=None)
        assert user1.merchant1.resp_payin_get == {'code': -32070, 'data': {'reason': None}, 'message': 'InvalidParam'}

    def test_wrong_payin_get_5(self):
        """ Getting order without lid parameter. """
        data = {'method': 'payin.get',
                'params': {},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.get' missing 1 argument: 'o_lid'"}}

    def test_wrong_payin_get_6(self):
        """ Getting order with excess parameter 'par'. """
        data = {'method': 'payin.get',
                'params': {'o_lid': None, 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'payin.get' received a redundant argument 'par'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_payin_get_7(self):
        """ Getting order with not real merchant. """
        data = {'method': 'payin.get',
                'params': {'o_lid': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}


    def test_wrong_payin_get_8(self):
        """ Getting order with NONE merchant. """
        data = {'method': 'payin.get',
                'params': {'o_lid': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_get_9(self):
        """ Getting order without merchant in headers. """
        data = {'method': 'payin.get',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}


    def test_wrong_payin_get_10(self):
        """ Getting order with wrong signature. """
        data = {'method': 'payin.get',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_payin_get_11(self):
        """ Getting order with NONE signature. """
        data = {'method': 'payin.get',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_get_12(self):
        """ Getting order without x-signature parameter. """
        data = {'method': 'payin.get',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_get_13(self):
        """ Getting order without x-utc-now-ms parameter. """
        data = {'method': 'payin.get',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_get_14(self):
        """ Getting order with request for wrong method. """
        data = {'method': 'payin.gett',
                'params': {'o_lid': '15'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32601, 'message': 'Method not found'}


@pytest.mark.usefixtures('_personal_operation_fee', '_personal_exchange_fee')
class TestPayinParams:
    """ Testing payin params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payin_params_1(self):
        """ Getting params for UAH:VISAMC without exchange and without fee by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'], tp=0)
        user1.merchant1.payin_params(payway='visamc', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_params['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payin_params['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payin_params['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0',
                                                               'mult': '0'}
        assert user1.merchant1.resp_payin_params['min'] == '0.01'
        assert user1.merchant1.resp_payin_params['max'] == '3000'
        assert user1.merchant1.resp_payin_params['rate'] == ['1', '1']

    def test_payin_params_2(self):
        """ Getting params for RUB:PAYEER without exchange and without fee by owner."""
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'params',
                               'payway': 'payeer', 'in_curr': 'USD'})
        assert user1.resp_delegate['is_convert'] is False
        assert user1.resp_delegate['payway'] == 'payeer'
        assert user1.resp_delegate['out_curr'] == 'USD'

    def test_payin_params_3(self):
        """ Getting params for UAH:PRIVAT24 with exchange to USD with common exchange fee by OWNER. """
        admin.set_pwc(pw_id=admin.payway['privat24']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(1), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['privat24']['id'], tp=0)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'params',
                               'payway': 'privat24', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.resp_delegate['is_convert'] is True
        assert user1.resp_delegate['payway'] == 'privat24'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.4819', '1']

    def test_payin_params_4(self):
        """ Getting params for USD:PAYEER with exchange to UAH with common exchange fee 2% by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway['payeer']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(2), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['payeer']['id'], tp=0)
        user1.merchant1.payin_params(payway='payeer', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_payin_params['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_params['min'] == '20'
        assert user1.merchant1.resp_payin_params['max'] == '2000'
        # assert user1.merchant1.resp_payin_params['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0',
                                                                # 'mult': '0'}
        assert user1.merchant1.resp_payin_params['rate'] == ['1', '27.6359']

    def test_payin_params_5(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for USD:PERFECT with exchange to UAH with common exchange fee 4% with personal exchange fee
            2% by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0)
        user1.merchant1.payin_params(payway='perfect', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_payin_params['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_params['min'] == '20'
        assert user1.merchant1.resp_payin_params['max'] == '2000'
        assert user1.merchant1.resp_payin_params['rate'] == ['1', '27.6359']
        assert user1.merchant1.resp_payin_params['payway'] == 'perfect'

    def test_payin_params_6(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for UAH:VISAMC with exchange to RUB with common exchange fee 3% with personal exchange fee
            1% by OWNER. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(3), rate=bl(2.6666), in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(fee=pers(1), in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'], tp=0)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'params',
                               'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'RUB'})
        assert user1.resp_delegate['is_convert'] is True
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.63993']

    def test_payin_params_7(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for USD:PERFECT with exchange to UAH with common absolute fee 2 USD
            with common percent fee 5%, with personal absolute fee 1 USD with personal percent fee 3%,
            with exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True,
                      add=bl(2), mult=pers(5))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'], tp=0, is_active=True,
                      add=bl(1), mult=pers(3), merchant_id=user1.merchant1.id)
        user1.merchant1.payin_params(payway='perfect', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_payin_params['in_curr'] == 'USD'
        assert user1.merchant1.resp_payin_params['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payin_params['min'] == '11.35'
        assert user1.merchant1.resp_payin_params['max'] == '200'
        assert user1.merchant1.resp_payin_params['in_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0',
                                                               'mult': '0.03'}
        assert user1.merchant1.resp_payin_params['out_fee'] == {'add': '27.78', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.03'}
        assert user1.merchant1.resp_payin_params['rate'] == ['1', '27.7769']


class TestWrongParams:
    """ Testing wrong payin params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_params_1(self):
        """ Getting params for payin with not active pair PAYWAY + CURRENCY by PW_CURRENCY table. """
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=False,
                      tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.payin_params(payway='visamc', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_params == {'code': -32077, 'data': {'reason': 'UAH visamc'},
                                                     'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(150))

    def test_wrong_params_2(self):
        """ Getting params for payin with not active pair PAYWAY by PWMERCHACTIVE table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        user1.merchant1.payin_params(payway='visamc', in_curr='UAH')
        assert user1.merchant1.resp_payin_params == {'code': -32062, 'data': {'reason': 'Payway visamc is inactive for merchant'},
                                                     'message': 'UnavailPayway'}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)

    def test_wrong_params_3(self):
        """ Getting params for payin with not real in_curr. """
        user1.merchant1.payin_params(payway='visamc', in_curr='UHA')
        assert user1.merchant1.resp_payin_params == {'code': -32076, 'data': {'reason': 'UHA'}, 'message': 'InvalidCurrency'}

    def test_wrong_params_4(self):
        """ Getting params for payin with not real out_curr. """
        user1.merchant1.payin_params(payway='visamc', in_curr='UAH', out_curr='UDS')
        assert user1.merchant1.resp_payin_params == {'code': -32076, 'data': {'reason': 'UDS'},
                                                     'message': 'InvalidCurrency'}

    def test_wrong_params_5(self):
        """ Getting params for payin with not real payway. """
        user1.merchant1.payin_params(payway='visam', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_payin_params == {'code': -32060, 'data': {'reason': 'visam'}, 'message': 'InvalidPayway'}

    def test_wrong_params_6(self):
        """ Getting params for payin with not active exchange pair. """
        user1.merchant1.payin_params(payway='ltc', in_curr='LTC', out_curr='USDT')
        assert user1.merchant1.resp_payin_params == {'code': -32065,
                                                     'data': {'reason': 'Unavailable excange for LTC to USDT'}, 'message': 'UnavailExchange'}

    def test_wrong_params_7(self):
        """ Getting params for payin without in_curr parameter. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.params' missing 1 argument: 'in_curr'"}}

    def test_wrong_params_8(self):
        """ Getting params for payin without payway parameter. """
        data = {'method': 'payin.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.params' missing 1 argument: 'payway'"}}

    def test_wrong_params_9(self):
        """ Getting params for payin with existing parameter. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH', 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.params' received a redundant argument 'par'"}}

    def test_wrong_params_10(self):
        """ Getting params for payin with wrong merchant. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_params_11(self):
        """ Getting params for payin without merchant. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_params_12(self):
        """ Getting params for payin with wrong signature: Api Key from other user. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_params_13(self):
        """ Getting params for payin without signature. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_params_14(self):
        """ Getting params for payin with None x-utc-now-ms. """
        data = {'method': 'payin.params',
                'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_personal_operation_fee')
class TestChequeVerify:
    """ Testing cheque_verify method for different external pay systems. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_cheque_verify_1(self):
        """ Checking NOT ACCEPTED EXMO cheque  without fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], tp=0, is_active=True)
        user1.merchant1.cheque_verify(cheque='EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b')
        assert user1.merchant1.resp_cheque_verify == {'payway': 'exmo', 'can_be_accepted': 'unknown', 'currency': 'USD',
                                                      'fee': {'add': '0', 'max': '0', 'min': '0', 'mult': '0',
                                                              'method': 'ceil'}, 'fee_value': 'unknown'}

    def test_cheque_verify_2(self):
        """ Checking ACCEPTED KUNA cheque without fee by OWNER. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['kuna']['id'], tp=0, is_active=True)
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'payin', 'merch_method': 'cheque_verify',
                               'cheque': 'm1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UAH-KCode'})
        assert user1.resp_delegate == {'payway': 'kuna', 'can_be_accepted': 'no', 'currency': 'UAH', 'amount': '100.0',
                                       'fee': {'add': '0', 'max': '0', 'min': '0', 'mult': '0',
                                               'method': 'ceil'}, 'fee_value': '0'}

    def test_cheque_verify_3(self):
        """ Checking NOT ACCEPTED EXMO cheque  with common percent fee 3% and common absolute absolute fee 0.5 USD
            by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], tp=0,
                      add=bl(0.5), mult=pers(3), is_active=True)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'cheque_verify',
                               'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'})
        assert user1.resp_delegate == {'payway': 'exmo', 'can_be_accepted': 'unknown', 'currency': 'USD',
                                       'fee': {'add': '0.5', 'max': '0', 'min': '0', 'mult': '0.03',
                                               'method': 'ceil'}, 'fee_value': 'unknown'}

    def test_cheque_verify_4(self):
        """ Checking ACCEPTED KUNA cheque without common percent fee and common absolute absolute fee 0.33 UAH
                    by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway['kuna']['id'], tp=0,
                      add=bl(0.33), is_active=True)
        user1.merchant1.cheque_verify(cheque='m1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UAH-KCode')
        assert user1.merchant1.resp_cheque_verify == {'payway': 'kuna', 'can_be_accepted': 'no', 'currency': 'UAH',
                                                      'amount': '100.0',
                                                      'fee': {'add': '0.33', 'max': '0', 'min': '0', 'mult': '0',
                                                              'method': 'ceil'}, 'fee_value': '0.33'}

    def test_cheque_verify_5(self, _custom_fee, _set_fee):
        """ Checking NOT ACCEPTED EXMO cheque  with common percent fee 5% and common absolute absolute fee 1 USD,
            with personal percent fee 3% and personal absolute fee 0.5 USD by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], tp=0,
                      add=bl(1), mult=pers(5), is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], tp=0,
                      add=bl(0.5), mult=pers(3), is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.cheque_verify(cheque='EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b')
        assert user1.merchant1.resp_cheque_verify == {'payway': 'exmo', 'can_be_accepted': 'unknown', 'currency': 'USD',
                                                      'fee': {'add': '0.5', 'max': '0', 'min': '0', 'mult': '0.03',
                                                              'method': 'ceil'}, 'fee_value': 'unknown'}


class TestWrongVerifyCheque:
    """ Test wrong verify cheque. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_verify_cheque_1(self):
        """ Getting cheque info by deactivated pair currency:payway by pwcurrency table."""
        admin.set_pwc(pw_id=admin.payway['exmo']['id'], currency='USD', is_out=False, is_active=False,
                      tech_min=bl(10), tech_max=bl(200))
        user1.merchant1.cheque_verify(cheque='EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b')
        assert user1.merchant1.resp_cheque_verify == {'code': -32076, 'message': 'InvalidCurrency',
                                                      'data': {'reason': 'Unavailable payin in USD in exmo',
                                                               'data': ['USD', 'exmo']}}
        admin.set_pwc(pw_id=admin.payway['exmo']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(200))

    def test_wrong_verify_cheque_2(self):
        """ Getting cheque by not active merchant. """
        admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
        user1.merchant1.cheque_verify(cheque='EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b')
        assert user1.merchant1.resp_cheque_verify == {'code': -32010, 'message': 'InvalidMerchant',
                                                      'data': {'reason': 'Merchant Is Not Active'}}
        admin.set_merchant(lid=user1.merchant1.lid, is_active=True)

    def test_wrong_verify_cheque_3(self):
        """ Cheque wrong format. """
        user1.merchant1.cheque_verify(cheque='m1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UAH-KCod')
        assert user1.merchant1.resp_cheque_verify == {'code': -32082, 'message': 'InvalidChequeCode',
                                                      'data': {'reason': 'Invalid cheque m1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UAH-KCod'}}

    def test_wrong_verify_cheque_4(self):
        """ Cheque not real currency. """
        user1.merchant1.cheque_verify(cheque='m1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UHA-KCode')
        assert user1.merchant1.resp_cheque_verify == {'code': -32082, 'message': 'InvalidChequeCode',
                                                      'data': {'reason': 'Invalid cheque m1HuR-XYmg5-ZjLSV-R62TQ-p5YWW-mnajn-hXWTo-Yk4hE-LpJYT-UHA-KCode'}}

    def test_wrong_verify_cheque_5(self):
        """ Request with NONE cheque. """
        user1.merchant1.cheque_verify(cheque=None)
        assert user1.merchant1.resp_cheque_verify == {'code': -32070, 'message': 'InvalidParam', 'data': {'reason': 'Cheque is None'}}

    def test_wrong_verify_cheque_6(self):
        """ Request without cheque parameter. """
        data = {'method': 'payin.cheque_verify', 'params': {},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.cheque_verify' missing 1 argument: 'cheque'"}}

    def test_wrong_verify_cheque_7(self):
        """ Request with existing parameter. """
        data = {'method': 'payin.cheque_verify', 'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b', 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.cheque_verify' received a redundant argument 'par'"}}

    def test_wrong_verify_cheque_8(self):
        """ Request with wrong merchant. """
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'},
                                          'message': 'InvalidMerchant'}

    def test_wrong_verify_cheque_9(self):
        """ Request without merchant. """
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_verify_cheque_10(self):
        """ Request without signature. """
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                          'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_verify_cheque_11(self):
        """ Request with wrong signature: Api Key from other user. """
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign',
                                          'data': {'reason': 'Invalid signature'}}

    def test_wrong_verify_cheque_12(self):
        """ Request without utc-now parameter. """
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': 'EX-CODE_3298543_USDf95e835c8a4a7f9ecd3a0540a99f8ec89900a01b'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-utc-now-ms to headers'}}


@pytest.mark.usefixtures('_creating_payin_list')
class TestPayinList:
    """ Test payin list for merchant. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payin_list_1(self):
        """ Getting full list for payin by MERCHANT. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]]
        user1.merchant1.payin_list(in_curr=None, out_curr=None, payway=None, first=None, count=None)
        us_ls = [dct['lid'] for dct in user1.merchant1.resp_payin_list['data']]
        assert us_ls == adm_ls

    def test_payin_list_2(self):
        """ Getting lists from first 5 elements by OWNER. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]]
        adm_ls = adm_ls[:5]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'list', 'in_curr': None, 'out_curr': None,
                               'payway': None, 'first': None, 'count': '5'})
        us_ls = [dct['lid'] for dct in user1.resp_delegate['data']]
        assert us_ls == adm_ls

    @pytest.mark.skip
    def test_payin_list_3(self):
        """ Getting list from second element by MERCHANT to default end element - first 20 elements from second. """
        user1.merchant1.payin_list(in_curr=None, out_curr=None, payway=None, first='1', count=None)
        us_ls = [dct['lid'] for dct in user1.merchant1.resp_payin_list['data']]
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]]
        adm_ls = adm_ls[1:len(user1.merchant1.resp_payin_list['data'])+2]
        print(us_ls, adm_ls)
        assert us_ls == adm_ls

    def test_payin_list_4(self):
        """ Getting 4 elements from second to 5 by OWNER. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]]
        adm_ls = adm_ls[1:5]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'list', 'in_curr': None, 'out_curr': None,
                               'payway': None, 'first': '1', 'count': '4'})
        us_ls = [dct['lid'] for dct in user1.resp_delegate['data']]
        assert adm_ls == us_ls

    def test_payin_list_5(self):
        """ Getting 4 elements from second to 5 by MERCHANT with PAYWAY filter. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]
                  if dct['payway_id'] == admin.payway['visamc']['id']]
        adm_ls = adm_ls[1:5]
        user1.merchant1.payin_list(in_curr=None, out_curr=None, payway='visamc', first='1', count='4')
        us_ls = [dct['lid'] for dct in user1.merchant1.resp_payin_list['data']]
        assert us_ls == adm_ls

    def test_payin_list_6(self):
        """ Getting 4 elements from second to 5 by OWNER with PAYWAY and IN_CURR filter. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:]
                  if dct['payway_id'] == admin.payway['visamc']['id'] and dct['in_currency_id'] == admin.currency['UAH']]
        adm_ls = adm_ls[1:5]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'payin', 'merch_method': 'list', 'in_curr': 'UAH', 'out_curr': None,
                               'payway': 'visamc', 'first': '1', 'count': '4'})
        us_ls = [dct['lid'] for dct in user1.resp_delegate['data']]
        assert adm_ls == us_ls

    def test_payin_list_7(self):
        """ Getting 4 elements from second to 5 by MERCHANT with PAYWAY and IN_CURR filter and OUT_CURR filter. """
        adm_ls = [dct['lid'] for dct in admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})[1:] if
                  dct['payway_id'] == admin.payway['visamc']['id'] and dct['in_currency_id'] == admin.currency['UAH']
                  and dct['out_currency_id'] == admin.currency['USD']]
        adm_ls = adm_ls[1:5]
        user1.merchant1.payin_list(in_curr='UAH', out_curr='USD', payway='visamc', first='1', count='4')
        us_ls = [dct['lid'] for dct in user1.merchant1.resp_payin_list['data']]
        assert adm_ls == us_ls


class TestWrongPayinList:
    """ Wrong payin list requests testing. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_payin_list_1(self):
        """ Request with not str in parameter. """
        user1.merchant1.payin_list(in_curr='UAH', out_curr='USD', payway='visamc', first=1, count='4')
        assert user1.merchant1.resp_payin_list == {'code': -32070, 'data': {'reason': "Key 'first' must not be of 'int' type"},
                                                   'message': 'InvalidParam'}

    def test_wrong_payin_list_2(self):
        """ Request with not str count parameter. """
        user1.merchant1.payin_list(in_curr='UAH', out_curr='USD', payway='visamc', first='1', count=4)
        assert user1.merchant1.resp_payin_list == {'code': -32070, 'data': {'reason': "Key 'count' must not be of 'int' type"},
                                                   'message': 'InvalidParam'}

    def test_wrong_payin_list_3(self):
        """ Request with negative number in first parameter. """
        user1.merchant1.payin_list(in_curr='UAH', out_curr='USD', payway='visamc', first='-1', count='4')
        assert user1.merchant1.resp_payin_list == {'code': -32070, 'message': 'InvalidParam',
                                                   'data': {'reason': 'first: - has to be a positive number'}}

    def test_wrong_payin_list_4(self):
        """ Request with negative number in count parameter. """
        user1.merchant1.payin_list(in_curr='UAH', out_curr='USD', payway='visamc', first='1', count='-4')
        assert user1.merchant1.resp_payin_list == {'code': -32070, 'message': 'InvalidParam',
                                                   'data': {'reason': 'count: - has to be a positive number'}}

    def test_wrong_payin_list_5(self):
        """ Request with not real currency in in_curr parameter. """
        user1.merchant1.payin_list(in_curr='UHA', out_curr='USD', payway='visamc', first='1', count='4')
        assert user1.merchant1.resp_payin_list == {'code': -32076, 'data': {'reason': 'UHA'}, 'message': 'InvalidCurrency'}

    def test_wrong_payin_list_6(self):
        """ Request with not real currency in out_curr parameter. """
        user1.merchant1.payin_list(in_curr='UAH', out_curr='UDS', payway='visamc', first='1', count='4')
        assert user1.merchant1.resp_payin_list == {'code': -32076, 'data': {'reason': 'UDS'}, 'message': 'InvalidCurrency'}

    def test_wrong_payin_list_7(self):
        """ Request with existing parameter. """
        data = {'method': 'payin.list', 'params':  {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None, 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'payin.list' received a redundant argument 'par'"}}

    def test_wrong_payin_list_8(self):
        """ Request with wrong merchant. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_payin_list_9(self):
        """ Request with NONE merchant. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_list_10(self):
        """ Request without x-merchant parameter. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_list_11(self):
        """ Request with wrong sign: used api key from other user. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_payin_list_12(self):
        """ Request with NONE sign. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_list_13(self):
        """ Request without x-signature parameter. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_payin_list_14(self):
        """ Request without x-utc-now-ms parameter. """
        data = {'method': 'payin.list', 'params': {'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent)}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}



