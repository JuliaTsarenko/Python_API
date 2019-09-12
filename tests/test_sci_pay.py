import requests
import pytest
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_sci_fee', '_personal_exchange_fee')
class TestSciPayCalc:
    """ Checking calc sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_pay_calc_1(self):
        """ Calc for sci_pay from VISAMC 0.01 UAH by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01), tech_max=bl(100))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '0.01', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '0.01'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '0.01'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '0.01'

    def test_sci_pay_calc_2(self):
        """ Calc for sci_pay from PAYEER 1.02 USD by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '1.02'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_pay_calc_3(self):
        """ Calc for sci_pay from BTC 0.99999 BTC by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.0008), tech_max=bl(1))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC', 'out_curr': 'BTC'})
        assert user1.resp_delegate['account_amount'] == '0.99999'
        assert user1.resp_delegate['in_amount'] == '0.99999'
        assert user1.resp_delegate['out_amount'] == '0.99999'
        assert user1.resp_delegate['orig_amount'] == '0.99999'

    def test_sci_pay_calc_4(self):
        """ Calc for sci_pay from PRIVAT24 10 UAH by MERCHANT with common percent fee 15. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(10),
                      tech_max=bl(200))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'privat24', 'amount': '10', 'in_curr': 'UAH'})
        # print(user1.merchant1.resp_sci_pay)
        assert user1.merchant1.resp_sci_pay['account_amount'] == '8.5'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '1.5'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '1.5'

    def test_sci_pay_calc_5(self):
        """ Calc for sci_pay from LTC 0.5 LTC by OWNER with common absolute fee 0.001 LTC. """
        admin.set_fee(currency_id=admin.currency['LTC'], payway_id=admin.payway_id['ltc'], tp=40, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway_id['ltc'], currency='LTC', is_out=False, is_active=True, tech_min=bl(0.4), tech_max=bl(200))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'ltc', 'amount': '0.5', 'in_curr': 'LTC', 'out_curr': 'LTC'})
        # print(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.499'
        assert user1.resp_delegate['in_amount'] == '0.5'
        assert user1.resp_delegate['out_amount'] == '0.5'
        assert user1.resp_delegate['in_fee_amount'] == '0.001'
        assert user1.resp_delegate['out_fee_amount'] == '0.001'

    def test_sci_pay_calc_6(self):
        """ Calc for sci_pay from QIWI 10 RUB by MERCHANT with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True, mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(8.45), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'qiwi', 'amount': '10', 'in_curr': 'RUB'})
        # print(user1.merchant1.resp_sci_pay)
        assert user1.merchant1.resp_sci_pay['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '1.55'

    def test_sci_pay_calc_7(self, _custom_fee, _set_fee):
        """ Calc for sci_pay from PERFECT 10 USD by OWNER with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'perfect', 'amount': '10', 'in_curr': 'USD', 'out_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'

    def test_sci_pay_calc_8(self, _custom_fee, _set_fee):
        """ Calc for sci_pay from CASH_KIEV 10 USD by MERCHANT with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True, mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='calc', params={'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '10'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_pay['orig_amount'] == '10'

    def test_sci_pay_calc_9(self):
        """ Calc for sci_pay from QIWI 50 RUB by MERCHANT with exchange to UAH without any fee. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.merchant1.sci_pay(method='calc', params={'payway': 'qiwi', 'amount': '50', 'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '18.75'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '50'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '18.75'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '0'

    def test_sci_pay_calc_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc for sci_pay from PAYEER 8.33 USD by OWNER with exchange to UAH with common exchange fee 3%, with personal exchange fee 1.55%. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'payeer', 'amount': '8.33', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.resp_delegate['account_amount'] == '231.26'
        assert user1.resp_delegate['rate'] == ['1', '27.7628']
        assert user1.resp_delegate['in_amount'] == '8.33'
        assert user1.resp_delegate['orig_amount'] == '8.33'

    def test_sci_pay_calc_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc for sci_pay from PRIVAT24 115 UAH by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False,
                      is_active=True, tech_min=bl(1), tech_max=bl(115))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True, mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'calc',
                               'payway': 'privat24', 'amount': '115', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '3.78'
        assert user1.resp_delegate['rate'] == ['28.7639', '1']
        assert user1.resp_delegate['in_fee_amount'] == '6.03'
        assert user1.resp_delegate['out_fee_amount'] == '0.21'
        assert user1.resp_delegate['in_amount'] == '115'
        assert user1.resp_delegate['out_amount'] == '3.99'

    def test_sci_pay_calc_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True, mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='calc', params={'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '3526.94428']
        assert user1.merchant1.resp_sci_pay['account_amount'] == '22.8'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '23.63'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '0.0002345'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '0.83'


class TestWrongCalcSciPay:
    """ Testing bad request sci_pay calc. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_pay_calc_1(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '0.99', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '0.99'}}

    def test_wrong_sci_pay_calc_2(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'privat24', 'amount': '100.01', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_sci_pay_calc_3(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100), in_currency='UAH', out_currency='USD')
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '4.99', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '4.99'}}
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '100.01', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_sci_pay_calc_4(self):
        """ Payin with not real currency. """
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '10', 'in_curr': 'UHA', 'out_curr': 'UHA'})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'message': 'InvalidCurrency', 'data': {'reason': 'UHA'}}

    def test_wrong_sci_pay_calc_5(self):
        """ Payin with not real payway. """
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visam', 'amount': '10', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visam is unknown'}}

    def test_wrong_sci_pay_calc_6(self):
        """ Payin with deactivated pair CURRENCY : PAYWAY by pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=False, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077, 'data': {'reason': 'UAH is not active currently'}, 'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))

    def test_wrong_sci_pay_calc_7(self):
        """ Payin with deactivated PAYWAY by payway table. """
        admin.set_payways(name='visamc', is_active=False, is_public=True)
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visamc is inactive'}}
        admin.set_payways(name='visamc', is_active=True, is_public=True)

    def test_wrong_sci_pay_calc_8(self):
        """ Payin with deactivated PAYWAY by pw_merchactive table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=False)
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32062, 'message': 'UnavailPayway',
                                                'data': {'reason': 'Payway visamc is inactive for merchant'}}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=True)

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_sci_pay_calc_9(self):
        """ Payin with convert in to not active currency. """
        user1.merchant1.sci_pay(method='calc', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'BCHABC'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_sci_pay_calc_10(self):
        """ Payin with convert by not active exchange pair. """
        admin.set_pwc(pw_id=admin.payway_id['ltc'], currency='LTC', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'ltc', 'amount': '3', 'in_curr': 'LTC', 'out_curr': 'ETH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32065, 'message': 'UnavailExchange',
                                                'data': {'reason': 'Unavailable excange for LTC to ETH'}}

    def test_wrong_sci_pay_calc_11(self):
        """ Payin by not real pair payway+currency. """
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='calc', params={'payway': 'qiwi', 'amount': '10', 'in_curr': 'USD', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {"reason": "Invalid data", "data": {}}, 'message': 'InvalidParam'}

    def test_wrong_sci_pay_calc_12(self):
        """ Payin without in_curr parameter. """
        user1.merchant1.sci_pay(method='calc', params={'payway': 'qiwi', 'amount': '20', 'out_curr': 'RUB'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'data': {'reason': "method 'sci_pay.calc' missing 1 argument: 'in_curr'"},
                                                'message': 'InvalidInputParams'}

    def test_wrong_sci_pay_calc_13(self):
        """ Payin without payway parameter. """
        user1.merchant1.sci_pay(method='calc', params={'amount': '10', 'in_curr': 'RUB', 'out_curr': 'RUB'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.calc' missing 1 argument: 'payway'"}}

    def test_wrong_sci_pay_calc_14(self):
        """ Payin without amount parameter. """
        user1.merchant1.sci_pay(method='calc', params={'payway': 'qiwi', 'in_curr': 'RUB', 'out_curr': 'RUB'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.calc' missing 1 argument: 'amount'"}}

    def test_wrong_sci_pay_calc_15(self):
        """ Payin with wrong format amount. """
        user1.merchant1.sci_pay(payway='visamc', amount='10.999', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                'data': {'reason': 'Invalid format 10.999 for UAH'}}
        user1.merchant1.sci_pay(payway='visamc', amount='String', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                'data': {'reason': 'Invalid format String for UAH'}}
        user1.merchant1.sci_pay(payway='visamc', amount=10, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'int' type"}}
        user1.merchant1.sci_pay(payway='visamc', amount=[1, 2], in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'list' type"}}
        user1.merchant1.sci_pay(payway='visamc', amount={'1': 1}, in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'dict' type"}}
        user1.merchant1.sci_pay(payway='visamc', amount='-10', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '-10'}}

    def test_wrong_sci_pay_calc_16(self):
        """ Payin with wrong merchant. """
        data = {'method': 'sci_pay.calc', 'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert user1.merchant1.resp_sci_pay == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_sci_pay_calc_17(self):
        """ Payin without merchant. """
        data = {'method': 'sci_pay.calc', 'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert user1.merchant1.resp_sci_pay == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_sci_pay_calc_18(self):
        """ Payin with wrong sign. """
        data = {'method': 'sci_pay.calc', 'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert user1.merchant1.resp_sci_pay == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_sci_pay_calc_19(self):
        """ Payin without sign. """
        data = {'method': 'sci_pay.calc', 'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert user1.merchant1.resp_sci_pay == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_sci_pay_calc_20(self):
        """ Payin without utc_time. """
        data = {'method': 'sci_pay.calc', 'params': {'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert user1.merchant1.resp_sci_pay == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-utc-now-ms to headers'}}


@pytest.mark.usefixtures('_personal_sci_fee', '_personal_exchange_fee')
class TestSciPayParams:
    """ Checking params sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_pay_params_1(self):
        """ Getting params for UAH:VISAMC without exchange and without fee by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40)
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_pay['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_pay['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user1.merchant1.resp_sci_pay['min'] == '0.01'
        assert user1.merchant1.resp_sci_pay['max'] == '3000'
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '1']

    def test_sci_pay_params_2(self):
        """ Getting params for RUB:PAYEER without exchange and without fee by owner."""
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'params',
                               'payway': 'payeer', 'in_curr': 'USD'})
        assert user1.resp_delegate['is_convert'] is False
        assert user1.resp_delegate['payway'] == 'payeer'
        assert user1.resp_delegate['out_curr'] == 'USD'

    def test_sci_pay_params_3(self):
        """ Getting params for UAH:PRIVAT24 with exchange to USD with common exchange fee by OWNER. """
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(1), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'params',
                               'payway': 'privat24', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.resp_delegate['is_convert'] is True
        assert user1.resp_delegate['payway'] == 'privat24'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.4819', '1']

    def test_sci_pay_params_4(self):
        """ Getting params for USD:PAYEER with exchange to UAH with common exchange fee 2% by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(2), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40)
        user1.merchant1.sci_pay(method='params', params={'payway': 'payeer', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_pay['min'] == '20'
        assert user1.merchant1.resp_sci_pay['max'] == '2000'
        assert user1.merchant1.resp_sci_pay['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '27.6359']

    def test_sci_pay_params_5(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for USD:PERFECT with exchange to UAH with common exchange fee 4% with personal exchange fee
            2% by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40)
        user1.merchant1.sci_pay(method='params', params={'payway': 'perfect', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_pay['min'] == '20'
        assert user1.merchant1.resp_sci_pay['max'] == '2000'
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '27.6359']
        assert user1.merchant1.resp_sci_pay['payway'] == 'perfect'

    def test_sci_pay_params_6(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for UAH:VISAMC with exchange to RUB with common exchange fee 3% with personal exchange fee
            1% by OWNER. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(20), tech_max=bl(2000))
        admin.set_rate_exchange(fee=pers(3), rate=bl(2.6666), in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(fee=pers(1), in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'params',
                               'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'RUB'})
        assert user1.resp_delegate['is_convert'] is True
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.63993']

    def test_sci_pay_params_7(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for USD:PERFECT with exchange to UAH with common absolute fee 2 USD
            with common percent fee 5%, with personal absolute fee 1 USD with personal percent fee 3%,
            with exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(10), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True, add=bl(2), mult=pers(5))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True,
                      add=bl(1), mult=pers(3), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='params', params={'payway': 'perfect', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_pay['out_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_pay['min'] == '11.35'
        assert user1.merchant1.resp_sci_pay['max'] == '200'
        assert user1.merchant1.resp_sci_pay['in_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.03'}
        assert user1.merchant1.resp_sci_pay['out_fee'] == {'add': '27.78', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.03'}
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '27.7769']


class TestWrongSciPayParams:
    """ Testing wrong sci_pay params request. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_pay_params_1(self):
        """ Getting params for payin with not active pair PAYWAY + CURRENCY by PW_CURRENCY table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=False, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077, 'data': {'reason': 'UAH visamc'}, 'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))

    def test_wrong_sci_pay_params_2(self):
        """ Getting params for payin with not active pair PAYWAY by PWMERCHACTIVE table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=False)
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32062, 'data': {'reason': 'Payway visamc is inactive for merchant'},
                                                'message': 'UnavailPayway'}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=True)

    def test_wrong_sci_pay_params_3(self):
        """ Getting params for payin with not real in_curr. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UHA', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'reason': 'UHA'}, 'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_params_4(self):
        """ Getting params for payin with not real out_curr. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UDS'})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'reason': 'UDS'}, 'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_params_5(self):
        """ Getting params for payin with not real payway. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'visam', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'data': {'reason': 'visam'}, 'message': 'InvalidPayway'}

    def test_wrong_sci_pay_params_6(self):
        """ Getting params for payin with not active exchange pair. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'ltc', 'in_curr': 'LTC', 'out_curr': 'USDT'})
        assert user1.merchant1.resp_sci_pay == {'code': -32065,
                                                'data': {'reason': 'Unavailable excange for LTC to USDT'}, 'message': 'UnavailExchange'}

    def test_wrong_sci_pay_params_7(self):
        """ Getting params for payin without in_curr parameter. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'out_curr': 'RUB'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.params' missing 1 argument: 'in_curr'"}}

    def test_wrong_sci_pay_params_8(self):
        """ Getting params for sci_pay without payway parameter. """
        user1.merchant1.sci_pay(method='params', params={'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.params' missing 1 argument: 'payway'"}}

    def test_wrong_sci_pay_params_9(self):
        """ Getting params for sci_pay with existing parameter. """
        user1.merchant1.sci_pay(method='params', params={'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'USD', 'par': '123'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'payin.params' received a redundant argument 'par'"}}

    def test_wrong_sci_pay_params_10(self):
        """ Getting params for sci_pay with wrong merchant. """
        data = {'method': 'sci_pay.params', 'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_sci_pay_params_11(self):
        """ Getting params for payin without merchant. """
        data = {'method': 'sci_pay.params', 'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_params_12(self):
        """ Getting params for payin with wrong signature: Api Key from other user. """
        data = {'method': 'sci_pay.params', 'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_sci_pay_params_13(self):
        """ Getting params for payin without signature. """
        data = {'method': 'sci_pay.params', 'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_params_14(self):
        """ Getting params for payin with None x-utc-now-ms. """
        data = {'method': 'sci_pay.params', 'params': {'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_create_sci_pay_order')
class TestSciPayGet:
    """ Testing sci pay get. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_pay_get_1(self):
        """ Getting last order by MERCHANT. """
        order = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_sci_pay['ctime'] == order['ctime']
        assert admin.payway_id[user1.merchant1.resp_sci_pay['payway_name']] == order['payway_id']

    def test_sci_pay_get_2(self):
        """ Getting order by OWNER. """
        order = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'get', 'o_lid': str(order['lid'])})
        assert user1.resp_delegate['lid'] == order['lid']
        assert user1.resp_delegate['tp'] == 'sci_pay'
        assert 'status' in user1.resp_delegate


@pytest.mark.usefixtures('_create_other_type_order')
class TestWrongSciPayGet:
    """ Wrong requests to sci_pay get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_get_1(self):
        """ Getting sci order for not sci_pay type. """
        order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 20][0]
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_sci_pay == {'code': -32090, 'data': {'reason': 'No order found with such params'}, 'message': 'NotFound'}

    def test_wrong_sci_pay_get_2(self):
        """ Getting sci order by not own merchant. """
        order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant2.id)][0]
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_sci_pay == {'code': -32090, 'data': {'reason': 'No order found with such params'}, 'message': 'NotFound'}

    def test_wrong_sci_pay_get_3(self, _merchant_activate):
        """ Getting sci order for not active merchant. """
        order = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_sci_pay == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_sci_pay_get_4(self):
        """ Getting sci order with None lid. """
        user1.merchant1.sci_pay(method='get', params={'o_lid': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'reason': None}, 'message': 'InvalidParam'}

    def test_wrong_sci_pay_get_5(self):
        """ Getting sci order without lid parameter. """
        user1.merchant1.sci_pay(method='get', params={})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.get' missing 1 argument: 'o_lid'"}}

    def test_wrong_sci_pay_get_6(self):
        """ Getting order with excess parameter 'par'. """
        order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)][0]
        user1.merchant1.sci_pay(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'data': {'reason': "method 'sci.get' received a redundant argument 'par'"},
                                                'message': 'InvalidInputParams'}

    def test_wrong_sci_pay_get_7(self):
        """ Getting order with not real merchant. """
        data = {'method': 'sci_pay.get', 'params': {'o_lid': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_sci_pay_get_8(self):
        """ Getting order with NONE merchant. """
        data = {'method': 'sci_pay.get', 'params': {'o_lid': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_get_9(self):
        """ Getting order with wrong sign in headers. """
        data = {'method': 'sci_pay.get', 'params': {'o_lid': '15'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.id,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_sci_pay_get_10(self):
        """ Getting order with NONE signature. """
        data = {'method': 'payin.get', 'params': {'o_lid': '15'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid), 'x-signature': None, 'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_get_11(self):
        """ Getting order without x-utc-now-ms parameter. """
        data = {'method': 'payin.get', 'params': {'o_lid': '15'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_personal_sci_fee', '_personal_exchange_fee')
class TestSciPayCreate:
    """ Test Sci_pay_creating. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


    def test_sci_pay_create_1(self):
        """ SCI payin from VISAMC 0.01 UAH by OWNER. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(0.01), tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'sci_pay', 'merch_method': 'create', 'in_curr': 'UAH',
                               'externalid': user1.ex_id(), 'payway': 'visamc', 'amount': '0.01', 'expiry': '60s', 'out_curr': 'UAH'})
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=0)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        assert user1.merchant1.balance('UAH') == '0.01'


    def test_sci_pay_create_2(self):
        """ SCI payin from PAYEER 1.02 USD by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create',  params={'payway': 'payeer', 'amount': '1.02', 'in_curr': 'USD', 'out_curr': None,
                                                          'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '1.02'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '1.02'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '1.02'
        assert user1.merchant1.resp_sci_pay['in_curr'] == 'USD'
        assert user1.merchant1.resp_sci_pay['out_curr'] == 'USD'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '0'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '0'


    def test_sci_pay_create_3(self):
        """ SCI payin from BTC 0.99999 BTC by MERCHANT. """
        admin.set_wallet_amount(balance=0, currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.0008), tech_max=bl(1))
        user1.merchant1.sci_pay(method='create',  params={'payway': 'btc', 'amount': '0.99999', 'in_curr': 'BTC', 'out_curr': 'BTC',
                                                          'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '0.99999'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '0.99999'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '0.99999'
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=0)
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=100)
        assert user1.merchant1.balance('BTC') == '0.99999'


    def test_sci_pay_create_4(self):
        """ SCI payin from PRIVAT24 10 UAH by OWNER with common percent fee 15%. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True, mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(10), tech_max=bl(200))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create', 'out_curr': 'UAH',
                               'externalid': user1.ex_id(), 'payway': 'privat24', 'amount': '10', 'in_curr': 'UAH', 'expiry': '1000s' })
        assert user1.resp_delegate['account_amount'] == '8.5'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['in_fee_amount'] == '1.5'
        assert user1.resp_delegate['out_fee_amount'] == '1.5'


    def test_sci_pay_create_5(self):
        """ SCI payin from LTC 0.5 LTC by MERCHANT with common absolute fee 0.001 LTC. """
        admin.set_fee(currency_id=admin.currency['LTC'], payway_id=admin.payway_id['ltc'], tp=40, is_active=True, add=bl(0.001))
        admin.set_pwc(pw_id=admin.payway_id['ltc'], currency='LTC', is_out=False, is_active=True, tech_min=bl(0.4), tech_max=bl(200))
        user1.merchant1.sci_pay(method='create',  params={'payway': 'ltc', 'amount': '0.5', 'in_curr': 'LTC', 'out_curr': 'LTC',
                                                          'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '0.499'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '0.5'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '0.5'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '0.001'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '0.001'

    def test_sci_pay_create_6(self):
        """ SCI payin from QIWI 10 RUB by OWNER with common absolute fee 1 RUB and common percent fee 5.5% . """
        admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True, mult=pers(5.5), add=bl(1))
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(8.45), tech_max=bl(1000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create', 'out_curr': None, 'payway': 'qiwi',
                               'externalid': user1.ex_id(), 'amount': '10', 'in_curr': 'RUB', 'expiry': '100s'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=0)
        admin.set_order_status(lid=user1.resp_delegate['lid'], status=100)
        assert user1.merchant1.balance('RUB') == '8.45'


    def test_sci_pay_create_7(self, _custom_fee, _set_fee):
        """ SCI payin from PERFECT 10 USD by MERCHANT with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=40, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(1000))
        user1.merchant1.sci_pay(method='create',  params={'payway': 'perfect', 'amount': '10', 'in_curr': 'USD', 'out_curr': 'USD',
                                                          'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '8.45'
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_sci_pay['tp'] == 'sci_pay'
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=0)
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=100)
        assert user1.merchant1.balance('USD') == '10.45'

    def test_sci_pay_create_8(self, _custom_fee, _set_fee):
        """ SCI payin from CASH_KIEV 10 USD by OWNER with common absolute fee 2 USD and common percent fee 10%,
            with personal absolute fee 1 USD and personal percent fee 5.5%. """
        admin.set_pwc(pw_id=admin.payway_id['cash_kiev'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True, mult=pers(10), add=bl(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['cash_kiev'], tp=40, is_active=True, mult=pers(5.5),
                      add=bl(1), merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create', 'out_curr': 'USD', 'expiry': '60s',
                               'externalid': user1.ex_id(), 'payway': 'cash_kiev', 'amount': '10', 'in_curr': 'USD'})
        assert user1.resp_delegate['account_amount'] == '8.45'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['tp'] == 'sci_pay'

    def test_sci_pay_create_9(self):
        """ SCI payin from QIWI 50 RUB by OWNER with exchange to UAH without any fee. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(2.6666), in_currency='RUB', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create', 'out_curr': 'UAH', 'expiry': '60s',
                               'externalid': user1.ex_id(), 'payway': 'qiwi', 'amount': '50', 'in_curr': 'RUB'})
        assert user1.resp_delegate['account_amount'] == '18.75'
        assert user1.resp_delegate['in_amount'] == '50'
        assert user1.resp_delegate['out_amount'] == '18.75'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_fee_amount'] == '0'

    def test_sci_pay_create_10(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PAYEER 8.33 USD by MERCHANT with exchange to UAH with common exchange fee 3%,
            with personal exchange fee 1.55%. """
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=40, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(3), rate=bl(28.1999), in_currency='USD', out_currency='UAH')
        admin.set_personal_exchange_fee(fee=pers(1.55), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '8.33', 'in_curr': 'USD', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '231.26'
        assert user1.merchant1.resp_sci_pay['rate'] == ['1', '27.7628']
        assert user1.merchant1.resp_sci_pay['in_amount'] == '8.33'
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=0)
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=100)
        assert user1.merchant1.balance('UAH') == '231.26'

    def test_sci_pay_create_11(self, _custom_fee, _disable_personal_exchange_fee):
        """ SCI payin from PRIVAT24 115 UAH by MERCHANT with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 5 UAH, with personal percent operation fee 3.5% with personal
            absolute operation fee 2 UAH, with common exchange fee 4% with personal exchange fee 2%. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(115))
        admin.set_rate_exchange(fee=pers(4), rate=bl(28.1999), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(5), add=bl(5))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True,
                      mult=pers(3.5), add=bl(2), merchant_id=user1.merchant1.id)
        user1.merchant1.sci_pay(model='create',  params={'payway': 'privat24', 'amount': '115', 'in_curr': 'UAH', 'out_curr': 'USD',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay['account_amount'] == '3.78'
        assert user1.merchant1.resp_sci_pay['rate'] == ['28.7639', '1']
        assert user1.merchant1.resp_sci_pay['in_fee_amount'] == '6.03'
        assert user1.merchant1.resp_sci_pay['out_fee_amount'] == '0.21'
        assert user1.merchant1.resp_sci_pay['in_amount'] == '115'
        assert user1.merchant1.resp_sci_pay['out_amount'] == '3.99'
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=0)
        admin.set_order_status(lid=user1.merchant1.resp_sci_pay['lid'], status=100)
        assert user1.merchant1.balance('USD') == '4.78'

    def test_sci_pay_create_12(self, _custom_fee, _disable_personal_exchange_fee):
        """ Payin from BTC 0.0067 BTC by OWNER with exchange to USD with common percent operation fee 5%
            with common absolute operation fee 0.0003 BTC, with personal percent operation fee 3.5% with personal,
            with common exchange fee 3% with personal exchange fee 1.5%. """
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.0005), tech_max=bl(1))
        admin.set_rate_exchange(fee=pers(3), rate=bl(3580.6541), in_currency='BTC', out_currency='USD')
        admin.set_personal_exchange_fee(fee=pers(1.5), in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True, mult=pers(5), add=bl(0.0003))
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=40, is_active=True,
                      mult=pers(3.5), add=0, merchant_id=user1.merchant1.id)
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'btc', 'amount': '0.0067', 'in_curr': 'BTC', 'out_curr': 'USD', 'expiry': '60s'})
        assert user1.resp_delegate['rate'] == ['1', '3526.94428']
        assert user1.resp_delegate['account_amount'] == '22.8'
        assert user1.resp_delegate['out_amount'] == '23.63'
        assert user1.resp_delegate['in_fee_amount'] == '0.0002345'
        assert user1.resp_delegate['out_fee_amount'] == '0.83'


class TestWrongSciPayCreate:
    """ Testing bad sci pay create request. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_pay_create_1(self, _merchant_activate):
        """ Payin with not active merchant. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '2', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_sci_pay_create_2(self):
        """ Payin with amount less than tech_min in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '0.99', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '0.99'}}

    def test_wrong_sci_pay_create_3(self):
        """ Payin with amount more than tech_max in pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '100.01', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.sci_pay == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_sci_pay_create_4(self):
        """ Payin with exchange: in_curr less than tech_min by exchange table
            Payin with exchange: in_curr more than tech_max by exchange table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(4), tech_max=bl(105))
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(5), tech_max=bl(100), in_currency='UAH', out_currency='USD')
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '4.99', 'in_curr': 'UAH', 'out_curr': 'USD',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s', 'contact': '+380661111111'})
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '4.99'}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '100.01', 'in_curr': 'UAH', 'out_curr': 'USD',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '100.01'}}

    def test_wrong_sci_pay_create_5(self):
        """ Payin with not real currency. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'privat24', 'amount': '50', 'in_curr': 'UHA', 'out_curr': 'UHA',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'message': 'InvalidCurrency', 'data': {'reason': 'UHA'}}

    def test_wrong_sci_pay_create_6(self):
        """ Payin with not real payway. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visam', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_payin_create == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visam is unknown'}}

    def test_wrong_sci_pay_create_7(self):
        """ Payin with deactivated pair CURRENCY : PAYWAY by pw_carrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=False, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077,
                                                'data': {'reason': 'UAH is not active currently'}, 'message': 'InactiveCurrency'}
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))

    def test_wrong_sci_pay_create_8(self):
        """ Payin with deactivated PAYWAY by payway table. """
        admin.set_payways(name='visamc', is_active=False, is_public=True)
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'message': 'InvalidPayway', 'data': {'reason': 'visamc'}}
        admin.set_payways(name='visamc', is_active=True, is_public=True)

    def test_wrong_sci_pay_create_9(self):
        """ Payin with deactivated PAYWAY by pw_merchactive table. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=False)
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32062, 'message': 'UnavailPayway',
                                                'data': {'reason': 'Payway visamc is inactive for merchant'}}
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id['visamc'], is_active=True)

    def test_wrong_sci_pay_create_10(self):
        """ Payin with convert in to not active currency. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'BCHABC',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_sci_pay_create_11(self):
        """ Payin with convert from not active currency. """
        admin.set_pwc(pw_id=admin.payway_id['bchabc'], currency='BCHABC', is_out=False, is_active=True, tech_min=bl(0.01), tech_max=bl(2))
        user1.merchant1.sci_pay(method='create', params={'payway': 'bchabc', 'amount': '2', 'in_curr': 'BCHABC', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_sci_pay_create_12(self):
        """ Payin with convert by not active exchange pair. """
        admin.set_pwc(pw_id=admin.payway_id['ltc'], currency='LTC', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create', params={'payway': 'ltc', 'amount': '2', 'in_curr': 'LTC', 'out_curr': 'ETH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32065, 'message': 'UnavailExchange',
                                                'data': {'reason': 'Unavailable excange for LTC to ETH'}}

    def test_wrong_sci_pay_create_13(self):
        """ Payin by not real pair payway+currency. """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(150))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'reason': None}, 'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_create_14(self):
        """ Payin without in_curr parameter. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.create' missing 1 argument: 'in_curr'"}}

    def test_wrong_sci_pay_create_15(self):
        """ Payin without payway parameter. """
        user1.merchant1.sci_pay(method='create', params={'amount': '10', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.create' missing 1 argument: 'payway'"}}

    def test_wrong_sci_pay_create_16(self):
        """ Payin without EXPIRY parameter. """
        user1.merchant1.sci_pay(method='create', params={'amount': '10', 'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'contact': '+380661111111'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.create' missing 1 argument: 'expiry'"}}

    def test_wrong_sci_pay_create_17(self):
        """ Payin without externalid parameter. """
        user1.merchant1.sci_pay(method='create', params={'amount': '10', 'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'contact': '+380661111111', 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.create' missing 1 argument: 'externalid'"}}

    def test_wrong_sci_pay_create_18(self):
        """ Payin without AMOUNT parameter. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'in_curr': 'UAH', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(),
                                                         'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'sci_pay.create' missing 1 argument: 'amount'"}}

    def test_wrong_sci_pay_create_19(self):
        """ Payin with wrong format amount. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '10.999', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                'data': {'reason': 'Invalid format 10.999 for UAH'}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': 'String', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                'data': {'reason': 'Invalid format String for UAH'}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': 10, 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'int' type"}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': [1, 2], 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'list' type"}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': {'1': 1}, 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': "Key 'amount' must not be of 'dict' type"}}
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '-10', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '-10'}}

    def test_wrong_sci_pay_create_20(self):
        """ Payin with duplicate externalid parameter. """
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_pay(method='create', params={'payway': 'visamc', 'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH',
                                                         'externalid': user1.merchant1.resp_sci_pay['externalid'], 'expiry': '60s'})
        assert user1.merchant1.resp_sci_pay == {'code': -32033, 'data': {'reason': 'Duplicated key for externalid'}, 'message': 'Unique'}

    def test_wrong_sci_pay_create_21(self):
        """ Payin with wrong merchant. """
        data = {'method': 'sci_pay.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(), 'expiry': '60s'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_sci_pay_create_22(self):
        """ Payin without merchant. """
        data = {'method': 'sci_pay.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(), 'expiry': '60s'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_sci_pay_create_23(self):
        """ Payin with wrong sign. """
        data = {'method': 'sci_pay.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(), 'expiry': '60s'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_sci_pay_create_24(self):
        """ Payin without sign. """
        data = {'method': 'sci_pay.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(), 'expiry': '60s'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid), 'x-signature': None, 'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_sci_pay_create_25(self):
        """ Payin without utc_time. """
        data = {'method': 'sci_pay.create',
                'params': {'payway': 'visamc', 'amount': '10', 'out_curr': 'UAH', 'externalid': user1.merchant1._id(), 'expiry': '60s'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-utc-now-ms to headers'}}


class TestSciPayCancel:
    """ Cancelling sci_pay order"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_cancel_sci_pay_order_1(self):
        """ Revoke order by MERCHANT. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'USD', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': user1.merchant1.resp_sci_pay['token']})
        assert user1.merchant1.resp_sci_pay['status'] == 'canceled'
        assert admin.get_model(model='order', _filter='token', value=user1.merchant1.resp_sci_pay['token'])[0]['status'] == 130
        assert user1.merchant1.balance('USD') == '1'

    def test_cancel_pay_order_2(self):
        """ Revoke order by OWNER with fee for sci_pay. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=40, is_active=True, mult=pers(15))
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(10), tech_max=bl(200))
        user1.merchant1.sci_pay(method='create', params={'payway': 'privat24', 'amount': '10', 'in_curr': 'UAH',
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'cancel',
                               'pay_token': user1.merchant1.resp_sci_pay['token']})
        assert user1.resp_delegate['status'] == 'canceled'

    def test_cancel_pay_order_3(self):
        """ Cancelling order after time expiry. """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'USD', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '5s'})
        time.sleep(8)
        assert admin.get_model(model='order', _filter='token', value=user1.merchant1.resp_sci_pay['token'])[0]['status'] == 120


class TestWrongCancelSciPay:
    """ Wrong cancelling sci_pay order. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_cancel_sci_pay_order_1(self):
        """ Revoking not own order . """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'USD', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant2.sci_pay(method='cancel', params={'pay_token': user2.merchant1.resp_sci_pay['token']})
        assert user1.merchant2.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': 'Order not found with ' + user1.merchant1.resp_sci_pay['token'] + ' token'}}
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'cancel',
                               'pay_token': user1.merchant1.resp_sci_pay['token']})
        assert user2.resp_delegate == {'code': -32070, 'message': 'InvalidParam',
                                       'data': {'reason': 'Order not found with ' + user1.merchant1.resp_sci_pay['token'] + ' token'}}
        assert admin.get_model(model='order', _filter='token', value=user1.merchant1.resp_sci_pay['token'])[0]['status'] == 0

    def test_wrong_cancel_sci_pay_order_2(self):
        """ Canceling order after canceled before. """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'USD', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': user1.merchant1.resp_sci_pay['token']})
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': user1.merchant1.resp_sci_pay['token']})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': 'Order not found with ' + user1.merchant1.resp_sci_pay['token'] + ' token'}}

    def test_wrong_cancel_sci_pay_order_3(self):
        """ Canceled payin order. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin(method='create', params={'payway': 'visamc', 'amount': '10', 'in_curr': 'UAH', 'out_curr': 'UAH',
                              'externalid': user1.merchant1._id(), 'payee': None, 'contact': None, 'region': None, 'payer': None})
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': user1.merchant1.resp_payin['token']})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam',
                                                'data': {'reason': 'Order not found with ' + user1.merchant1.resp_sci_pay['token'] + ' token'}}

    def test_wrong_cancel_sci_pay_order_4(self):
        """ Canceled with wrong token. """
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_pay(method='create', params={'payway': 'payeer', 'amount': '10', 'in_curr': 'USD', 'out_curr': None,
                                                         'externalid': user1.merchant1._id(), 'expiry': '60s'})
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': user1.merchant1.resp_payin['token'] + '1'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070,
                                                'data': {'reason': "Order not found with " + user1.merchant1.resp_payin['token'] + '1' + ' token'},
                                                'message': 'InvalidParam'}

    def test_wrong_cancel_sci_pay_order_5(self):
        """ Request without pay token. """
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam'}

    def test_wrong_cancel_sci_pay_order_6(self):
        """ Request with excess parameter. """
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': '333', 'par': '123'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam'}

    def test_wrong_cancel_sci_pay_order_7(self):
        """ Request with excess parameter. """
        user1.merchant1.sci_pay(method='cancel', params={'pay_token': '333', 'par': '123'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam'}

    def test_wrong_cancel_sci_pay_order_8(self):
        """ Cancel order with wrong merchant. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_cancel_sci_pay_order_9(self):
        """ Cancel order without merchant. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_cancel_sci_pay_order_10(self):
        """ Cancel order with wrong sign. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_cancel_sci_pay_order_11(self):
        """ Cancel order without sign. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_cancel_sci_pay_order_12(self):
        """ Cancel order without sign. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_cancel_sci_pay_order_13(self):
        """ Cancel order with NONE x-utc-now-ms sign. """
        data = {'method': 'sci_pay.cancel', 'params': {'pay_token': '333'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_create_sci_pay_list')
class TestListSciPay:
    """ Testing list sci_pay. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_sci_pay_1(self):
        """ Getting list with all default parameter sci_pay orders by MERCHANT. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None})
        us_ls_tp = [dct['tp'] for dct in user1.merchant1.resp_sci_pay['data']]
        us_ls_owner = [dct['owner'] for dct in user1.merchant1.resp_sci_pay['data']]
        assert equal_list(_list=us_ls_tp, elem='sci_pay') and equal_list(_list=us_ls_owner, elem=user1.merchant1.lid)

    def test_list_sci_pay_2(self):
        """ Getting list with COUNT parameter sci_pay orders by OWNER. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40]
        adm_ls = adm_ls[:4]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_pay', 'merch_method': 'list',
                               'payway': None, 'in_curr': None, 'out_curr': None, 'first': None, 'count': '4'})
        us_ls = [dct['ctime'] for dct in user1.resp_delegate['data']]
        assert adm_ls == us_ls

    def test_list_sci_pay_3(self):
        """ Getting list with FIRST and COUNT parameter by MERCHANT. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40]
        adm_ls = adm_ls[1:5]
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': '1', 'count': '4'})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_pay['data']]
        assert adm_ls == us_ls

    def test_list_sci_pay_4(self):
        """ Getting list with FIRST, COUNT and PAYWAY parameter. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40
                  and dct['payway_id'] == admin.payway_id['privat24']]
        adm_ls = adm_ls[1:5]
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': 'privat24', 'first': '1', 'count': '4'})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_pay['data']]
        print(adm_ls, us_ls)
        assert adm_ls == us_ls

    def test_list_sci_pay_5(self):
        """ Getting list with FIRST, COUNT, PAYWAY and IN_CURR parameter. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40
                  and dct['payway_id'] == admin.payway_id['payeer'] and dct['in_currency_id'] == admin.currency['USD']]
        adm_ls = adm_ls[1:5]
        user1.merchant1.sci_pay(method='list', params={'in_curr': 'USD', 'out_curr': None, 'payway': 'payeer', 'first': '1', 'count': '4'})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_pay['data']]
        print(adm_ls, us_ls)
        assert adm_ls == us_ls

    def test_list_sci_pay_6(self):
        """ Getting list with FIRST, PAYWAY and IN_CURR and OUT_CURR parameter. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40
                  and dct['payway_id'] == admin.payway_id['payeer'] and dct['in_currency_id'] == admin.currency['USD'] and
                  dct['out_currency_id'] == admin.currency['UAH']]
        user1.merchant1.sci_pay(method='list', params={'in_curr': 'USD', 'out_curr': 'UAH', 'payway': 'payeer', 'first': None, 'count': None})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_pay['data']]
        print(adm_ls, us_ls)
        assert adm_ls == us_ls


class TestWrongListSciPay:
    """ Wrong request to sci_pay.list. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_pay_list_1(self):
        """ Request with not correct parameter COUNT. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': 1})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'reason': "Key 'count' must not be of 'int' type"},
                                                'message': 'InvalidParam'}
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': '1.5'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'field': 'count', 'reason': 'Should be an Integer'},
                                                'message': 'InvalidParam'}
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': '-1'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'field': 'count', 'reason': 'Should be more than zero'},
                                                'message': 'InvalidParam'}

    def test_wrong_sci_pay_list_2(self):
        """ Request with not correct parameter FIRST. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': 1, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'reason': "Key 'first' must not be of 'int' type"},
                                                'message': 'InvalidParam'}
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': '1.5', 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'field': 'first', 'reason': 'Should be an Integer'},
                                                'message': 'InvalidParam'}
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': '-1', 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'data': {'field': 'first', 'reason': 'Should be a positive Number'},
                                                'message': 'InvalidParam'}

    def test_wrong_sci_pay_list_3(self):
        """ Request with not real IN_CURR. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': 'UHA', 'out_curr': None, 'payway': None, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'field': 'in_curr', 'reason': 'Invalid currency name'},
                                                'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_list_4(self):
        """ Request with not string IN_CURR. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': True, 'out_curr': None, 'payway': None, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'field': 'in_curr', 'reason': 'Invalid currency name'},
                                                'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_list_5(self):
        """ Request with not real OUT_CURR. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': 'UHA', 'payway': None, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'field': 'out_curr', 'reason': 'Invalid currency name'},
                                                'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_list_6(self):
        """ Request with not string OUT_CURR. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': False, 'payway': None, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32076, 'data': {'field': 'out_curr', 'reason': 'Invalid currency name'},
                                                'message': 'InvalidCurrency'}

    def test_wrong_sci_pay_list_7(self):
        """ Request with not real payway. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': 'visam', 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'data': {'field': 'payway', 'reason': 'Invalid payway name'},
                                                'message': 'InvalidPayway'}

    def test_wrong_sci_pay_list_8(self):
        """ Request with not string payway. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': True, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32060, 'data': {'field': 'payway', 'reason': 'Invalid payway name'},
                                                'message': 'InvalidPayway'}

    def test_wrong_sci_pay_list_9(self):
        """ Request with excess parameter. """
        user1.merchant1.sci_pay(method='list', params={'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None, 'par': '123'})
        assert user1.merchant1.resp_sci_pay == {'code': -32070, 'message': 'InvalidParam'}

    def test_wrong_sci_pay_list_10(self):
        """ Request with wrong merchant. """
        data = {'method': 'sci_pay.list', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_sci_pay_list_11(self):
        """ Request without merchant. """
        data = {'method': 'sci_pay.cancel', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_list_12(self):
        """ Request with wrong sign. """
        data = {'method': 'sci_pay.cancel', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_sci_pay_list_13(self):
        """ Request without sign. """
        data = {'method': 'sci_pay.list', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_list_14(self):
        """ Request without sign. """
        data = {'method': 'sci_pay.list', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_list_15(self):
        """ Request without x-utc-now. """
        data = {'method': 'sci_pay.list', 'params': {'in_curr': None, 'out_curr': None, 'payway': None, 'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_sci_pay_list_16(self):
        """ Request with wrong method. """
        user1.merchant1.sci_pay(method='listt', params={'in_curr': None, 'out_curr': False, 'payway': None, 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_pay == {'code': -32601, 'message': 'Method not found'}
