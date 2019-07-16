import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

class TestPayout:
    """ Output """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    # def test_payout_1(self): # Перевод суммы равной сумме на счету списания
    #                          # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     # print('lid', user1.merchant1.lid)
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['reqdata']['amount'] == '0.01'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_payout_2(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     # print('lid', user1.merchant1.lid)
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['reqdata']['amount'] == '0.01'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # @pytest.mark.skip
    # def test_payout_3(self): # Перевод суммы равной сумме на счету списания
    #     """ Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     pprint.pprint(user1.merchant1.resp_payout_create)
    #     time.sleep(2)
    #     assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='RUB') == '0'
    #
    # def test_payout_4(self): # Вывод суммы равной техническому максимуму по таблице pwcurrency
    #     """ Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='BTC',
    #                   payway=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='BTC',
    #                   payway=admin.payway['btc']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.99999))
    #     user1.merchant1.payout_create(payway='btc', amount='0.99999', out_curr='BTC', payee='32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='BTC') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.00463))
    #
    # def test_payout_5(self):
    #     """ Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
    #     admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'privat24', 'amount': '10', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '11.5'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.5'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.5'
    #     assert user1.resp_delegate['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['privat24']['id'], is_active=False)
    #
    # def test_payout_6(self):
    #     """ Payout to ltc 0.5 LTC: LTC to LTC by MERCHANT with common absolute fee 0.001 LTC for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='LTC',
    #                   payway=admin.payway['ltc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=10, currency='LTC',
    #                   payway=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=True,
    #                                  tech_min=bl(0.002), tech_max=bl(0.6))
    #     user1.merchant1.payout_create(payway='ltc', amount='0.5', out_curr='LTC',
    #                                   payee='M93SfGQPnNp3dEdPJx1GrizvNWUFA1hSVi')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '0.5'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '0.5'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0.001'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '0.501'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0.001'
    #     # assert user1.merchant1.balance(curr='LTC') == '0.499'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=False,
    #                                  tech_min=bl(0.002), tech_max=bl(0.01349))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='LTC',
    #                   payway=admin.payway['ltc']['id'], is_active=False)
    #
    # @pytest.mark.skip
    # def test_payout_7(self):
    #     """ Payout to qiwi 10 RUB: RUB to RUB by OWNER with common percent fee 5.5% for payout
    #      and common absolute fee 1 RUB for payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['qiwi']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'qiwi', 'amount': '10', 'out_curr': 'RUB',
    #                            'm_lid': user1.merchant1.lid, 'payee': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='RUB') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['qiwi']['id'], is_active=False)
    #
    # def test_payout_8(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Payout to perfect 10 USD: USD to USD by MERCHANT with personal percent fee 5.5% for transfer
    #     and with personal absolute fee 1 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['perfect']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['perfect']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(15))
    #     user1.merchant1.payout_create(payway='perfect', amount='10', out_curr='USD', payee='U6768929')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '10'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '10'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '1.55'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '11.55'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '1.55'
    #     assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(2.24))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['perfect']['id'], is_active=False)
    #
    # def test_payout_9(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(15))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(1))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_payout_10(self):
    #     """ Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '18.76'
    #     assert user1.resp_delegate['in_amount'] == '18.76'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '50'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['1', '2.6666']
    #     assert user1.resp_delegate['reqdata']['amount'] == '50'
    #     assert user1.merchant1.balance(curr='UAH') == '1.24'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_payout_11(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '8.33'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.637', '1']
    #     assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '8.33'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_payout_12(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(17.82))
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '431.46'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '15'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '72.78'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '504.24'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '2.53'
    #     assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.7639', '1']
    #     assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '15'
    #     assert user1.merchant1.balance(curr='UAH') == '0.76'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=False)


class TestWrongPayout:
    """ Wrong payout. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    # def test_wrong_payout_1(self, _disable_st_value):# Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'UnavailableOutPay'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_2(self, _disable_st_value):# Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailableOutPay'
    #
    # def test_wrong_payout_3(self, _enable_merchant_payout_allowed):# Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'UnavailableOutPay'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_4(self, _enable_merchant_payout_allowed):# Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailableOutPay'
    #
    # def test_wrong_payout_5(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.02', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InsufficientFunds'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_6(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='3.02', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InsufficientFunds'
    #
    # def test_wrong_payout_7(self):# Вывод суммы не существующим мерчантом
    #     """ Payout by non-existing merchant
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': '1234567890', 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidMerchant'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_8(self, _enable_merchant_is_active):# Вывод суммы не активным мерчантом
    #     """ Payout by an active merchant
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': '1234567890', 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidMerchant'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_9(self):# Вывод без суммы (amount = None)
    #     """ amount = None  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': None, 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidAmountFormat'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_10(self):# Вывод без суммы (amount = None)
    #     """ amount = None  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount=None, out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidAmountFormat'
    #
    # def test_wrong_payout_11(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidInputParams'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_12(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'in_curr': None, 'out_curr': 'RUB', 'payway': 'payeer', 'externalid': ex_id,
    #                        'payee': 'P1007817628', 'contact': None, 'region': None, 'payer': None},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #
    # def test_wrong_payout_13(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': 'Test', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidAmountFormat'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_14(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='Test', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidAmountFormat'
    #
    # def test_wrong_payout_15(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.111', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidAmountFormat'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_16(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='0.111', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidAmountFormat'
    #
    # def test_wrong_payout_17(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'TST',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['message']== 'InvalidCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_18(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='TST', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidCurrency'
    #
    # def test_wrong_payout_19(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['message']== 'InactiveCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_20(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InactiveCurrency'
    #
    # def test_wrong_payout_21(self):# Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'TST',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message']== 'InvalidCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_22(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):# Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='TST', payee='Z123456789012')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_23(self, _enable_currency):# Вывод неактивной валюты in_curr
    #     """ Payout inactive currency in_curr delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     assert user1.resp_delegate['message']== 'InactiveCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_24(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):# Вывод неактивной валюты in_curr
    #     """ Payout inactive currency in_curr payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(17.82))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InactiveCurrency'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_wrong_payout_25(self, _enable_currency):# Вывод отключенной валюты out_curr
    #     """ Currency out_curr off delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['message']== 'InactiveCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_26(self, _enable_currency):# Вывод отключенной валюты out_curr
    #     """ Currency out_curr off payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InactiveCurrency'
    #
    # def test_wrong_payout_27(self, _enable_currency):# Вывод отключенной валюты in_curr
    #     """ Currency in_curr off delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     assert user1.resp_delegate['message']== 'InactiveCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_28(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):# Вывод отключенной валюты in_curr
    #     """ Currency in_curr off payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(17.82))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InactiveCurrency'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_wrong_payout_29(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
    #     """ Amount payout below the technical minimum in the pwcurrency table delegate
    #     Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.02), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message'] == 'AmountTooSmall'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_30(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
    #     """ Amount payout below the technical minimum in the pwcurrency table payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(2), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'AmountTooSmall'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #
    # def test_wrong_payout_31(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Payout of the amount equal to the technical minimum in the pwcurrency table payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1.02), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='RUB') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #
    # def test_wrong_payout_32(self): # Вывод суммы выше технического максимума по таблице pwcurrency
    #     """ Payout above technical maximum in pwcurrency table payout_create
    #     Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='BTC',
    #                   payway=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='BTC',
    #                   payway=admin.payway['btc']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.00463))
    #     user1.merchant1.payout_create(payway='btc', amount='0.99999', out_curr='BTC', payee='32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'AmountTooBig'
    #
    # def test_wrong_payout_33(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы выше технического максимума по таблице pwcurrency
    #     Payout above technical maximum in pwcurrency table delegate
    #     Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(1))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     assert user1.resp_delegate['message'] == 'AmountTooBig'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_wrong_payout_34(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы равной техническому максимуму по таблице pwcurrency
    #     Payout of the amount equal to the technical minimum in the pwcurrency table delegate
    #     Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(1))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_wrong_payout_35(self): # Вывод суммы ниже технического минимума по таблице exchange
    #     """ Amount payout below the technical minimum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(20), tech_max=bl(40650.07))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     assert user1.resp_delegate['message'] == 'AmountTooSmall'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.01), tech_max=bl(40650.07))
    #
    # def test_wrong_payout_36(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы ниже технического минимума по таблице exchange
    #     Amount payout below the technical minimum in the exchange table payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(250), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'AmountTooSmall'
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_37(self): # Вывод суммы равной техническому минимуму по таблице exchange
    #     """ Payout of the amount equal to the technical minimum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(18.76), tech_max=bl(40650.07))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '18.76'
    #     assert user1.resp_delegate['in_amount'] == '18.76'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '50'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['1', '2.6666']
    #     assert user1.resp_delegate['reqdata']['amount'] == '50'
    #     assert user1.merchant1.balance(curr='UAH') == '1.24'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.01), tech_max=bl(40650.07))
    #
    # def test_wrong_payout_38(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы равной техническому минимуму по таблице exchange
    #     Payout of the amount equal to the technical minimum in the exchange table payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(238.55), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z735396623255')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '8.33'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.637', '1']
    #     assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '8.33'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_wrong_payout_39(self): # Вывод суммы выше технического максимума по таблице exchange
    #     """ Amount payout above the technical maximum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.01), tech_max=bl(15))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     assert user1.resp_delegate['message'] == 'AmountTooBig'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.01), tech_max=bl(40650.07))
    #
    # def test_wrong_payout_40(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы выше технического максимума по таблице exchange
    #     Amount payout above the technical maximum in the exchange table payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(200))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'AmountTooBig'
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_41(self): # Вывод суммы равной техническому максимуму по таблице exchange
    #     """ Payout of the amount equal to the technical maximum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(18.76))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '18.76'
    #     assert user1.resp_delegate['in_amount'] == '18.76'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '50'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['1', '2.6666']
    #     assert user1.resp_delegate['reqdata']['amount'] == '50'
    #     assert user1.merchant1.balance(curr='UAH') == '1.24'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_wrong_payout_42(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы равной техническому максимуму по таблице exchange
    #     Payout of the amount equal to the technical maximum in the exchange table payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(431.46))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(17.82))
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '431.46'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '15'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '72.78'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '504.24'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '2.53'
    #     assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.7639', '1']
    #     assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '15'
    #     assert user1.merchant1.balance(curr='UAH') == '0.76'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['exmo']['id'], is_active=False)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_wrong_payout_43(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Payout with the amount parameter, the value of which is less than the out_curr currency grain delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.009', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_44(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Payout with the amount parameter, the value of which is less than the out_curr currency grain payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='0.009', out_curr='RUB', payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidAmountFormat'
    #
    # def test_wrong_payout_45(self): # Запрос без out_curr (не передан)
    #     """ Request without out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_46(self): # Запрос без out_curr (не передан)
    #     """ Request without out_curr payout.create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #
    # def test_wrong_payout_47(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': None,
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message']== 'InvalidCurrency'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_48(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr=None, payee='P1007817628')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidCurrency'
    #
    # def test_wrong_payout_49(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '4731185613244273', 'par': '123'})
    #     assert user1.resp_delegate['message']== 'InvalidInputParams'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_50(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'UAH', 'par': '123'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #
    # def test_wrong_payout_51(self): # Запрос без externalid
    #     """ Request without externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     assert user1.resp_delegate['message']== 'InvalidInputParams'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_52(self): # Запрос без externalid
    #     """ Request without externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'payee': 'P14812343', 'out_curr': 'UAH'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #
    # def test_wrong_payout_53(self): # Запрос с существующим externalid
    #     """ Request with existing externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     tmp_ex_id = user1.ex_id()
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message']== 'Unique'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_54(self): # Запрос с существующим externalid
    #     """ Request with existing externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343', 'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'Unique'

    # def test_wrong_payout_55(self): # Запрос без подписи
    #     """ Unsigned request
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343', 'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #
    # def test_wrong_payout_56(self): # Запрос с невалидной подписью
    #     """ Request with invalid sign
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343', 'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     assert loads(r.text)['error']['message'] == 'InvalidSign'

    # def test_wrong_payout_57(self, _enable_exchange_operation_UAH_RUB):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ inactive exchange direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'contact': 'R378259361317'})
    #     assert user1.resp_delegate['message'] == 'UnavailExchange'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_58(self): # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: USD to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='USD', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'USD',
    #                            'm_lid': user1.merchant1.lid, 'contact': 'R378259361317'})
    #     assert user1.resp_delegate['message'] == 'UnavailExchange'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(39.99))

    # def test_wrong_payout_59(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_exchange_operation_UAH_USD):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailExchange'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_60(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to webmoney 8.33 USD: BCHABC to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='BCHABC', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['BCHABC'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='BCHABC', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailExchange'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
    #                   payway=admin.payway['webmoney']['id'], is_active=False)

    # def test_wrong_payout_61(self): # указана неверная платежная система
    #     """ invalid payment system specified
    #     Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
    #                   payway=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'test', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': user1.merchant1.lid, 'payee': '5363542305527674'})
    #     assert user1.resp_delegate['message'] == 'InvalidPayway'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_62(self): # указана неверная платежная система
    #     """ invalid payment system specified
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
    #                   payway=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='test', amount='1.02', out_curr='RUB', payee='P14812343')
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'

    def test_wrong_payout_63(self, _activate_kuna): # указана неактивная платежная система (is_active=False)
        """ inactive payment system specified (is_active = False)
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        admin.set_payways(name='kuna', is_active=False)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
        assert user1.resp_delegate['message'] == 'InvalidPayway'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_64(self, _activate_payeer): # указана неактивная платежная система (is_active=False)
        """ inactive payment system specified (is_active = False)
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        admin.set_payways(name='payeer', is_active=False)
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'

    def test_wrong_payout_65(self, _activate_kuna): # указана отключенная платежная система (is_disabled=True)
        """ disabled payment system specified (is_disabled=True)
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        admin.set_payways(name='kuna', is_disabled=True)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid, 'payee': '4731185613244273'})
        assert user1.resp_delegate['message'] == 'InvalidPayway'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_66(self, _activate_payeer): # указана отключенная платежная система (is_disabled=True)
        """ disabled payment system specified (is_disabled=True)
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        admin.set_payways(name='payeer', is_disabled=True)
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'

    @pytest.mark.skip
    def test_wrong_payout_67(self): # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='TEST')
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidField'

    @pytest.mark.skip
    def test_wrong_payout_68(self): # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
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
                               'm_lid': user1.merchant1.lid, 'payee': 'TEST'})
        assert user1.resp_delegate['message'] == 'InvalidField'

    def test_wrong_payout_69(self): # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'privat24', 'amount': '10', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid})
        assert user1.resp_delegate['message'] == 'InvalidField'

    @pytest.mark.skip
    def test_wrong_payout_70(self, _activate_payeer): # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=True,
                                     tech_min=bl(1), tech_max=bl(15))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
                               'm_lid': user1.merchant1.lid, 'contact': 'TEST'})
        assert user1.resp_delegate['message'] == 'InvalidField'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=False,
                                     tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=False)

    @pytest.mark.skip
    def test_wrong_payout_71(self, _activate_payeer): # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=True,
                                     tech_min=bl(1), tech_max=bl(15))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD', 'm_lid': user1.merchant1.lid})
        pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidField'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD', is_active=False,
                                     tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='USD',
                      payway=admin.payway['cash_kiev']['id'], is_active=False)



