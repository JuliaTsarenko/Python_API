import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

@pytest.mark.usefixtures('_personal_exchange_fee')
class TestConvertCalc:
    """ Convert Calc. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    # def test_Calc_Convert_1(self):
    #     """ Calc Convert UAH to USD: baying 0.01 USD by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.29),
    #                             tech_max=bl(3000))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid),  'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': None, 'out_amount': '0.01'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '0.29'
    #     assert user1.resp_delegate['orig_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['rate'] == ['28.1999', '1']
    #
    # def test_Calc_Convert_2(self):
    #     """ Calc Convert UAH to USD: baying 2.78 USD by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='2.78', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '78.4'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '2.78'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '2.78'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['28.1999', '1']
    #
    # def test_Calc_Convert_3(self):
    #     """ Calc Convert USD to UAH: baying 0.01 UAH by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.01', in_curr='USD', out_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '28.1999']
    #
    # def test_Calc_Convert_4(self):
    #     """ Calc Convert USD to UAH: baying 33.15 UAH by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'USD', 'out_curr': 'UAH', 'in_amount': None, 'out_amount': '33.15'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '1.18'
    #     assert user1.resp_delegate['orig_amount'] == '33.15'
    #     assert user1.resp_delegate['out_amount'] == '33.15'
    #     assert user1.resp_delegate['rate'] == ['1', '28.1999']
    #
    # def test_Calc_Convert_5(self):
    #     """ Calc Convert USD to UAH: selling 0.01 USD by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(0.1), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'USD', 'out_curr': 'UAH', 'in_amount': '0.01', 'out_amount': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['orig_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.28'
    #     assert user1.resp_delegate['rate'] == ['1', '28.1999']
    #
    # def test_Calc_Convert_6(self):
    #     """ Calc Convert USD to UAH: selling 2.15 USD by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(3), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(7.55), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
    #     user1.merchant1.convert_calc(in_amount='2.15', out_amount=None, in_curr='USD', out_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '2.15'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '2.15'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '60.62'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '28.1999']
    #
    # def test_Calc_Convert_7(self):
    #     """ Calc Convert UAH to USD: selling 45.19 UAH by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount='45.19', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '45.19'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '45.19'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '1.6'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['28.1999', '1']
    #
    # def test_Calc_Convert_8(self):
    #     """ Calc Convert UAH to USD: selling 0.28 UAH by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '0.28', 'out_amount': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '0.28'
    #     assert user1.resp_delegate['orig_amount'] == '0.28'
    #     assert user1.resp_delegate['out_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['28.1999', '1']
    #
    # def test_Calc_Convert_9(self):
    #     """ Calc Convert UAH to BTC: baying 0.000 01 BTC by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.00001', in_curr='UAH', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.18'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '0.00001'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '0.00001'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['17919.3156', '1']
    #
    # def test_Calc_Convert_10(self):
    #     """ Calc Convert UAH to BTC: baying 0.000 000 01 BTC by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'BTC', 'in_amount': None, 'out_amount': '0.00000001'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['orig_amount'] == '0.00000001'
    #     assert user1.resp_delegate['out_amount'] == '0.00000001'
    #     assert user1.resp_delegate['rate'] == ['17919.3156', '1']
    #
    # def test_Calc_Convert_11(self):
    #     """ Calc Convert USD to BTC: baying 0.005 BTC by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(18), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.0003), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC')
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'USD', 'out_curr': 'BTC', 'in_amount': None, 'out_amount': '0.005'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '17.91'
    #     assert user1.resp_delegate['orig_amount'] == '0.005'
    #     assert user1.resp_delegate['out_amount'] == '0.005'
    #     assert user1.resp_delegate['rate'] == ['3580.6541', '1']
    #
    # def test_Calc_Convert_12(self):
    #     """ Calc Convert BTC to USD: baying 0.01 USD by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(0.003), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.0000001),
    #                             tech_max=bl(3))
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.01', in_curr='BTC', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.0000028'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '3580.6541']
    #
    # def test_Calc_Convert_13(self):
    #     """ Calc Convert UAH to BTC: selling 0.01 UAH by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
    #                             tech_max=bl(3000))
    #     user1.merchant1.convert_calc(in_amount='0.01', out_amount=None, in_curr='UAH', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '0.01'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '0.00000055'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['17919.3156', '1']
    #
    # def test_Calc_Convert_14(self):
    #     """ Calc Convert BTC to UAH: selling 0.00000055 BTC by OWNER without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000055),
    #                             tech_max=bl(3000))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'BTC', 'out_curr': 'UAH', 'in_amount': '0.00000055', 'out_amount': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '0.00000055'
    #     assert user1.resp_delegate['orig_amount'] == '0.00000055'
    #     assert user1.resp_delegate['out_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['1', '17919.3156']
    #
    # def test_Calc_Convert_15(self):
    #     """ Calc Convert BTC to USD: selling 0.005 BTC by MERCHANT without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(0.5), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount='0.005', out_amount=None, in_curr='BTC', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.005'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '0.005'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '17.9'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '3580.6541']
    #
    # def test_Calc_Convert_16(self):
    #     """ Calc Convert UAH to USD: baying 2 USD by OWNER with common fee 0.1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(80), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=pers(0.1), in_currency='UAH', out_currency='USD')
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': None, 'out_amount': '2'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '56.46'
    #     assert user1.resp_delegate['orig_amount'] == '2'
    #     assert user1.resp_delegate['out_amount'] == '2'
    #     assert user1.resp_delegate['rate'] == ['28.2281', '1']
    #
    # def test_Calc_Convert_17(self):
    #     """ Calc Convert USD to UAH: selling 2 USD by MERCHANT with common fee 50% for exchange. """
    #     admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=pers(50), in_currency='USD', out_currency='UAH')
    #     user1.merchant1.convert_calc(in_amount='2', out_amount=None, in_curr='USD', out_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '2'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '2'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '28.19'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '14.09995']
    #
    # def test_Calc_Convert_18(self, _custom_fee, _disable_personal_exchange_fee):
    #     """ Calc Convert UAH to USD: selling 45.15 UAH by MERCHANT with personal fee 0.1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(2.3), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=pers(0.1))
    #     user1.merchant1.convert_calc(in_amount='45.15', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '45.15'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '45.15'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '1.59'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['28.2281', '1']
    #
    # def test_Calc_Convert_19(self, _custom_fee, _disable_personal_exchange_fee):
    #     """ Calc Convert UAH to RUB: baying 35 RUB by OWNER with personal fee 2% for exchange. """
    #     admin.set_wallet_amount(balance=bl(14), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'RUB', 'in_amount': None, 'out_amount': '35'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '13.4'
    #     assert user1.resp_delegate['orig_amount'] == '35'
    #     assert user1.resp_delegate['out_amount'] == '35'
    #     assert user1.resp_delegate['rate'] == ['1', '2.61326']
    #
    # def test_Calc_Convert_20(self, _custom_fee, _disable_personal_exchange_fee):
    #     """ Calc Convert UAH to USD: baying 2.40 USD by MERCHANT with common fee 3.3% for exchange
    #         and with personal fee 2.1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(70), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.3), in_currency='UAH', out_currency='USD')
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=pers(2.1))
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='2.40', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '69.11'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '2.4'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '2.4'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['28.7921', '1']
    #
    # def test_Calc_Convert_21(self, _custom_fee, _disable_personal_exchange_fee):
    #     """ Calc Convert UAH to RUB: selling 10 UAH by OWNER with common fee 3% for exchange
    #         and with personal fee 2% for exchange. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB')
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
    #     user1.delegate(params={'m_lid': str(user1.merchant1.lid), 'merch_model': 'convert', 'merch_method': 'calc',
    #                            'in_curr': 'UAH', 'out_curr': 'RUB', 'in_amount': '10', 'out_amount': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['orig_amount'] == '10'
    #     assert user1.resp_delegate['out_amount'] == '26.13'
    #     assert user1.resp_delegate['rate'] == ['1', '2.61326']
    #
    # def test_Calc_Convert_22(self, _custom_fee, _disable_personal_exchange_fee):
    #     """ Calc Convert BTC to USD: baying 4.4 USD by MERCHANT with common fee 3% for exchange
    #         and with personal fee 2% for exchange. """
    #     admin.set_wallet_amount(balance=bl(0.005), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1.5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(3), in_currency='BTC', out_currency='USD', tech_min=bl(0.0002),
    #                             tech_max=bl(3000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='4.4', in_curr='BTC', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['account_amount'] == '0'
    #     assert user1.merchant1.resp_convert_calc['in_amount'] == '0.00125391'
    #     assert user1.merchant1.resp_convert_calc['orig_amount'] == '4.4'
    #     assert user1.merchant1.resp_convert_calc['out_amount'] == '4.4'
    #     assert user1.merchant1.resp_convert_calc['rate'] == ['1', '3509.04101']
    #
    # def test_Calc_Convert_23(self, _merchant_activate):
    #     """ Calc Convert with inactive merchant. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='50', out_amount=None, in_curr='UAH', out_curr='USD')
    #     assert user1.merchant1.resp_convert_calc == {'code': -32010, 'message': 'InvalidMerchant',
    #                                                    'data': {'reason': 'Merchant Is Not Active'}}
    #
    # def test_Calc_Convert_24(self):
    #     """ Request with int's and float's in in_curr and out_curr. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=50, out_amount=None, in_curr='UAH', out_curr='USD')
    #     assert user1.merchant1.resp_convert_calc == {'code': -32070, 'message': 'InvalidParam',
    #                                                  'data': {'reason': "Key 'in_amount' must not be of 'int' type"}}
    #     user1.merchant1.convert_calc(in_amount=None, out_amount=1.5, in_curr='UAH', out_curr='USD')
    #     assert user1.merchant1.resp_convert_calc == {'code': -32070, 'message': 'InvalidParam',
    #                                                  'data': {'reason': "Key 'out_amount' must not be of 'float' type"}}
    #
    # def test_Calc_Convert_25(self):
    #     """ Exchange with in_amount wrong format. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='1.122', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmountFormat'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Invalid format 1.122 for UAH'
    #     user1.merchant1.convert_calc(in_amount='String', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmountFormat'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Invalid format String for UAH'
    #
    # def test_Calc_Convert_26(self):
    #     """ Calc Convert with out_amount wrong format. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.015', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmountFormat'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Invalid format 0.015 for USD'
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='String', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmountFormat'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Invalid format String for USD'
    #
    # def test_Calc_Convert_27(self):
    #     """ Exchange with equal pair of currency. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Unavailable exchange from UAH to UAH'
    #
    # def test_Calc_Convert_28(self):
    #     """ Exchange without pair of currencies. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr=None, out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Unavailable exchange from None to None'
    #
    # def test_Calc_Convert_29(self):
    #     """ Exchange without in_curr. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr=None, out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidInputParams'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == "'in_curr'"
    #
    # def test_Calc_Convert_30(self):
    #     """ Exchange without out_curr. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == None
    #
    # def test_Calc_Convert_31(self):
    #     """ Exchange in to not real currency. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UDS')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'UDS'
    #
    # def test_Calc_Convert_32(self):
    #     """ Exchange from not real currency. """
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='0.2', in_curr='UHA', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'UHA'
    #
    # def test_Calc_Convert_33(self):
    #     """ Exchange in to not active currency."""
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='10', out_amount=None, in_curr='UAH', out_curr='ETH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Unavailable exchange for UAH to ETH'
    #
    # def test_Calc_Convert_34(self):
    #     """ Exchange from not active currency. """
    #     admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Unavailable exchange for ETH to UAH'
    #
    # def test_Calc_Convert_35(self):
    #     """ Exchange with not active exchange pair. """
    #     admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='LTC')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Unavailable exchange for ETH to LTC'
    #
    # def test_Calc_Convert_36(self):
    #     """ Exchange WITH in_amount and out_amount. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount='1', out_amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmount'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == \
    #            "Must be provided one amount: 'in_amount' or 'out_amount'"
    #
    # def test_Calc_Convert_37(self):
    #     """ Exchange WITHOUT in_amount and out_amount. """
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     user1.merchant1.convert_calc(in_amount=None, out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InvalidAmount'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == \
    #            "Must be provided one amount: 'in_amount' or 'out_amount'"
    #
    # def test_Calc_Convert_38(self):
    #     """ Exchange UAH to USD: baying 1 USD, in_amount with fee less than user has in his balance. """
    #     admin.set_wallet_amount(balance=bl(31.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), in_currency='UAH', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InsufficientFunds'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Balance 31.01 less then amount 31.02 in UAH'
    #
    # def test_Calc_Convert_39(self):
    #     """ Exchange UAH to USD: selling 50.01 UAH, in_amount less than user has in his balance. """
    #     admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount='50.01', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'InsufficientFunds'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == 'Balance 50 less then amount 50.01 in UAH'
    #
    # def test_Calc_Convert_40(self):
    #     """ Exchange UAH to USD: selling 31.02 UAH with in_amount less than admin_min in exchange table
    #         Exchange UAH to USD: selling 93.06 UAH with in_amount more than admin_max in exchange table.
    #         Exchange UAH to USD: baying 1 USD with in_amount less than admin_min in exchange table.
    #         Exchange UAH to USD: baying 3 USD with in_amount more than admin_max in exchange table. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), tech_min=bl(31.03), tech_max=bl(93.05),
    #                             in_currency='UAH', out_currency='USD')
    #     user1.merchant1.convert_calc(in_amount='31.02', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'AmountTooSmall'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == '31.02'
    #     user1.merchant1.convert_calc(in_amount='93.06', out_amount=None, in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'AmountTooBig'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == '93.06'
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'AmountTooSmall'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == '31.02'
    #     user1.merchant1.convert_calc(in_amount=None, out_amount='3', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_convert_calc)
    #     assert user1.merchant1.resp_convert_calc['message'] == 'AmountTooBig'
    #     assert user1.merchant1.resp_convert_calc['data']['reason'] == '93.06'
    #
    # def test_Calc_Convert_41(self):
    #     """ Exchange with wrong sign. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '10', 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': 'WRONG SIGN',
    #                                'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['message'] == 'InvalidSign'
    #     assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'
    #
    # def test_Calc_Convert_42(self):
    #     """ Exchange without sign = None. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': None,
    #                                'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == "Add x-signature to headers"
    #
    # def test_Calc_Convert_43(self):
    #     """ Exchange without SIGN in headers. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == 'Add x-signature to headers'
    #
    # def test_Calc_Convert_44(self):
    #     """ Exchange with wrong merchant id. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': '105',
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == "InvalidMerchant"
    #     assert loads(r.text)['error']['data']['reason'] == "Merchant Is Not Active"
    #
    # def test_Calc_Convert_45(self):
    #     """ Exchange with None merchant id. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': 1, 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': None,
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == 'Add x-merchant to headers'
    #
    # def test_Calc_Convert_46(self):
    #     """ Exchange without merchant id in headers. """
    #     admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
    #     data = {'method': 'convert.calc',
    #             'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
    #                        'externalid': '123'},
    #             'jsonrpc': 2.0, 'id': '123456'}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == 'Add x-merchant to headers'

    def test_Calc_Convert_47(self):
        """ Exchange without IN_CURR parameter. """
        data = {'method': 'convert.calc',
                'params': {'out_curr': 'USD', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        assert loads(r.text)['error']['data']['reason'] == "method 'convert.calc' missing 1 argument: 'in_curr'"

    def test_Calc_Convert_48(self):
        """ Exchange without OUT_CURR parameter. """
        data = {'method': 'convert.calc',
                'params': {'in_curr': 'UAH', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        assert loads(r.text)['error']['data']['reason'] == "method 'convert.calc' missing 1 argument: 'out_curr'"

    def test_Calc_Convert_49(self):
        """ Exchange without IN_AMOUNT and OUT_AMOUNT. """
        data = {'method': 'convert.calc',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['message'] == 'InvalidAmount'
        assert loads(r.text)['error']['data']['reason'] == "Must be provided one amount: 'in_amount' or 'out_amount'"

    def test_Calc_Convert_50(self):
        """ Exchange with excess parameter in params field. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.calc',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None, 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        assert loads(r.text)['error']['data']['reason'] == "method 'convert.calc' received a redundant argument 'par'"
