import requests
import pytest
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.positive
@pytest.mark.usefixtures('_personal_exchange_fee')
class TestConvertCalc:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_convert_calc_1(self):
        """ Calc exchange UAH to USD: baying 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.29),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': None, 'out_amount': '0.01'})
        assert user1.resp_delegate['in_amount'] == '0.29'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']

    def test_convert_calc_2(self):
        """ Calc convert UAH to USD: baying 2.78 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '2.78', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '78.4'
        assert user1.merchant1.resp_convert['out_amount'] == '2.78'

    def test_convert_calc_3(self):
        """ Calc exchange USD to UAH: baying 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.01', 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert['rate'] == ['1', '28.1999']

    def test_convert_calc_4(self):
        """ Calc exchange USD to UAH: baying 33.15 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_curr': 'USD', 'out_curr': 'UAH', 'in_amount': None, 'out_amount': '33.15'})
        assert user1.resp_delegate['in_amount'] == '1.18'
        assert user1.resp_delegate['out_amount'] == '33.15'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']

    def test_convert_calc_5(self):
        """ Calc exchange USD to UAH: selling 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_curr': 'USD', 'out_curr': 'UAH', 'in_amount': '0.01', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.28'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']

    def test_convert_calc_6(self):
        """ Exchange USD to UAH: selling 2.15 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(7.55), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.merchant1.convert(method='calc', params={'in_amount': '2.15', 'out_amount': None, 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert['in_amount'] == '2.15'
        assert user1.merchant1.resp_convert['out_amount'] == '60.62'
        assert user1.merchant1.resp_convert['rate'] == ['1', '28.1999']

    def test_convert_calc_7(self):
        """ Calc exchange UAH to USD: selling 45.19 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': '45.19', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '45.19'
        assert user1.merchant1.resp_convert['out_amount'] == '1.6'
        assert user1.merchant1.resp_convert['rate'] == ['28.1999', '1']

    def test_convert_calc_8(self):
        """ Calc exchange UAH to USD: selling 0.28 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': '0.28', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.28'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']

    def test_convert_calc_9(self):
        """ Calc exchange UAH to BTC: baying 0.000 01 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.00001', 'in_curr': 'UAH', 'out_curr': 'BTC'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.18'
        assert user1.merchant1.resp_convert['out_amount'] == '0.00001'
        assert user1.merchant1.resp_convert['rate'] == ['17919.3156', '1']

    def test_convert_calc_10(self):
        """ Calc exchange UAH to BTC: baying 0.000 000 01 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'UAH', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.00000001'})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.00000001'
        assert user1.resp_delegate['rate'] == ['17919.3156', '1']

    def test_convert_calc_11(self):
        """ Calc exchange USD to BTC: baying 0.005 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(18), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.0003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'USD', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.005'})
        assert user1.resp_delegate['in_amount'] == '17.91'
        assert user1.resp_delegate['out_amount'] == '0.005'
        assert user1.resp_delegate['rate'] == ['3580.6541', '1']

    def test_convert_calc_12(self):
        """ Calc exchange BTC to USD: baying 0.01 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.0000001),
                                tech_max=bl(3))
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.01', 'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.0000028'
        assert user1.merchant1.resp_convert['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert['rate'] == ['1', '3580.6541']

    def test_convert_calc_13(self):
        """ Calc exchange UAH to BTC: selling 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert(method='calc', params={'in_amount': '0.01', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'BTC'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert['out_amount'] == '0.00000055'
        assert user1.merchant1.resp_convert['rate'] == ['17919.3156', '1']

    def test_convert_calc_14(self):
        """ Calc exchange BTC to UAH: selling 0.000 000 55 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.01), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000055),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'BTC', 'out_curr': 'UAH',
                               'in_amount': '0.00000055', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.00000055'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['rate'] == ['1', '17919.3156']

    def test_convert_calc_15(self):
        """ Exchange BTC to USD: selling 0.005 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.5), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': '0.005', 'out_amount': None, 'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.005'
        assert user1.merchant1.resp_convert['out_amount'] == '17.9'
        assert user1.merchant1.resp_convert['rate'] == ['1', '3580.6541']

    def test_convert_calc_16(self):
        """ Calc exchange UAH to USD: baying 2 USD by OWNER with common fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(80), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(0.1), in_currency='UAH', out_currency='USD')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': None, 'out_amount': '2'})
        assert user1.resp_delegate['in_amount'] == '56.46'
        assert user1.resp_delegate['out_amount'] == '2'
        assert user1.resp_delegate['rate'] == ['28.2281', '1']

    def test_convert_calc_17(self):
        """ Calc exchange USD to UAH: selling 2 USD by MERCHANT with common fee 50% for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(50), in_currency='USD', out_currency='UAH')
        user1.merchant1.convert(method='calc', params={'in_amount': '2', 'out_amount': None, 'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert['in_amount'] == '2'
        assert user1.merchant1.resp_convert['out_amount'] == '28.19'
        assert user1.merchant1.resp_convert['rate'] == ['1', '14.09995']

    def test_convert_calc_18(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc exchange UAH to USD: selling 45.15 UAH by MERCHANT with personal fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(2.3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(0.1))
        user1.merchant1.convert(method='calc', params={'in_amount': '45.15', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '45.15'
        assert user1.merchant1.resp_convert['out_amount'] == '1.59'
        assert user1.merchant1.resp_convert['rate'] == ['28.2281', '1']

    def test_convert_calc_19(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc exchange UAH to RUB: baying 35 RUB by OWNER with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(14), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': None, 'out_amount': '35'})
        assert user1.resp_delegate['in_amount'] == '13.4'
        assert user1.resp_delegate['out_amount'] == '35'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']

    def test_convert_calc_20(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc exchange UAH to USD: baying 2.40 USD by MERCHANT with common fee 3.3% for exchange
            and with personal fee 2.1% for exchange. """
        admin.set_wallet_amount(balance=bl(70), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.3), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2.1))
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '2.40', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '69.11'
        assert user1.merchant1.resp_convert['out_amount'] == '2.4'
        assert user1.merchant1.resp_convert['rate'] == ['28.7921', '1']

    def test_convert_calc_21(self, _custom_fee, _disable_personal_exchange_fee):
        """ Calc exchange UAH to RUB: selling 10 UAH by OWNER with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'calc', 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': '10', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '26.13'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']

    def test_convert_calc_22(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange BTC to USD: baying 4.4 USD by MERCHANT with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(0.005), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(3), in_currency='BTC', out_currency='USD', tech_min=bl(0.0002),
                                tech_max=bl(3000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '4.4', 'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert['in_amount'] == '0.00125391'
        assert user1.merchant1.resp_convert['out_amount'] == '4.4'
        assert user1.merchant1.resp_convert['rate'] == ['1', '3509.04101']


@pytest.mark.negative
class TestWrongConvertCalc:
    """ Wrong Calc"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    @pytest.mark.skip(reason='Fail')
    def test_wrong_convert_calc_1(self, _merchant_activate):
        """ Calc convert with inactive merchant. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': '50', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32031, 'message': 'EStateMerchantInactive',
                                                'data': {'field': 'x-merchant', 'reason': 'Merchant inactive'}}

    def test_wrong_convert_calc_2(self):
        """ Request with int's and float's in in_curr and out_curr. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': 50, 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32003, 'message': 'EParamType',
                                                'data': {'field': 'in_amount', 'reason': "'in_amount' must not be of 'int' type", 'value': 50}}
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': 1.5, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32003, 'message': 'EParamType',
                                                'data': {'field': 'out_amount', 'reason': "'out_amount' must not be of 'float' type", 'value': 1.5}}

    def test_wrong_convert_calc_3(self):
        """ Calc with in_amount wrong format. """
        admin.set_wallet_amount(balance=bl(2), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': '1.122', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32082, 'data': {'field': 'amount'}, 'message': 'EParamAmountFormatInvalid'}
        user1.merchant1.convert(method='calc', params={'in_amount': 'String', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'field': 'in_amount', 'reason': 'Should be a Number'},
                                                'message': 'EParamInvalid'}

    def test_wrong_convert_calc_4(self):
        """ Calc with out_amount wrong format. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.015', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32082, 'data': {'field': 'amount'}, 'message': 'EParamAmountFormatInvalid'}
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': 'String', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'field': 'out_amount', 'reason': 'Should be a Number'},
                                                'message': 'EParamInvalid'}

    def test_wrong_convert_calc_5(self):
        """ Calc with equal pair of currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.5', 'in_curr': 'UAH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert == {'code': -32084, 'data': {'reason': 'Unavailable exchange from UAH to UAH'},
                                                'message': 'EStateExchangeUnavail'}

    def test_wrong_convert_calc_6(self):
        """ Calc without pair of currencies. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.5', 'in_curr': None, 'out_curr': None})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'field': 'in_curr', 'reason': 'Should be provided'},
                                                'message': 'EParamInvalid'}

    def test_wrong_convert_calc_7(self):
        """ Exchange without out_curr. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.2', 'in_curr': 'UAH', 'out_curr': None})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'field': 'out_curr', 'reason': 'Should be provided'},
                                                'message': 'EParamInvalid'}

    def test_wrong_convert_calc_9(self):
        """ Calc exchange in to not real currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.2', 'in_curr': 'UAH', 'out_curr': 'UDS'})
        assert user1.merchant1.resp_convert == {'code': -32014, 'data': {'field': 'out_curr', 'reason': 'Invalid currency name'},
                                                'message': 'EParamCurrencyInvalid'}

    def test_wrong_convert_calc_10(self):
        """ Exchange from not real currency. """
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.2', 'in_curr': 'UHA', 'out_curr': 'UDS'})
        assert user1.merchant1.resp_convert == {'code': -32014, 'data': {'field': 'in_curr', 'reason': 'Invalid currency name'},
                                                'message': 'EParamCurrencyInvalid'}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_convert_calc_11(self):
        """ Exchange in to not active currency."""
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.2', 'in_curr': 'UHA', 'out_curr': 'ETH'})
        assert user1.merchant1.resp_convert == {'code': -32033, 'data': {'field': 'curr', 'reason': 'Inactive'}, 'message': 'EStateCurrencyInactive'}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_convert_calc_12(self):
        """ Exchange from not active currency. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '0.2', 'in_curr': 'ETH', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert == {'code': -32033, 'data': {'field': 'curr', 'reason': 'Inactive'}, 'message': 'EStateCurrencyInactive'}

    @pytest.mark.skip(reason='Not disabled exchange pair')
    def test_wrong_convert_calc_13(self):
        """ Exchange with not active exchange pair. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': '0.1', 'out_amount': None, 'in_curr': 'ETH', 'out_curr': 'LTC'})
        assert user1.merchant1.resp_convert == {'code': -32084, 'data': {'reason': 'Unavailable exchange from ETH to LTC'},
                                                'message': 'EStateExchangeUnavail'}

    def test_wrong_convert_calc_14(self):
        """ Exchange WITH in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': '0.1', 'out_amount': '0.1', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'reason': 'Unable to complete: both/no amounts passed',
                                                                         'value': "['0.1', '0.1']"}, 'message': 'EParamInvalid'}

    def test_wrong_convert_calc_15(self):
        """ Exchange WITHOUT in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32002, 'data': {'reason': 'Unable to complete: both/no amounts passed',
                                                                         'value': '[None, None]'}, 'message': 'EParamInvalid'}

    def test_wrong_convert_calc_16(self):
        """ Exchange UAH to USD: baying 1 USD, in_amount with fee less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(31.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), in_currency='UAH', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '1', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32056, 'message': 'EStateInsufficientFunds',
                                                'data': {'reason': 'Balance 31.01 less then amount 31.02'}}

    def test_wrong_convert_calc_17(self):
        """ Exchange UAH to USD: selling 50.01 UAH, in_amount less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': '50.01', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32072, 'message': 'InsufficientFunds',
                                                'data': {'reason': 'Balance 50 less then amount 50.01 in UAH'}}

    def test_wrong_convert_calc_18(self):
        """ Exchange UAH to USD: selling 31.02 UAH with in_amount less than admin_min in exchange table
            Exchange UAH to USD: selling 93.06 UAH with in_amount more than admin_max in exchange table.
            Exchange UAH to USD: baying 1 USD with in_amount less than admin_min in exchange table.
            Exchange UAH to USD: baying 3 USD with in_amount more than admin_max in exchange table. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), tech_min=bl(31.03), tech_max=bl(93.05),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.convert(method='calc', params={'in_amount': '31.02', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '31.02'}}
        user1.merchant1.convert(method='calc', params={'in_amount': '93.06', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '93.06'}}
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '1', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '31.02'}}
        user1.merchant1.convert(method='calc', params={'in_amount': None, 'out_amount': '3', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '93.06'}}

    def test_wrong_convert_calc_19(self):
        """ Exchange with wrong sign. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.calc', 'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '10', 'out_amount': None},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_convert_calc_20(self):
        """ Exchange without sign = None. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.calc', 'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {"code": -32012, "message": "EParamHeadersInvalid",
                                          "data": {"field": "x-signature", "reason": "Not present"}}

    def test_wrong_convert_calc_21(self):
        """ Exchange with wrong merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.calc', 'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_convert_calc_22(self):
        """ Exchange with None merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.calc', 'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': 1, 'out_amount': None},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_convert_calc_23(self):
        """ Exchange without IN_CURR parameter. """
        user1.merchant1.convert(method='calc', params={'in_amount': '0.1', 'out_amount': None, 'out_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'convert.calc' missing 1 argument: 'in_curr'"}}

    def test_wrong_convert_calc_24(self):
        """ Exchange without OUT_CURR parameter. """
        user1.merchant1.convert(method='calc', params={'in_amount': '0.1', 'out_amount': None, 'in_curr': 'USD'})
        assert user1.merchant1.resp_convert == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'convert.calc' missing 1 argument: 'out_curr'"}}

    def test_wrong_convert_calc_25(self):
        """ Exchange without IN_AMOUNT and OUT_AMOUNT. """
        user1.merchant1.convert(method='calc', params={'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.merchant1.resp_convert == {'code': -32070, 'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                                         "'out_amount'"}, 'message': 'InvalidInputParams'}

    def test_wrong_convert_calc_26(self):
        """ Exchange with excess parameter in params field. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='calc', params={'in_amount': '5', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'USD', 'par': '123'})
        assert user1.merchant1.resp_convert == {'code': -32602, 'message': 'InvalidInputParams',
                                                'data': {'reason': "method 'convert.calc' received a redundant argument 'par'"}}


@pytest.mark.usefixtures('_personal_exchange_fee')
class TestConvertCreate:
    """ Exchanging currency. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_exchange_1(self):
        """ Exchange UAH to USD: baying 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.29),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': None, 'out_amount': '0.01'})
        assert user1.resp_delegate['in_amount'] == '0.29'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']


    def test_exchange_2(self):
        """ Exchange UAH to USD: baying 2.78 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount=None, out_amount='2.78', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '78.4'
        assert user1.merchant1.resp_convert_create['out_amount'] == '2.78'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        '''
        assert user1.merchant1.balance(curr='UAH') == '21.6'
        assert user1.merchant1.balance(curr='USD') == '2.78'
        '''


    def test_exchange_3(self):
        """ Exchange USD to UAH: baying 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.01', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '28.1999']


    def test_exchange_4(self):
        """ Exchange USD to UAH: baying 33.15 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'UAH',
                               'in_amount': None, 'out_amount': '33.15'})
        assert user1.resp_delegate['in_amount'] == '1.18'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '33.15'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.82'
        assert user1.merchant1.balance(curr='UAH') == '33.15'
        '''


    def test_exchange_5(self):
        """ Exchange USD to UAH: selling 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'UAH',
                               'in_amount': '0.01', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '0.28'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']


    def test_exchange_6(self):
        """ Exchange USD to UAH: selling 2.15 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(7.55), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.merchant1.convert_create(in_amount='2.15', out_amount=None, in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '2.15'
        assert user1.merchant1.resp_convert_create['out_amount'] == '60.62'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '28.1999']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.85'
        assert user1.merchant1.balance(curr='UAH') == '68.17'
        '''


    def test_exchange_7(self):
        """ Exchange UAH to USD: selling 45.19 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='45.19', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '45.19'
        assert user1.merchant1.resp_convert_create['out_amount'] == '1.6'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.1999', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '4.81'
        assert user1.merchant1.balance(curr='USD') == '1.6'
        '''


    def test_exchange_8(self):
        """ Exchange UAH to USD: selling 0.28 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': '0.28', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.28'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']

    def test_exchange_9(self):
        """ Exchange UAH to BTC: baying 0.000 01 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.00001', in_curr='UAH', out_curr='BTC')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.18'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.00001'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['rate'] == ['17919.3156', '1']


    def test_exchange_10(self):
        """ Exchange UAH to BTC: baying 0.000 000 01 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.00000001'})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.00000001'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['rate'] == ['17919.3156', '1']

    def test_exchange_11(self):
        """ Exchange USD to BTC: baying 0.005 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(18), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.0003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.005'})
        assert user1.resp_delegate['in_amount'] == '17.91'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '0.005'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['rate'] == ['3580.6541', '1']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.09'
        assert user1.merchant1.balance(curr='BTC') == '0.0053'
        '''

    def test_exchange_12(self):
        """ Exchange BTC to USD: baying 0.01 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.0000001),
                                tech_max=bl(3))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.01', in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.0000028'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3580.6541']


    def test_exchange_13(self):
        """ Exchange UAH to BTC: selling 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount='0.01', out_amount=None, in_curr='UAH', out_curr='BTC')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.00000055'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['rate'] == ['17919.3156', '1']


    def test_exchange_14(self):
        """ Exchange BTC to UAH: selling 0.000 000 55 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.01), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000055),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'BTC', 'out_curr': 'UAH',
                               'in_amount': '0.00000055', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.00000055'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '17919.3156']


    def test_exchange_15(self):
        """ Exchange BTC to USD: selling 0.005 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.5), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD')
        user1.merchant1.convert_create(in_amount='0.005', out_amount=None, in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.005'
        assert user1.merchant1.resp_convert_create['out_amount'] == '17.9'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3580.6541']
        '''
        assert user1.merchant1.balance(curr='BTC') == '0'
        assert user1.merchant1.balance(curr='USD') == '17.9'
        '''


    def test_exchange_16(self):
        """ Exchange UAH to USD: baying 2 USD by OWNER with common fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(80), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(0.1), in_currency='UAH', out_currency='USD')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': None, 'out_amount': '2'})
        assert user1.resp_delegate['in_amount'] == '56.46'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '2'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.2281', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '23.54'
        assert user1.merchant1.balance(curr='USD') == '2'
        '''


    def test_exchange_17(self):
        """ Exchange USD to UAH: selling 2 USD by MERCHANT with common fee 50% for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(50), in_currency='USD', out_currency='UAH')
        user1.merchant1.convert_create(in_amount='2', out_amount=None, in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '2'
        assert user1.merchant1.resp_convert_create['out_amount'] == '28.19'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '14.09995']
        '''
        assert user1.merchant1.balance(curr='USD') == '0'
        assert user1.merchant1.balance(curr='UAH') == '28.19'
        '''

    def test_exchange_18(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to USD: selling 45.15 UAH by MERCHANT with personal fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(2.3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(0.1))
        user1.merchant1.convert_create(in_amount='45.15', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '45.15'
        assert user1.merchant1.resp_convert_create['out_amount'] == '1.59'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.2281', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '4.85'
        assert user1.merchant1.balance(curr='USD') == '3.89'
        '''

    def test_exchange_19(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to RUB: baying 35 RUB by OWNER with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(14), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': None, 'out_amount': '35'})
        assert user1.resp_delegate['in_amount'] == '13.4'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '35'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0.6'
        assert user1.merchant1.balance(curr='USD') == '45'
        '''

    def test_exchange_20(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to USD: baying 2.40 USD by MERCHANT with common fee 3.3% for exchange
            and with personal fee 2.1% for exchange. """
        admin.set_wallet_amount(balance=bl(70), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.3), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2.1))
        user1.merchant1.convert_create(in_amount=None, out_amount='2.40', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '69.11'
        assert user1.merchant1.resp_convert_create['out_amount'] == '2.4'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.7921', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0.89'
        assert user1.merchant1.balance(curr='USD') == '2.9'
        '''


    def test_exchange_21(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to RUB: selling 10 UAH by OWNER with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': '10', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '26.13'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0'
        assert user1.merchant1.balance(curr='RUB') == '26.13'
        '''

    def test_exchange_22(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange BTC to USD: baying 4.4 USD by MERCHANT with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(0.005), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(3), in_currency='BTC', out_currency='USD', tech_min=bl(0.0002),
                                tech_max=bl(3000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.merchant1.convert_create(in_amount=None, out_amount='4.4', in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.00125391'
        assert user1.merchant1.resp_convert_create['out_amount'] == '4.4'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3509.04101']
        '''
        assert user1.merchant1.balance(curr='BTC') == '0.04874609'
        assert user1.merchant1.balance(curr='USD') == '5.9'
        '''


class TestWrongConvert:
    """ Wrong convert. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_exchange_1(self, _merchant_activate):
        """ Exchange with inactive merchant. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='50', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32010, 'message': 'InvalidMerchant',
                                                       'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_exchange_2(self):
        """ Request with int's and float's in in_curr and out_curr. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=50, out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data': {'reason': "Key 'in_amount' must not be of 'int' type"}}
        user1.merchant1.convert_create(in_amount=None, out_amount=1.5, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data': {'reason': "Key 'out_amount' must not be of 'float' type"}}

    def test_wrong_exchange_3(self):
        """ Exchange with in_amount wrong format. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='1.122', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                       'data': {'reason': 'Invalid format 1.122 for UAH'}}
        user1.merchant1.convert_create(in_amount='String', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data': {'field': 'in_amount', 'reason': 'Should be a Number'}}

    def test_wrong_exchange_4(self):
        """ Exchange with out_amount wrong format. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.015', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat',
                                                       'data': {'reason': 'Invalid format 0.015 for USD'}}
        user1.merchant1.convert_create(in_amount=None, out_amount='String', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data':  {'field': 'out_amount', 'reason': 'Should be a Number'}}

    def test_wrong_exchange_5(self):
        """ Exchange with equal pair of currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_convert_create == {'code': -32065, 'message': 'UnavailExchange',
                                                       'data': {'reason': 'Unavailable exchange from UAH to UAH'}}

    def test_wrong_exchange_6(self):
        """ Exchange without pair of currencies. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr=None, out_curr=None)
        assert user1.merchant1.resp_convert_create == {'code': -32602, 'message': 'InvalidInputParams',
                                                       'data': {'reason': "method 'convert.create' missing 2 arguments: 'in_curr' and 'out_curr'"}}

    def test_wrong_exchange_7(self):
        """ Exchange without in_curr. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr=None, out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32602, 'message': 'InvalidInputParams',
                                                       'data': {'reason': "method 'convert.create' missing 1 argument: 'in_curr'"}}

    def test_wrong_exchange_8(self):
        """ Exchange without out_curr. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr=None)
        assert user1.merchant1.resp_convert_create == {'code': -32602, 'message': 'InvalidInputParams',
                                                       'data': {'reason': "method 'convert.create' missing 1 argument: 'out_curr'"}}

    def test_wrong_exchange_9(self):
        """ Exchange in to not real currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UDS')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency',
                                                       'data': {'field': 'out_curr', 'reason': 'Invalid currency name'}}

    def test_wrong_exchange_10(self):
        """ Exchange from not real currency. """
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UHA', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency',
                                                       'data': {'field': 'in_curr', 'reason': 'Invalid currency name'}}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_exchange_11(self):
        """ Exchange in to not active currency."""
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='10', out_amount=None, in_curr='UAH', out_curr='ETH')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_exchange_12(self):
        """ Exchange from not active currency. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='UAH')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not disabled exchange pair')
    def test_wrong_exchange_13(self):
        """ Exchange with not active exchange pair. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='LTC')
        assert user1.merchant1.resp_convert_create == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_exchange_14(self):
        """ Exchange WITH in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='1', out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070,
                                                       'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                                "'out_amount'"}, 'message': 'InvalidParam'}

    def test_wrong_exchange_15(self):
        """ Exchange WITHOUT in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070,
                                                       'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                                "'out_amount'"}, 'message': 'InvalidParam'}

    def test_wrong_exchange_16(self):
        """ Exchange UAH to USD: baying 1 USD, in_amount with fee less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(31.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32072, 'message': 'InsufficientFunds',
                                                       'data': {'reason': 'Balance 31.01 less then amount 31.02 in UAH'}}

    def test_wrong_exchange_17(self):
        """ Exchange UAH to USD: selling 50.01 UAH, in_amount less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='50.01', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32072, 'message': 'InsufficientFunds',
                                                       'data': {'reason': 'Balance 50 less then amount 50.01 in UAH'}}

    def test_wrong_exchange_18(self):
        """ Exchange UAH to USD: selling 31.02 UAH with in_amount less than admin_min in exchange table
            Exchange UAH to USD: selling 93.06 UAH with in_amount more than admin_max in exchange table.
            Exchange UAH to USD: baying 1 USD with in_amount less than admin_min in exchange table.
            Exchange UAH to USD: baying 3 USD with in_amount more than admin_max in exchange table. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), tech_min=bl(31.03), tech_max=bl(93.05),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='31.02', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '31.02'}}
        user1.merchant1.convert_create(in_amount='93.06', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '93.06'}}
        user1.merchant1.convert_create(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32075, 'message': 'AmountTooSmall', 'data': {'reason': '31.02'}}
        user1.merchant1.convert_create(in_amount=None, out_amount='3', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32074, 'message': 'AmountTooBig', 'data': {'reason': '93.06'}}

    def test_wrong_exchange_19(self):
        """ Exchange with wrong sign. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '10', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_exchange_20(self):
        """ Exchange without sign = None. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {"code": -32012, "message": "EParamHeadersInvalid", "data": {"field": "x-signature", "reason": "Not present"}}

    def test_wrong_exchange_21(self):
        """ Exchange without SIGN in headers. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {"code": -32012, "message": "EParamHeadersInvalid", "data": {"field": "x-signature", "reason": "Not present"}}

    def test_wrong_exchange_22(self):
        """ Exchange with wrong merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_exchange_23(self):
        """ Exchange with None merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': 1, 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_exchange_24(self):
        """ Exchange without merchant id in headers. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_exchange_25(self):
        """ Exchange without IN_CURR parameter. """
        data = {'method': 'convert.create',
                'params': {'out_curr': 'USD', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.create' missing 1 argument: 'in_curr'"}}

    def test_wrong_exchange_26(self):
        """ Exchange without OUT_CURR parameter. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {"reason": "method 'convert.create' missing 1 argument: 'out_curr'"}}

    def test_wrong_exchange_27(self):
        """ Exchange without IN_AMOUNT and OUT_AMOUNT. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'externalid': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32070,
                                          'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                             "'out_amount'"}, 'message': 'InvalidParam'}

    def test_wrong_exchange_28(self):
        """ Exchange without EXTERNAL_ID. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, "data": {'reason': "method 'convert.create' missing 1 argument: 'externalid'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_exchange_29(self):
        """ Exchange with equal EXTERNAL_ID. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        ex_id = user1.merchant1._id()
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None, 'externalid': ex_id},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        requests.post(url=user1.merchant1.japi_url, json=data,
                      headers={'x-merchant': str(user1.merchant1.lid),
                               'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                               'x-utc-now-ms': time_sent}, verify=False)
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32033, 'data': {'reason': 'Duplicated key for externalid'}, 'message': 'Unique'}

    def test_wrong_exchange_30(self):
        """ Exchange with excess parameter in params field. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None,
                           'externalid': user1.merchant1._id(), 'par': '123'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.create' received a redundant argument 'par'"}}


@pytest.mark.usefixtures('_personal_exchange_fee')
class TestConvertParams:
    """ Testing convert params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_params_1(self):
        """ Getting params for UAH -> USD by MERCHANT. """
        admin.set_wallet_amount(balance=bl(1.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(0.01), tech_max=bl(3000),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_params(in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_params['is_convert'] is True
        assert user1.merchant1.resp_convert_params['in_curr_balance'] == '1.01'
        assert user1.merchant1.resp_convert_params['in_min'] == '0.01'
        assert user1.merchant1.resp_convert_params['in_max'] == '3000'
        assert user1.merchant1.resp_convert_params['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_params['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_params['rate'] == ['28.1999', '1']

    def test_params_2(self):
        """ Getting params for RUB -> UAH by OWNER. """
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(10),
                                tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.resp_delegate['out_min'] == '3.76'
        assert user1.resp_delegate['out_max'] == '37.5'
        assert user1.resp_delegate['rate'] == ['2.6666', '1']
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_3(self):
        """ Getting params for BTC -> USD by OWNER. """
        admin.set_wallet_amount(balance=bl(0.02), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.001),
                                tech_max=bl(1.3))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.resp_delegate['in_min'] == '0.001'
        assert user1.resp_delegate['in_max'] == '1.3'
        assert user1.resp_delegate['out_min'] == '3.59'
        assert user1.resp_delegate['out_max'] == '4654.85'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['1', '3580.6541']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.00000001),
                                tech_max=bl(3))

    def test_params_4(self):
        """ Getting params for USD -> UAH by OWNER with 3.8 percent common fee. """
        admin.set_wallet_amount(balance=bl(5.11), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.8), in_currency='USD', out_currency='UAH', tech_min=bl(0.5),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.resp_delegate['in_curr_balance'] == '5.11'
        assert user1.resp_delegate['in_min'] == '0.5'
        assert user1.resp_delegate['in_max'] == '3000'
        assert user1.resp_delegate['out_min'] == '13.57'
        assert user1.resp_delegate['out_max'] == '81384.9'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '27.1283']
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_5(self):
        """ Getting params for USD -> BTC by MERCHANT with 5 percent common fee. """
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(5), in_currency='USD', out_currency='BTC', tech_min=bl(3),
                                tech_max=bl(3000))
        user1.merchant1.convert_params(in_curr='USD', out_curr='BTC')
        assert user1.merchant1.resp_convert_params['in_curr_balance'] == '15'
        assert user1.merchant1.resp_convert_params['in_min'] == '3'
        assert user1.merchant1.resp_convert_params['in_max'] == '3000'
        assert user1.merchant1.resp_convert_params['out_min'] == '0.00079794'
        assert user1.merchant1.resp_convert_params['out_max'] == '0.7979388'
        assert user1.merchant1.resp_convert_params['rate'] == ['3759.68681', '1']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_6(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for UAH -> RUB by MERCHANT with 5% common fee and 3% personal fee. """
        admin.set_wallet_amount(balance=bl(15), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(5), in_currency='UAH', out_currency='RUB', tech_min=bl(17),
                                tech_max=bl(950))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3))
        user1.merchant1.convert_params(in_curr='UAH', out_curr='RUB')
        assert user1.merchant1.resp_convert_params['in_min'] == '17'
        assert user1.merchant1.resp_convert_params['in_max'] == '950'
        assert user1.merchant1.resp_convert_params['out_min'] == '43.98'
        assert user1.merchant1.resp_convert_params['out_max'] == '2457.27'
        assert user1.merchant1.resp_convert_params['rate'] == ['1', '2.5866']
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='USD', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_7(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for BTC -> USD by OWNER with 5% common fee and 3% personal fee. """
        admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(5), in_currency='BTC', out_currency='USD', tech_min=bl(0.1),
                                tech_max=bl(3))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.resp_delegate['out_min'] == '347.33'
        assert user1.resp_delegate['out_max'] == '10419.7'
        assert user1.resp_delegate['rate'] == ['1', '3473.23447']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.00000001),
                                tech_max=bl(3))


class TestWrongConvertParams:
    """ Testing wrong requests for exchange params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_params_1(self):
        """ Getting params for equal currency. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_convert_params == {'code': -32084, 'message': 'EStateExchangeUnavail',
                                                       'data': {'reason': 'Unavailable exchange from UAH to UAH'}}

    def test_wrong_params_2(self):
        """ Getting params from not real currency. """
        user1.merchant1.convert_params(in_curr='UHA', out_curr='USD')
        assert user1.merchant1.resp_convert_params == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                                       'data': {'field': 'in_curr', 'reason': 'Invalid currency name'}}

    def test_wrong_params_3(self):
        """ Getting params to not real currency. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr='UDS')
        assert user1.merchant1.resp_convert_params == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                                       'data': {'field': 'out_curr', 'reason': 'Invalid currency name'}}

    def test_wrong_params_4(self):
        """ Getting params with NONE in_curr. """
        user1.merchant1.convert_params(in_curr=None, out_curr='USD')
        assert user1.merchant1.resp_convert_params == {'code': -32002, 'message': 'EParamInvalid',
                                                       'data': {'field': 'in_curr', 'reason': 'Should be provided'}}

    def test_wrong_params_5(self):
        """ Getting params with NONE out_curr. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr=None)
        assert user1.merchant1.resp_convert_params == {'code': -32002, 'message': 'EParamInvalid',
                                                       'data': {'field': 'out_curr', 'reason': 'Should be provided'}}

    def test_wrong_params_6(self):
        """ Getting params without in_curr parameter. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params', 'params': {'out_curr': 'USD'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {"code": -32002, "message": "EParamInvalid",
                                          "data": {"field": "in_curr", "reason": "Should be provided"}}

    def test_wrong_params_7(self):
        """ Getting params without out_curr parameter. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params', 'params': {'in_curr': 'USD'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {"code": -32002, "message": "EParamInvalid",
                                          "data": {"field": "out_curr", "reason": "Should be provided"}}

    def test_wrong_params_8(self):
        """ Getting params with excess parameter in params field. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'par': 'boom'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {"code": -32002, "message": "EParamInvalid",
                                          "data": {"field": "par", "reason": "Should not be provided"}}

    def test_wrong_params_9(self):
        """ Getting params with NONE signature. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {"code": -32012, "message": "EParamHeadersInvalid",
                                          "data": {"field": "x-signature", "reason": "Not present"}}

    def test_wrong_params_10(self):
        """ Getting params with wrong signature. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD'},
                'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'EParamSignInvalid',
                                          'data': {'reason': 'Invalid signature'}}


@pytest.mark.usefixtures('_create_convert_order')
class TestConvertGet:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_convert_get_1(self):
        """ Getting order by oid by MERCHANT. """
        order = [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if ls['tp'] == 20][0]
        user1.merchant1.convert(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_convert['in_amount'] == str(int(orig(order['in_amount'])))
        assert user1.merchant1.resp_convert['ctime'] == order['ctime']

    def test_convert_get_2(self):
        """ Getting order by oid by MERCHANT. Checking all keys. """
        ls_keys = ['account_amount', 'ctime', 'externalid', 'ftime', 'in_amount', 'in_curr', 'in_fee_amount', 'lid', 'orig_amount',
                   'out_amount', 'out_curr', 'out_fee_amount', 'owner', 'payee', 'payway_name', 'rate', 'ref', 'renumeration', 'reqdata',
                   'status', 'tgt', 'token', 'tp', 'userdata']
        ls_keys.sort()
        order = [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if ls['tp'] == 20][0]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'get', 'o_lid': str(order['lid'])})
        us_ls = [ls for ls in user1.resp_delegate]
        us_ls.sort()
        assert us_ls == ls_keys


@pytest.mark.usefixtures('_create_convert_order')
class TestWrongConvertGet:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_convert_get_1(self):
        """ Get not own order. """
        order = [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant2.id) if ls['tp'] == 20][0]
        user1.merchant1.convert(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_convert == {'code': -32090, 'data': {'reason': 'No order found with such params'},
                                                'message': 'NotFound'}

    def test_wrong_convert_get_2(self):
        """ Getting with int in O_LID parameter. """
        order = [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant2.id) if ls['tp'] == 20][0]
        user1.merchant1.convert(method='get', params={'o_lid': order['lid']})
        assert user1.merchant1.resp_convert == {'code': -32070, 'data': {'reason': "Key 'o_lid' must not be of 'int' type"},
                                                'message': 'InvalidParam'}

    def test_wrong_convert_get_3(self):
        """ Request with NONE O_LID parameter. """
        user1.merchant1.convert(method='get', params={'o_lid': None})
        assert user1.merchant1.resp_convert == {'code': -32602, 'data': {'reason': "method 'convert.get' missing 1 argument: "
                                                "'o_lid'"}, 'message': 'InvalidInputParams'}

    def test_wrong_convert_get_4(self):
        """ Request with excess parameter. """
        user1.merchant1.convert(method='get', params={'o_lid': '333', 'par': '123'})
        assert user1.merchant1.resp_convert == {'code': -32602, 'data': {'reason': "method 'convert.get' received a redundant "
                                                "argument 'par'"}, 'message': 'InvalidInputParams'}

    def test_wrong_convert_get_5(self, _merchant_activate):
        """ Request from inactive merchant. """
        order = [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if ls['tp'] == 20][0]
        user1.merchant1.convert(method='get', params={'o_lid': str(order['lid'])})
        assert user1.merchant1.resp_convert == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_convert_get_6(self):
        """ Getting params with not real merchant . """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.get', 'params': {'o_lid': '333'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '01',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_convert_get_7(self):
        """ Getting params without merchant . """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.get', 'params': {'o_lid': '333'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_convert_get_8(self):
        """ Getting params with wrong sign . """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.get', 'params': {'o_lid': '333'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant2.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_convert_get_9(self):
        """ Getting params without sign . """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.get', 'params': {'o_lid': '333'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_convert_get_10(self):
        """ Getting params without sign . """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.get', 'params': {'o_lid': '333'}, 'jsonrpc': user1.json_rpc, 'id': user1.ex_id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': user1.merchant1.lid,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': None}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


class TestConvertList:
    """ Testing convert list method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success no filter list test. """
        admin_count = int(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': '20'})[0]['count'])
        assert admin_count == user1.merchant1.convert_list()['total']

    def test_2(self):
        """ Success in_curr filter test. """
        curr = 'USD'
        r = user1.merchant1.convert_list(in_curr=curr)['data'][0]
        assert r['in_curr'] == curr, r

    def test_3(self):
        """ Unknown in_curr filter test. """
        curr = 'ГРН'
        r = user1.merchant1.convert_list(in_curr=curr)
        assert r['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                              'data': {'field': 'in_curr', 'reason': 'Invalid currency name'}}, r

    def test_4(self):
        """ Success out_curr filter test. """
        curr = 'USD'
        r = user1.merchant1.convert_list(out_curr=curr)['data'][0]
        assert r['out_curr'] == curr, r

    def test_5(self):
        """ Unknown out_curr filter test. """
        curr = 'ГРН'
        r = user1.merchant1.convert_list(out_curr=curr)
        assert r['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                              'data': {'field': 'out_curr', 'reason': 'Invalid currency name'}}, r

    def test_6(self):
        """ First filter test. """
        r = user1.merchant1.convert_list()['data'][1]
        test = user1.merchant1.convert_list(first='1')['data'][0]
        assert r == test

    def test_7(self):
        """ First filter test. """
        r = user1.merchant1.convert_list(first=1)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                       'value': 1}}

    def test_8(self):
        """ First filter test. """
        r = user1.merchant1.convert_list(first='one')
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'first', 'reason': 'Should be an Integer'}}

    def test_9(self):
        """ First filter test. """
        r = user1.merchant1.convert_list(first='9999999')['data']
        assert not r

    def test_10(self):
        """ Count filter test. """
        count = 10
        r = user1.merchant1.convert_list(count=str(count))
        len = r['data'].__len__()
        assert len == count or len == r['total']

    def test_11(self):
        """ Wrong Count filter test. """
        r = user1.merchant1.convert_list(count='0')
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'count', 'reason': 'Should be more than zero'}}

