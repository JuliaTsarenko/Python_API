import requests
import pytest
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_sub_pay_fee', '_personal_exchange_fee', '_create_sci_pay_order')
class TestSciSubPayCalc:
    """ Checking calc sub_pay order for created SCI_PAY order. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, token
        admin, user1, user2 = start_session
        token = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]['token']

    def test_sci_subpay_calc_1(self):
        """ Calc subpay order with full amount. In_curr UAH, without exchange and without operations fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50'})
        assert user2.merchant1.resp_sci_subpay == {'account_amount': '50', 'in_amount': '50', 'in_fee_amount': '0', 'orig_amount': '50',
                                                   'out_amount': '50', 'out_fee_amount': '0'}

    def test_sci_subpay_calc_2(self):
        """ Calc subpay order with half amount. In_curr UAH, without exchange and without operations fee by OWNER. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'privat24', 'amount': '25', 'in_curr': 'UAH'})
        assert user2.resp_delegate == {'account_amount': '25', 'in_amount': '25', 'in_fee_amount': '0', 'orig_amount': '25',
                                       'out_amount': '25', 'out_fee_amount': '0'}

    def test_sci_subpay_calc_3(self):
        """ Calc subpay order with more amount then SCI_PAY order. In_curr UAH, without exchange and without operations fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'privat24', 'in_curr': 'UAH', 'amount': '50.01'})
        assert user1.merchant1.resp_sci_subpay == {'account_amount': '50.01', 'in_amount': '50.01', 'in_fee_amount': '0', 'orig_amount': '50.01',
                                                   'out_amount': '50.01', 'out_fee_amount': '0'}

    def test_sci_subpay_calc_4(self):
        """ Calc subpay order with exchange without fee: USD to UAH. Amount in request in USD equal with amount in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(0.5), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'payeer', 'amount': '1.77', 'in_curr': 'USD'})
        assert user2.resp_delegate == {'account_amount': '50', 'in_amount': '1.77', 'in_fee_amount': '0', 'orig_amount': '1.77',
                                       'out_amount': '50', 'out_fee_amount': '0', 'rate': ['1', '28.24859']}

    def test_sci_subpay_calc_5(self):
        """ Calc subpay order with exchange without fee: RUB to UAH. Amount in request in RUB more than in sci_pay order by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=0, rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'payeer', 'in_curr': 'RUB', 'amount': '131.09'})
        assert user1.merchant1.resp_sci_subpay == {'account_amount': '50.01', 'in_amount': '131.09', 'in_fee_amount': '0', 'orig_amount': '131.09',
                                                   'out_amount': '50.01', 'out_fee_amount': '0', 'rate': ['2.6211', '1']}

    def test_sci_subpay_calc_6(self):
        """ Calc subpay order with exchange without fee: BTC to UAH. Amount in request in BTC less than in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.00000001), tech_max=bl(1))
        admin.set_rate_exchange(fee=0, rate=bl(17919.3156), in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000001), tech_max=bl(1))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'btc', 'amount': '0.00000056', 'in_curr': 'BTC'})
        assert user2.resp_delegate == {'account_amount': '0.01', 'in_amount': '0.00000056', 'in_fee_amount': '0', 'orig_amount': '0.00000056',
                                       'out_amount': '0.01', 'out_fee_amount': '0', 'rate': ['1', '17919.3156']}

    def test_sci_subpay_calc_7(self):
        """ Calc subpay order with exchange common exchange fee 0.55%: USD to UAH. Amount in request in USD equal with amount in sci_pay order
            by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(0.55), rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(0.5), tech_max=bl(100))
        user2.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'perfect', 'in_curr': 'USD', 'amount': '1.78'})
        assert user2.merchant1.resp_sci_subpay == {'account_amount': '50', 'in_amount': '1.78', 'in_fee_amount': '0', 'orig_amount': '1.78',
                                                   'out_amount': '50', 'out_fee_amount': '0', 'rate': ['1', '28.09322']}

    def test_sci_subpay_calc_8(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc subpay order with exchange common exchange fee 5%, with personal exchange fee 3.3%: RUB to UAH.
            Amount in request in RUB more than amount in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(5), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3.3))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'qiwi', 'amount': '135.41', 'in_curr': 'RUB'})
        assert user2.resp_delegate == {'account_amount': '50.01', 'in_amount': '135.41', 'in_fee_amount': '0', 'orig_amount': '135.41',
                                       'out_amount': '50.01', 'out_fee_amount': '0', 'rate': ['2.7076', '1']}

    def test_sci_subpay_calc_9(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc subpay order with exchange common exchange fee 5%, with personal exchange fee 3.3%: USD to UAH.
            Amount in request in USD less than amount in sci_pay order by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(5), rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(1), tech_max=bl(100))
        admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3.3))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'perfect', 'in_curr': 'USD', 'amount': '1'})
        assert user1.merchant1.resp_sci_subpay == {'account_amount': '27.31', 'in_amount': '1', 'in_fee_amount': '0', 'orig_amount': '1',
                                                   'out_amount': '27.31', 'out_fee_amount': '0', 'rate': ['1', '27.31638']}

    def test_sci_subpay_calc_10(self):
        """ Calc subpay order without exchange with common operations fee: 1 UAH and 1.5% by OWNER. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(1), mult=pers(1.5), tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'visamc', 'amount': '51.78', 'in_curr': 'UAH'})
        assert user2.resp_delegate == {'account_amount': '50', 'in_amount': '51.78', 'in_fee_amount': '1.78', 'orig_amount': '51.78',
                                       'out_amount': '51.78', 'out_fee_amount': '1.78'}

    def test_sci_subpay_calc_11(self, _custom_fee, _set_fee):
        """ Calc subpay order without exchange with common operations fee: 2 UAH and 17% and personal operations fee 1 UAH and 1,5% by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(2), mult=pers(1.7), tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(1), mult=pers(1.5), tp=45,
                      merchant_id=user1.merchant1.id, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '51.79'})
        assert user2.merchant1.resp_sci_subpay == {'account_amount': '50.01', 'in_amount': '51.79', 'in_fee_amount': '1.78', 'orig_amount': '51.79',
                                                   'out_amount': '51.79', 'out_fee_amount': '1.78'}

    def test_sci_subpay_calc_12(self):
        """ Calc subpay order with exchange USD to UAH with common exchange fee with common operations fee: 0.1 USD and 1,5% by OWNER """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], add=bl(0.1), mult=pers(1.5), tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(28.1433), in_currency='USD', out_currency='UAH', tech_min=bl(1), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'calc', 'sci_pay_token': token,
                               'payway': 'payeer', 'amount': '1.2', 'in_curr': 'USD'})
        assert user2.resp_delegate == {'account_amount': '30.39', 'in_amount': '1.2', 'in_fee_amount': '0.12', 'orig_amount': '1.2',
                                       'out_amount': '33.77', 'out_fee_amount': '3.38', 'rate': ['1', '28.1433']}

    def test_sci_subpay_calc_13(self, _custom_fee, _disable_personal_exchange_fee, _set_fee):
        """ Calc subpay order with exchange RUB to UAH with common exchange fee and personal exchange fee with common operations fee:
            5 RUB and 15% and personal operations fee 2 RUB and 10% by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], add=bl(5), mult=pers(2), tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], add=bl(1), mult=pers(1.5), tp=45,
                      merchant_id=user1.merchant1.id, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(6), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(5))
        user2.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'payeer', 'in_curr': 'RUB', 'amount': '160'})
        assert user2.merchant1.resp_sci_subpay == {'account_amount': '56.89', 'in_amount': '160', 'in_fee_amount': '3.4', 'orig_amount': '160',
                                                   'out_amount': '58.13', 'out_fee_amount': '1.24', 'rate': ['2.75216', '1']}


@pytest.mark.usefixtures('_create_sci_pay_order')
class TestWrongSciSubPayCalc:
    """ Checking wrong request to sci_subpay calc method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, token
        admin, user1, user2 = start_session
        token = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]['token']

    def test_wrong_sci_sub_pay_calc_1(self):
        """ Calc sub pay order with amount less than pwcurrency tech_min. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '0.99'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32074, 'data': {'field': 'amount', 'reason': 'Amount is too small', 'value': '0.99'},
                                                   'message': 'EParamAmountTooSmall'}

    def test_wrong_sci_sub_pay_calc_2(self):
        """ Calc sub pay order with amount less than pwcurrency tech_min. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '100.01'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32073, 'data': {'field': 'amount', 'reason': 'Amount is too big', 'value': '100.01'},
                                                   'message': 'EParamAmountTooBig'}

    def test_wrong_sci_sub_pay_calc_3(self, _create_payin_order):
        """ Calc sub pay order with not sci_pay type order. """
        payin_order = admin.get_model(model='order', _filter='tp', value=0)[0]
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': payin_order['token'], 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'order_token', 'reason': 'Invalid order_token value',
                                                   'value': payin_order['token']}, 'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_calc_4(self):
        """ Calc sub pay order with int amount. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': 50})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'amount', 'reason': "'amount' must not be of 'int' type",
                                                                            'value': 50}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_calc_5(self):
        """ Calc sub pay order with not digit amount. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': []})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'amount', 'reason': "'amount' must not be of 'list' type",
                                                   'value': []}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_calc_6(self):
        """ Calc sub pay order with not real in_curr. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UHA', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32014, 'data': {'field': 'in_curr', 'reason': 'Invalid currency name'},
                                                   'message': 'EParamCurrencyInvalid'}

    def test_wrong_sci_sub_pay_calc_7(self):
        """ Calc sub pay order with not real payway. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visam', 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32081, 'data': {'field': 'payway', 'reason': 'Invalid payway name'},
                                                   'message': 'EParamPaywayInvalid'}

    def test_wrong_sci_sub_pay_calc_8(self):
        """ Calc sub pay order with not active pair currency: payway by pwcurrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=False, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32033, 'data': {'field': 'currency', 'reason': 'Inactive'},
                                                   'message': 'EStateCurrencyInactive'}
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))

    def test_wrong_sci_sub_pay_calc_9(self):
        """ Calc sub pay order without sci_pay_token. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': None, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'sci_pay_token', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_calc_10(self):
        """ Calc sub pay order without payway parameter. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': None, 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'payway', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_calc_11(self):
        """ Calc sub pay order without payway parameter. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': None, 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'in_curr', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_calc_12(self):
        """ Calc sub pay order without amount parameter. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': None})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'amount', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_calc_13(self):
        """ Calc sub pay order with excess parameter. """
        user1.merchant1.sci_subpay(method='calc', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50', 'par': '123'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002,  'data': {'field': 'par', 'reason': 'Should not be provided'},
                                                   'message': 'EParamInvalid'}


@pytest.mark.usefixtures('_personal_sub_pay_fee', '_personal_exchange_fee', '_create_sci_pay_order')
class TestSciSubPayCreate:
    """ Checking creating sci_subpay order. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, token
        admin, user1, user2 = start_session
        token = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]['token']

    def test_sci_subpay_create_1(self, _start_sci_pay_order):
        """ Create subpay order with full amount. In_curr UAH, without exchange and without operations fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='visamc')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'visamc']})
        user2.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'amount': '50', 'in_curr': 'UAH', 'payway': 'visamc',
                                                            'externalid': user2.merchant1._id()})
        assert user2.merchant1.resp_sci_subpay['account_amount'] == '50'
        assert user2.merchant1.resp_sci_subpay['in_amount'] == '50'
        assert user2.merchant1.resp_sci_subpay['out_amount'] == '50'

    def test_sci_subpay_create_2(self, _start_sci_pay_order):
        """ Create subpay order with half amount. In_curr UAH, without exchange and without operations fee by OWNER. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='privat24')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'privat24']})
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'privat24', 'amount': '25', 'in_curr': 'UAH', 'externalid': user2.merchant1._id()})
        assert user2.resp_delegate['account_amount'] == '25'
        assert user2.resp_delegate['payway_name'] == 'privat24'
        assert user2.resp_delegate['in_fee_amount'] == '0'
        assert user2.resp_delegate['out_fee_amount'] == '0'
        assert admin.get_model(model='order', _filter='lid', value=user2.resp_delegate['lid'])[0]['base_order_id'] == \
            admin.get_model(model='order', _filter='token', value=token)[0]['id']

    def test_sci_subpay_create_3(self, _start_sci_pay_order):
        """ Create subpay order with more amount then SCI_PAY order. In_curr UAH, without exchange and without operations fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='privat24')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'privat24']})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'privat24', 'in_curr': 'UAH', 'amount': '50.01',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay['account_amount'] == '50.01'
        assert user1.merchant1.resp_sci_subpay['in_amount'] == '50.01'
        assert user1.merchant1.resp_sci_subpay['out_amount'] == '50.01'
        assert user1.merchant1.resp_sci_subpay['in_curr'] == 'UAH'
        assert user1.merchant1.resp_sci_subpay['tp'] == 'sci_subpay'

    def test_sci_subpay_create_4(self, _start_sci_pay_order):
        """ Create subpay order with exchange without fee: USD to UAH. Amount in request in USD equal with amount in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(0.5), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='payeer')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'payeer']})
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'payeer', 'amount': '1.77', 'in_curr': 'USD', 'externalid': user1.merchant1._id()})
        assert user1.resp_delegate['account_amount'] == '50'
        assert user1.resp_delegate['in_amount'] == '1.77'
        assert user1.resp_delegate['out_amount'] == '50'
        assert user1.resp_delegate['orig_amount'] == '1.77'
        assert user1.resp_delegate['rate'] == ['1', '28.24859']

    def test_sci_subpay_create_5(self, _start_sci_pay_order):
        """ Create subpay order with exchange without fee: RUB to UAH. Amount in request in RUB more than in sci_pay order by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=0, rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        params = admin.get_model(model='payway', _filter='name', value='payeer')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'payeer']})
        user2.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'payeer', 'in_curr': 'RUB', 'amount': '131.09',
                                                            'externalid': user2.merchant1._id()})
        assert user2.merchant1.resp_sci_subpay['account_amount'] == '50.01'
        assert user2.merchant1.resp_sci_subpay['in_fee_amount'] == '0'
        assert user2.merchant1.resp_sci_subpay['out_fee_amount'] == '0'
        assert user2.merchant1.resp_sci_subpay['rate'] == ['2.6211', '1']

    def test_sci_subpay_create_6(self, _start_sci_pay_order):
        """ Create subpay order with exchange without fee: BTC to UAH. Amount in request in BTC less than in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['BTC'], payway_id=admin.payway_id['btc'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['btc'], currency='BTC', is_out=False, is_active=True, tech_min=bl(0.00000001), tech_max=bl(1))
        admin.set_rate_exchange(fee=0, rate=bl(17919.3156), in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000001), tech_max=bl(1))
        params = admin.get_model(model='payway', _filter='name', value='btc')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'btc']})
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'btc', 'amount': '0.00000056', 'in_curr': 'BTC', 'externalid': user2.merchant1._id()})
        assert user2.resp_delegate['account_amount'] == '0.01'
        assert user2.resp_delegate['in_amount'] == '0.00000056'
        assert user2.resp_delegate['out_amount'] == '0.01'
        assert user2.resp_delegate['rate'] == ['1', '17919.3156']

    def test_sci_subpay_create_7(self, _start_sci_pay_order):
        """ Create subpay order with exchange common exchange fee 0.55%: USD to UAH. Amount in request in USD equal with amount in sci_pay order
            by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(0.55), rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(0.5), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='perfect')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'perfect']})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'perfect', 'in_curr': 'USD', 'amount': '1.78',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay['account_amount'] == '50'
        assert user1.merchant1.resp_sci_subpay['in_amount'] == '1.78'
        assert user1.merchant1.resp_sci_subpay['rate'] == ['1', '28.09322']
        assert admin.get_model(model='order', _filter='lid', value=user1.merchant1.resp_sci_subpay['lid'])[0]['base_order_id'] == \
            admin.get_model(model='order', _filter='token', value=token)[0]['id']

    def test_sci_subpay_create_8(self, _start_sci_pay_order, _custom_fee, _disable_personal_exchange_fee):
        """ Create subpay order with exchange common exchange fee 5%, with personal exchange fee 3.3%: RUB to UAH.
            Amount in request in RUB more than amount in sci_pay order by OWNER. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(5), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3.3))
        params = admin.get_model(model='payway', _filter='name', value='qiwi')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'qiwi']})
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'qiwi', 'amount': '135.41', 'in_curr': 'RUB', 'externalid': user2.merchant1._id(),
                               'payer': '+380661111111'})
        assert user2.resp_delegate['account_amount'] == '50.01'
        assert user2.resp_delegate['in_amount'] == '135.41'
        assert user2.resp_delegate['rate'] == ['2.7076', '1']

    def test_sci_subpay_create_9(self, _start_sci_pay_order, _custom_fee, _disable_personal_exchange_fee):
        """ Create subpay order with exchange common exchange fee 5%, with personal exchange fee 3.3%: USD to UAH.
            Amount in request in USD less than amount in sci_pay order by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(5), rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(1), tech_max=bl(100))
        admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3.3))
        params = admin.get_model(model='payway', _filter='name', value='perfect')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'perfect']})
        user2.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'perfect', 'in_curr': 'USD', 'amount': '1',
                                                            'externalid': user2.merchant1._id()})
        assert user2.merchant1.resp_sci_subpay['account_amount'] == '27.31'
        assert user2.merchant1.resp_sci_subpay['orig_amount'] == '1'
        assert user2.merchant1.resp_sci_subpay['in_amount'] == '1'
        assert user2.merchant1.resp_sci_subpay['out_amount'] == '27.31'
        assert user2.merchant1.resp_sci_subpay['rate'] == ['1', '27.31638']

    def test_sci_subpay_create_10(self, _start_sci_pay_order):
        """ Create subpay order without exchange with common operations fee: 1 UAH and 1.5% by OWNER. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(1), mult=pers(1.5), tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='visamc')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'visamc']})
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'visamc', 'amount': '51.78', 'in_curr': 'UAH', 'externalid': user1.merchant1._id()})
        assert user1.resp_delegate['account_amount'] == '50'
        assert user1.resp_delegate['in_fee_amount'] == '1.78'
        assert user1.resp_delegate['out_fee_amount'] == '1.78'
        assert admin.get_model(model='order', _filter='lid', value=user1.resp_delegate['lid'])[0]['base_order_id'] == \
            admin.get_model(model='order', _filter='token', value=token)[0]['id']

    def test_sci_subpay_create_11(self, _start_sci_pay_order, _custom_fee, _set_fee):
        """ Create subpay order without exchange with common operations fee: 2 UAH and 17% and personal operations fee 1 UAH and 1,5% by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(2), mult=pers(1.7), tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(1), mult=pers(1.5), tp=45,
                      merchant_id=user1.merchant1.id, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='visamc')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'visamc']})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '51.79',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay['account_amount'] == '50.01'
        assert user1.merchant1.resp_sci_subpay['in_fee_amount'] == '1.78'
        assert user1.merchant1.resp_sci_subpay['out_fee_amount'] == '1.78'

    def test_sci_subpay_create_12(self, _start_sci_pay_order):
        """ Create subpay order with exchange USD to UAH with common exchange fee with common operations fee: 0.1 USD and 1,5% by OWNER """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], add=bl(0.1), mult=pers(1.5), tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=0, rate=bl(28.1433), in_currency='USD', out_currency='UAH', tech_min=bl(1), tech_max=bl(100))
        params = admin.get_model(model='payway', _filter='name', value='payeer')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'payeer']})
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'create', 'sci_pay_token': token,
                               'payway': 'payeer', 'amount': '1.2', 'in_curr': 'USD', 'externalid': user2.merchant1._id()})
        assert user2.resp_delegate['account_amount'] == '30.39'
        assert user2.resp_delegate['in_amount'] == '1.2'
        assert user2.resp_delegate['in_fee_amount'] == '0.12'
        assert user2.resp_delegate['out_fee_amount'] == '3.38'
        assert user2.resp_delegate['out_amount'] == '33.77'
        assert user2.resp_delegate['rate'] == ['1', '28.1433']
        assert admin.get_model(model='order', _filter='lid', value=user2.resp_delegate['lid'])[0]['base_order_id'] == \
            admin.get_model(model='order', _filter='token', value=token)[0]['id']

    def test_sci_subpay_create_13(self, _start_sci_pay_order, _custom_fee, _disable_personal_exchange_fee, _set_fee):
        """ Calc subpay order with exchange RUB to UAH with common exchange fee and personal exchange fee with common operations fee:
            5 RUB and 15% and personal operations fee 2 RUB and 10% by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], add=bl(5), mult=pers(2), tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], add=bl(1), mult=pers(1.5), tp=45,
                      merchant_id=user1.merchant1.id, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(6), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(5))
        params = admin.get_model(model='payway', _filter='name', value='payeer')[0]['params']
        params['payment_expiry'] = '1h'
        admin.set_model(model='payway', data={'params': params}, selector={'name': ['eq', 'payeer']})
        user2.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'payeer', 'in_curr': 'RUB', 'amount': '160',
                                                            'externalid': user2.merchant1._id()})
        assert user2.merchant1.resp_sci_subpay['account_amount'] == '56.89'
        assert user2.merchant1.resp_sci_subpay['in_amount'] == '160'
        assert user2.merchant1.resp_sci_subpay['in_fee_amount'] == '3.4'
        assert user2.merchant1.resp_sci_subpay['out_fee_amount'] == '1.24'
        assert user2.merchant1.resp_sci_subpay['rate'] == ['2.75216', '1']