class TestParams:
    """ Testing payout params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_params_1(self):
        """ Getting params for payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['in_curr_balance'] == '0.01'
        assert user1.resp_delegate['is_convert'] == False
        assert user1.resp_delegate['max'] == '98'
        assert user1.resp_delegate['max_by_balance'] == '0.01'
        assert user1.resp_delegate['min'] == '0.01'
        assert user1.resp_delegate['min_balance_limit'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['out_fee'] == None
        assert user1.resp_delegate['payway'] == 'visamc'
        assert user1.resp_delegate['pwtp'] == 'sci'
        assert user1.resp_delegate['rate'] == ['1', '1']
        assert user1.resp_delegate['uaccount'] == None
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_params_2(self):
        """ Getting params for payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='UAH',
                      payway=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'kuna', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['in_curr_balance'] == '0.01'
        assert user1.resp_delegate['is_convert'] == False
        assert user1.resp_delegate['max'] == '98'
        assert user1.resp_delegate['max_by_balance'] == '0.01'
        assert user1.resp_delegate['min'] == '0.01'
        assert user1.resp_delegate['min_balance_limit'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['out_fee'] == None
        assert user1.resp_delegate['payway'] == 'kuna'
        assert user1.resp_delegate['pwtp'] == 'cheque'
        assert user1.resp_delegate['rate'] == ['1', '1']
        assert user1.resp_delegate['uaccount'] == None
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_params_3(self):
        """ Getting params for payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency='RUB',
                      payway=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
        pprint.pprint(user1.merchant1.resp_payout_params)
        assert user1.merchant1.resp_payout_params['in_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_params['in_curr_balance'] == '1.02'
        assert user1.merchant1.resp_payout_params['is_convert'] == False
        assert user1.merchant1.resp_payout_params['max'] == '3.36'
        assert user1.merchant1.resp_payout_params['max_by_balance'] == '1.02'
        assert user1.merchant1.resp_payout_params['min'] == '1'
        assert user1.merchant1.resp_payout_params['min_balance_limit'] == '1'
        assert user1.merchant1.resp_payout_params['out_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_params['out_fee'] == None
        assert user1.merchant1.resp_payout_params['payway'] == 'payeer'
        assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
        assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
        assert user1.merchant1.resp_payout_params['uaccount'] == None