@pytest.mark.usefixtures('_create_sci_pay_order')
class TestWrongSciSubPayCreate:
    """ Wrong request sci_subpay.create. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, token
        admin, user1, user2 = start_session
        token = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]['token']

    def test_wrong_sci_sub_pay_create_1(self):
        """ Create sub pay order with amount less than pwcurrency tech_min. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '0.99',
                                                            'externalid': user1.merchant1._id()})
        assert user2.merchant1.resp_sci_subpay == {'code': -32074, 'data': {'field': 'amount', 'reason': 'Amount is too small', 'value': '0.99'},
                                                   'message': 'EParamAmountTooSmall'}

    def test_wrong_sci_sub_pay_create_2(self):
        """ Create sub pay order with amount more than pwcurrency tech_max. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '100.01',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32073, 'data': {'field': 'amount', 'reason': 'Amount is too big', 'value': '100.01'},
                                                   'message': 'EParamAmountTooBig'}

    def test_wrong_sci_sub_pay_create_3(self, _create_payin_order):
        """ Create sub pay order with not sci_pay type order. """
        payin_order = admin.get_model(model='order', _filter='tp', value=0)[0]
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': payin_order['token'], 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'order_token', 'reason': 'Invalid order_token value',
                                                   'value': payin_order['token']}, 'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_4(self):
        """ Create sub pay order with int amount. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': 50,
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'amount', 'reason': "'amount' must not be of 'int' type",
                                                                            'value': 50}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_create_5(self):
        """ Create sub pay order with not digit amount. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': [],
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'amount', 'reason': "'amount' must not be of 'list' type",
                                                   'value': []}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_create_6(self):
        """ Create sub pay order with not real in_curr. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UHA', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32014, 'data': {'field': 'in_curr', 'reason': 'Invalid currency name'},
                                                   'message': 'EParamCurrencyInvalid'}

    def test_wrong_sci_sub_pay_create_7(self):
        """ Create sub pay order with not real payway. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visam', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32081, 'data': {'field': 'payway', 'reason': 'Invalid payway name'},
                                                   'message': 'EParamPaywayInvalid'}

    def test_wrong_sci_sub_pay_create_8(self):
        """ Create sub pay order with not active pair currency: payway by pwcurrency table. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=False, tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32033, 'data': {'field': 'currency', 'reason': 'Inactive'},
                                                   'message': 'EStateCurrencyInactive'}
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))

    def test_wrong_sci_sub_pay_create_9(self):
        """ Create sub pay order without sci_pay_token. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': None, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'sci_pay_token', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_10(self):
        """ Create sub pay order without payway parameter. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': None, 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'payway', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_11(self):
        """ Create sub pay order without payway parameter. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': None, 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'in_curr', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_12(self):
        """ Create sub pay order without amount parameter. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': None,
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'amount', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_13(self):
        """ Create sub pay order without externalid parameter. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'externalid', 'reason': 'Should be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_14(self):
        """ Create sub pay order with excess parameter. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50', 'par': '123',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002,  'data': {'field': 'par', 'reason': 'Should not be provided'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_create_15(self, _start_sci_pay_order):
        """ Create sub pay order on not finished order created before. """
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        user1.merchant1.sci_subpay(method='create', params={'sci_pay_token': token, 'payway': 'visamc', 'in_curr': 'UAH', 'amount': '50',
                                                            'externalid': user1.merchant1._id()})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'order_token', 'reason': 'Invalid order_token value',
                                                   'value': token}, 'message': 'EParamInvalid'}


@pytest.mark.usefixtures('_personal_sub_pay_fee', '_personal_exchange_fee', '_create_sci_pay_order')
class TestSciSubPayParams:
    """ Getting params for sci_sub params. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, token
        admin, user1, user2 = start_session
        token = admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)[0]['token']

    def test_sci_sub_pay_params_1(self):
        """ Getting sub_pay params for UAH:VISAMC without exchange and without fee by MERCHANT. """
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(3000))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=45)
        user2.merchant1.sci_subpay(method='params', params={'sci_pay_token': token,  'payway': 'visamc', 'in_curr': 'UAH'})
        assert user2.merchant1.resp_sci_subpay['in_curr'] == 'UAH'
        assert user2.merchant1.resp_sci_subpay['out_curr'] == 'UAH'
        assert user2.merchant1.resp_sci_subpay['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user2.merchant1.resp_sci_subpay['rate'] == ['1', '1']

    def test_sci_sub_pay_params_2(self):
        """ Getting params for USD:perfect with common exchange fee without fee for operations by OWNER. """
        admin.set_pwc(pw_id=admin.payway_id['perfect'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(3000))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['perfect'], tp=45)
        admin.set_rate_exchange(fee=0, rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(0.5), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'params', 'sci_pay_token': token,
                               'payway': 'perfect', 'in_curr': 'USD'})
        assert user2.resp_delegate['in_curr'] == 'USD'
        assert user2.resp_delegate['out_curr'] == 'UAH'
        assert user2.resp_delegate['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user2.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user2.resp_delegate['payway'] == 'perfect'
        assert user2.resp_delegate['is_convert'] is True


    def test_sci_sub_pay_params_3(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for RUB:payeer with common exchange fee and with personal exchange fee by MERCHANT. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(200))
        admin.set_rate_exchange(fee=pers(5), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3.3))
        user2.merchant1.sci_subpay(method='params', params={'sci_pay_token': token,  'payway': 'payeer', 'in_curr': 'RUB'})
        assert user2.merchant1.resp_sci_subpay['in_curr'] == 'RUB'
        assert user2.merchant1.resp_sci_subpay['out_curr'] == 'UAH'
        assert user2.merchant1.resp_sci_subpay['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user2.merchant1.resp_sci_subpay['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
        assert user2.merchant1.resp_sci_subpay['payway'] == 'payeer'
        assert user2.merchant1.resp_sci_subpay['rate'] == ['2.7076', '1']
        assert user2.merchant1.resp_sci_subpay['min'] == '1'
        assert user2.merchant1.resp_sci_subpay['max'] == '200'


    def test_sci_sub_pay_params_4(self):
        """ Getting params for UAH:visamc without exchange with common fee for operations. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], add=bl(1), mult=pers(10), _min=bl(2), _max=bl(5),
                      tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'params', 'sci_pay_token': token,
                               'payway': 'visamc', 'in_curr': 'UAH'})
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['in_fee'] == {'add': '1', 'max': '5', 'method': 'ceil', 'min': '2', 'mult': '0.1'}
        assert user1.resp_delegate['min'] == '3'
        assert user1.resp_delegate['max'] == '100'

    def test_sci_sub_pay_params_5(self, _custom_fee, _set_fee):
        """ Getting params for UAH:visamc without exchange with common fee and with personal fee for operations. """
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], add=bl(2), mult=pers(20), _min=bl(3.5), _max=bl(7),
                      tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['privat24'], add=bl(1), mult=pers(10),
                      tp=45, is_active=True, merchant_id=user1.merchant1.id)
        admin.set_pwc(pw_id=admin.payway_id['privat24'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        user2.delegate(params={'m_lid': user2.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'params', 'sci_pay_token': token,
                               'payway': 'privat24', 'in_curr': 'UAH'})
        assert user2.resp_delegate['in_curr'] == 'UAH'
        assert user2.resp_delegate['out_curr'] == 'UAH'
        assert user2.resp_delegate['in_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.1'}
        assert user2.resp_delegate['min'] == '2.23'
        assert user2.resp_delegate['max'] == '100'
        assert user2.resp_delegate['pwtp'] == 'sci'

    def test_sci_sub_pay_params_6(self):
        """ Getting params for RUB:qiwi with exchange with common exchange fee with common operations fee. """
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['qiwi'], add=bl(1), mult=pers(10),
                      tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['qiwi'], currency='RUB', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(5), rate=bl(2.6211), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        user2.merchant1.sci_subpay(method='params', params={'sci_pay_token': token, 'payway': 'qiwi', 'in_curr': 'RUB'})
        assert user2.merchant1.resp_sci_subpay['in_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.1'}
        assert user2.merchant1.resp_sci_subpay['out_fee'] == {'add': '0.37', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.1'}
        assert user2.merchant1.resp_sci_subpay['min'] == '2.23'
        assert user2.merchant1.resp_sci_subpay['max'] == '100'
        assert user2.merchant1.resp_sci_subpay['rate'] == ['2.75216', '1']

    def test_sci_sub_pay_params_7(self, _custom_fee, _set_fee, _disable_personal_exchange_fee):
        """ Getting params for USD:payeer with exchange with common exchange fee with personal exchange fee,
            with common operations fee with personal operations fee. """
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], add=bl(5), mult=pers(30),
                      tp=45, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], add=bl(1), mult=pers(10), _min=bl(2), _max=bl(5),
                      merchant_id=user1.merchant1.id, tp=45, is_active=True)
        admin.set_pwc(pw_id=admin.payway_id['payeer'], currency='USD', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(fee=pers(5), rate=bl(28.24859), in_currency='USD', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_personal_exchange_fee(fee=pers(3.3), in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                        merchant_id=user1.merchant1.id, is_active=True)
        user1.merchant1.sci_subpay(method='params', params={'sci_pay_token': token, 'payway': 'payeer', 'in_curr': 'USD'})
        assert user1.merchant1.resp_sci_subpay['in_fee'] == {'add': '1', 'max': '5', 'method': 'ceil', 'min': '2', 'mult': '0.1'}
        assert user1.merchant1.resp_sci_subpay['out_fee'] == {'add': '27.32', 'max': '136.58', 'method': 'ceil', 'min': '54.64', 'mult': '0.1'}
        assert user1.merchant1.resp_sci_subpay['min'] == '3'
        assert user1.merchant1.resp_sci_subpay['max'] == '100'
        assert user1.merchant1.resp_sci_subpay['rate'] == ['1', '27.31638']


# @pytest.mark.usefixtures('_create_sci_sub_pay_list')
class TestSciSubPayList:
    """ Checking sub_pay orders list. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2, sci_pay_order
        admin, user1, user2 = start_session
        sci_pay_order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40][0]

    def test_sci_sub_pay_list_1(self):
        """ Getting full list by order token of sub_pay orders by MERCHANT. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)
                  if dct['base_order_id'] == sci_pay_order['id']][0:3]
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': sci_pay_order['token'], 'first': None, 'count': None})
        print(user1.merchant1.resp_sci_subpay)
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_subpay['data']]
        assert adm_ls == us_ls

    def test_sci_sub_pay_list_2(self):
        """ Getting list of first two elements list of sub_pay orders by OWNER. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)
                  if dct['base_order_id'] == sci_pay_order['id']][0:2]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'list', 'sci_pay_token': sci_pay_order['token'],
                               'first': None, 'count': '2'})
        us_ls = [dct['ctime'] for dct in user1.resp_delegate['data']]
        print(adm_ls, us_ls)
        assert adm_ls == us_ls

    def test_sci_sub_pay_list_3(self):
        """ Getting list from second element by MERCHANT. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)
                  if dct['base_order_id'] == sci_pay_order['id']][1:]
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': sci_pay_order['token'], 'first': '1', 'count': None})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_subpay['data']]
        print(adm_ls, us_ls)
        assert adm_ls == us_ls

    def test_sci_sub_pay_list_4(self):
        """ Getting list from second element with count 2 list of sub_pay orders by OWNER. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)
                  if dct['base_order_id'] == sci_pay_order['id']][1:3]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'list', 'sci_pay_token': sci_pay_order['token'],
                               'first': '1', 'count': '2'})
        us_ls = [dct['ctime'] for dct in user1.resp_delegate['data']]
        assert adm_ls == us_ls

    def test_sci_sub_pay_list_5(self):
        """ Getting full list of sub_pay orders by MERCHANT. """
        adm_ls = [dct['ctime'] for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id)
                  if dct['tp'] == 45][:20]
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': None, 'first': None, 'count': None})
        us_ls = [dct['ctime'] for dct in user1.merchant1.resp_sci_subpay['data']]
        assert adm_ls == us_ls


class TestWrongSciSubPayList:
    """ Wrong request to sci_subpay method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_sci_sub_pay_list_1(self):
        """ Request with int type in first parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': 1, 'count': None})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                                                            'value': 1}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_list_2(self):
        """ Request with int type in first parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': '0.7', 'count': None})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'first', 'reason': 'Should be an Integer'},
                                                   'message': 'EParamType'}

    def test_wrong_sci_sub_pay_list_3(self):
        """ Request with negative number in first parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': '-1', 'count': None})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'first', 'reason': 'Should be a positive Number'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_list_4(self):
        """ Request with int type in count parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': None, 'count': 1})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'count', 'reason': "'count' must not be of 'int' type",
                                                                            'value': 1}, 'message': 'EParamType'}

    def test_wrong_sci_sub_pay_list_5(self):
        """ Request with int type in count parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': None, 'count': '0.6'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32003, 'data': {'field': 'count', 'reason': 'Should be an Integer'},
                                                   'message': 'EParamType'}

    def test_wrong_sci_sub_pay_list_6(self):
        """ Request with int type in count parameter. """
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': '123', 'first': None, 'count': '-1'})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'count', 'reason': 'Should be more than zero'},
                                                   'message': 'EParamInvalid'}

    def test_wrong_sci_sub_pay_list_7(self, _create_payin_order):
        """ Request with payin order token. """
        payin_order = admin.get_model(model='order', _filter='tp', value=0)[0]
        user1.merchant1.sci_subpay(method='list', params={'sci_pay_token': payin_order['token'], 'first': None, 'count': None})
        assert user1.merchant1.resp_sci_subpay == {'code': -32002, 'data': {'field': 'order_token', 'reason': 'Invalid order_token value',
                                                   'value': payin_order['token']}, 'message': 'EParamInvalid'}


@pytest.mark.usefixtures('_create_sci_sub_pay_list')
class TestSciSubPayGet:
    """ Checking sub_pay orders list. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_sub_pay_get_1(self):
        """ Getting lust sub_pay order by MERCHANT. """
        sub_pay_order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 45][0]
        user1.merchant1.sci_subpay(method='get', params={'sci_pay_token': sub_pay_order['token']})
        assert user1.merchant1.resp_sci_subpay['token'] == sub_pay_order['token']
        assert user1.merchant1.resp_sci_subpay['lid'] == sub_pay_order['lid']

    def test_sci_sub_pay_get_2(self):
        """ Getting before lust sub_pay order by OWNER. """
        sub_pay_order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 45][1]
        admin.set_order_status(lid=sub_pay_order['lid'], status=100)
        user1.delegate = user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'get',
                                                'sci_pay_token': sci_pay_order['token']})
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'sci_subpay', 'merch_method': 'get',
                               'sci_pay_token': sci_pay_order['token']})
        assert user1.resp_delegate['token'] == sub_pay_order['token']
        assert user1.resp_delegate['lid'] == sub_pay_order['lid']


class TestSciSubPayCancel:
    """ Checking sub_pay orders list. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_sci_sub_pay_cancel_1(self):
        """ Getting lust sub_pay order by MERCHANT. """
        sub_pay_order = [dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 45][0]
        user1.merchant1.sci_subpay(method='get', params={'sci_pay_token': sub_pay_order['token']})
        assert user1.merchant1.resp_sci_subpay['token'] == sub_pay_order['token']
        assert user1.merchant1.resp_sci_subpay['lid'] == sub_pay_order['lid']

