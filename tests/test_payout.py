import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import pprint


@pytest.mark.usefixtures('_payout_fee', '_personal_exchange_fee')
class TestPayout:
    """ Output """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_payout_1(self): # Вывод суммы равной сумме на счету списания
                             # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        # print('lid', user1.merchant1.lid)
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_payout_2(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
        # print('lid', user1.merchant1.lid)
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    @pytest.mark.skip
    def test_payout_3(self): # Перевод суммы равной сумме на счету списания
        """ Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # time.sleep(2)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '1.02'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '1.02'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '1.02'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='RUB') == '0'

    def test_payout_4(self): # Вывод суммы равной техническому максимуму по таблице pwcurrency
        """ Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
                                     tech_min=bl(0.001), tech_max=bl(0.99999))
        user1.merchant1.payout_create(payway='btc', amount='0.99999', out_curr='BTC', payee='32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '0.99999'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '0.99999'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '0.99999'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='BTC') == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
                                     tech_min=bl(0.001), tech_max=bl(0.00463))

    def test_payout_5(self):
        """ Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'privat24', 'amount': '10', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '11.5'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.5'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_fee_amount'] == '1.5'
        assert user1.resp_delegate['reqdata']['amount'] == '10'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=False,
                                     tech_min=bl(1), tech_max=bl(10))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=False)

    def test_payout_6(self):
        """ Payout to ltc 0.5 LTC: LTC to LTC by MERCHANT with common absolute fee 0.001 LTC for payout. """
        admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
                      payway_id=admin.payway['ltc']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
                      payway_id=admin.payway['ltc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=True,
                                     tech_min=bl(0.002), tech_max=bl(0.6))
        user1.merchant1.payout_create(payway='ltc', amount='0.5', out_curr='LTC',
                                      payee='M93SfGQPnNp3dEdPJx1GrizvNWUFA1hSVi')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '0.5'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '0.5'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0.001'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '0.501'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0.001'
        # assert user1.merchant1.balance(curr='LTC') == '0.499'
        admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=False,
                                     tech_min=bl(0.002), tech_max=bl(0.01349))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
                      payway_id=admin.payway['ltc']['id'], is_active=False)

    @pytest.mark.skip
    def test_payout_7(self):
        """ Payout to qiwi 10 RUB: RUB to RUB by OWNER with common percent fee 5.5% for payout
         and common absolute fee 1 RUB for payout."""
        admin.set_wallet_amount(balance=bl(15), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['qiwi']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'qiwi', 'amount': '10', 'out_curr': 'RUB',
                               'm_lid': str(user1.merchant1.lid), 'payee': '380965781066'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '11.55'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['reqdata']['amount'] == '10'
        assert user1.merchant1.balance(curr='RUB') == '3.45'
        admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=False,
                                     tech_min=bl(1), tech_max=bl(10))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['qiwi']['id'], is_active=False)

    def test_payout_8(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Payout to perfect 10 USD: USD to USD by MERCHANT with personal percent fee 5.5% for transfer
        and with personal absolute fee 1 USD  payout. """
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['perfect']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(15))
        user1.merchant1.payout_create(payway='perfect', amount='10', out_curr='USD', payee='U6768929')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '10'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '10'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '11.55'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '1.55'
        assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '10'
        assert user1.merchant1.balance(curr='USD') == '3.45'
        admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(2.24))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['perfect']['id'], is_active=False)

    def test_payout_9(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(1), tech_max=bl(15))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
                               'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '11.55'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        assert user1.resp_delegate['reqdata']['amount'] == '10'
        assert user1.merchant1.balance(curr='USD') == '3.45'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['cash_kiev']['id'], is_active=False)

    def test_payout_10(self):
        """ Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '18.76'
        assert user1.resp_delegate['in_amount'] == '18.76'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '50'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['rate'] == ['1', '2.6666']
        assert user1.resp_delegate['reqdata']['amount'] == '50'
        assert user1.merchant1.balance(curr='UAH') == '1.24'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))

    def test_payout_11(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
                                      in_curr='UAH', payee='Z123456789012')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '238.55'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '8.33'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '238.55'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.637', '1']
        assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '8.33'
        assert user1.merchant1.balance(curr='UAH') == '11.45'
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_payout_12(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 4% for exchange and with personal fee 2% for exchange
        with common percent fee 5% for payout and with common absolute fee 5 USD for payout
        with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
        admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
        admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
        user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        assert user1.merchant1.resp_payout_create['result']['in_amount'] == '431.46'
        assert user1.merchant1.resp_payout_create['result']['out_amount'] == '15'
        assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '72.78'
        assert user1.merchant1.resp_payout_create['result']['account_amount'] == '504.24'
        assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '2.53'
        assert user1.merchant1.resp_payout_create['result']['rate'] == ['28.7639', '1']
        assert user1.merchant1.resp_payout_create['result']['reqdata']['amount'] == '15'
        assert user1.merchant1.balance(curr='UAH') == '0.76'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['exmo']['id'], is_active=False)


@pytest.mark.usefixtures('_payout_fee', '_personal_exchange_fee')
class TestWrongPayout:
    """ Wrong payout. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    # def test_wrong_payout_1(self, _disable_st_value):# Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32036
    #     assert user1.resp_delegate['message'] == 'EStateOutPayUnavailable'
    #     assert user1.resp_delegate['data']['reason'] == 'Out pay is blocked'
    #
    # def test_wrong_payout_2(self, _disable_st_value):# Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32036
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateOutPayUnavailable'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Out pay is blocked'
    #
    # def test_wrong_payout_3(self, _enable_merchant_payout_allowed):
    #     # Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32036
    #     assert user1.resp_delegate['message'] == 'EStateOutPayUnavailable'
    #     assert user1.resp_delegate['data']['reason'] == 'Out pay is blocked'
    #
    # def test_wrong_payout_4(self, _enable_merchant_payout_allowed):# Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32036
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateOutPayUnavailable'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Out pay is blocked'
    #
    # def test_wrong_payout_5(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.02', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32056
    #     assert user1.resp_delegate['message'] == 'EStateInsufficientFunds'
    #     assert user1.resp_delegate['data']['reason'] == 'Balance 0.01 less then amount 0.02'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_6(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='3.02', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32056
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateInsufficientFunds'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Balance 1.02 less then amount 3.02'
    #
    # def test_wrong_payout_7(self):# Вывод суммы не существующим мерчантом
    #     """ Payout by non-existing merchant
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': '1234567890', 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32090
    #     assert user1.resp_delegate['message'] == 'EParamNotFound'
    #     assert user1.resp_delegate['data']['field'] == 'm_lid'
    #     assert user1.resp_delegate['data']['reason'] == 'Not found'
    #
    # def test_wrong_payout_8(self, _enable_merchant_is_active):# Вывод суммы не активным мерчантом
    #     """ Payout by an active merchant
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'm_lid'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #
    # def test_wrong_payout_9(self):# Вывод без суммы (amount = None)
    #     """ amount = None  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': None, 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_10(self):# Вывод без суммы (amount = None)
    #     """ amount = None  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     user1.merchant1.payout_create(payway='payeer', amount=None, out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_11(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_12(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
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
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['data']['field'] == 'amount'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should be provided'
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #
    # def test_wrong_payout_13(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': 'Test', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be a Number'
    #
    # def test_wrong_payout_14(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     user1.merchant1.payout_create(payway='payeer', amount='Test', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Should be a Number'
    #
    # def test_wrong_payout_15(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.111', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #
    # def test_wrong_payout_16(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     user1.merchant1.payout_create(payway='payeer', amount='0.111', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32082
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #
    # def test_wrong_payout_17(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'TST',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #
    # def test_wrong_payout_18(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='TST', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32014
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Invalid currency name'
    #
    # def test_wrong_payout_19(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_20(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_21(self):# Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'TST',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #
    # def test_wrong_payout_22(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     # Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='TST', payee='Z123456789012')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32014
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Invalid currency name'
    #
    # def test_wrong_payout_23(self, _enable_currency, _activate_merchant_payways):# Вывод неактивной валюты in_curr
    #     """ Payout inactive currency in_curr delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_24(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency,
    #                          _activate_merchant_payways):
    #     # Вывод неактивной валюты in_curr
    #     """ Payout inactive currency in_curr payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_25(self, _enable_currency, _activate_merchant_payways):# Вывод отключенной валюты out_curr
    #     """ Currency out_curr off delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_26(self, _enable_currency, _activate_merchant_payways):# Вывод отключенной валюты out_curr
    #     """ Currency out_curr off payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P1007817628')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_27(self, _enable_currency, _activate_merchant_payways):# Вывод отключенной валюты in_curr
    #     """ Currency in_curr off delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_28(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency,
    #                          _activate_merchant_payways):
    #     # Вывод отключенной валюты in_curr
    #     """ Currency in_curr off payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_29(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
    #     """ Amount payout below the technical minimum in the pwcurrency table delegate
    #     Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.02), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32074
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_30(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
    #     """ Amount payout below the technical minimum in the pwcurrency table payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(2), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32074
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Amount is too small'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #
    # def test_wrong_payout_31(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Payout of the amount equal to the technical minimum in the pwcurrency table payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1.02), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     assert user1.merchant1.resp_payout_create['result']['in_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_create['result']['account_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='RUB') == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #
    # def test_wrong_payout_32(self): # Вывод суммы выше технического максимума по таблице pwcurrency
    #     """ Payout above technical maximum in pwcurrency table payout_create
    #     Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.00463))
    #     user1.merchant1.payout_create(payway='btc', amount='0.99999', out_curr='BTC',
    #                                   payee='32LdQGCG1PHYNP2sRkZgrP6UAfQYTSkshx')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32073
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountTooBig'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Amount is too big'
    #
    # def test_wrong_payout_33(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы выше технического максимума по таблице pwcurrency
    #     Payout above technical maximum in pwcurrency table delegate
    #     Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(1))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32073
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_wrong_payout_34(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Вывод суммы равной техническому максимуму по таблице pwcurrency
    #     Payout of the amount equal to the technical minimum in the pwcurrency table delegate
    #     Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(10))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     # assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['reqdata']['amount'] == '10'
    #     assert user1.merchant1.balance(curr='USD') == '3.45'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(1))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_wrong_payout_35(self):  # Вывод суммы ниже технического минимума по таблице exchange
    #     """ Amount payout below the technical minimum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(20), tech_max=bl(40650.07))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32074
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
    #     assert user1.resp_delegate['data']['field'] == 'in_amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
    #     assert user1.resp_delegate['data']['value'] == '18.76'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # print(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32074
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'in_amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Amount is too small'
    #     assert user1.merchant1.resp_payout_create['error']['data']['value'] == '238.55'
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_37(self): # Вывод суммы равной техническому минимуму по таблице exchange
    #     """ Payout of the amount equal to the technical minimum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(18.76), tech_max=bl(40650.07))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
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
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
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
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32073
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
    #     assert user1.resp_delegate['data']['field'] == 'in_amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
    #     assert user1.resp_delegate['data']['value'] == '18.76'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32073
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountTooBig'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'in_amount'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Amount is too big'
    #     assert user1.merchant1.resp_payout_create['error']['data']['value'] == '238.55'
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_41(self): # Вывод суммы равной техническому максимуму по таблице exchange
    #     """ Payout of the amount equal to the technical maximum in the exchange table delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(18.76))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
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
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
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
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['exmo']['id'], is_active=False)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_wrong_payout_43(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Payout with the amount parameter, the value of which is less than the out_curr currency grain delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.009', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_44(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Payout with the amount parameter, the value of which is less than the out_curr currency grain payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='0.009', out_curr='RUB', payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32082
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'amount'
    #
    # def test_wrong_payout_45(self): # Запрос без out_curr (не передан)
    #     """ Request without out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'm_lid': str(user1.merchant1.lid),
    #                            'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_46(self): # Запрос без out_curr (не передан)
    #     """ Request without out_curr payout.create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'out_curr'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_47(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': None,
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_48(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr=None, payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_49(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273', 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'par'
    #     assert user1.resp_delegate['data']['reason'] == 'Should not be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_50(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'par'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should not be provided'
    #
    # def test_wrong_payout_51(self): # Запрос без externalid
    #     """ Request without externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'externalid'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_52(self): # Запрос без externalid
    #     """ Request without externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'externalid'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_53(self): # Запрос с существующим externalid
    #     """ Request with existing externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     tmp_ex_id = user1.ex_id()
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32091
    #     assert user1.resp_delegate['message'] == 'EParamUnique'
    #     assert user1.resp_delegate['data']['field'] == 'externalid'
    #     assert user1.resp_delegate['data']['reason'] == 'Such externalid already present'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_54(self): # Запрос с существующим externalid
    #     """ Request with existing externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32091
    #     assert loads(r.text)['error']['message'] == 'EParamUnique'
    #     assert loads(r.text)['error']['data']['field'] == 'externalid'
    #     assert loads(r.text)['error']['data']['reason'] == 'Such externalid already present'
    #
    # def test_wrong_payout_55(self): # Запрос без подписи
    #     """ Unsigned request
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32012
    #     assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'x-signature'
    #     assert loads(r.text)['error']['data']['reason'] == 'Not present'
    #
    # def test_wrong_payout_56(self): # Запрос с невалидной подписью
    #     """ Request with invalid sign
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['code'] == -32010
    #     assert loads(r.text)['error']['message'] == 'EParamSignInvalid'
    #     assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'
    #
    # def test_wrong_payout_57(self, _enable_exchange_operation_UAH_RUB):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ inactive exchange direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': 'R378259361317'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32084
    #     assert user1.resp_delegate['message'] == 'EStateExchangeUnavail'
    #     assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange from UAH to RUB'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_58(self): # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: USD to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='USD', out_currency='RUB', is_active=False)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'USD',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': 'R378259361317'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32084
    #     assert user1.resp_delegate['message'] == 'EStateExchangeUnavail'
    #     assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange from USD to RUB'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='USD', out_currency='RUB')
    #
    # def test_wrong_payout_59(self, _custom_fee, _disable_personal_operation_fee_transfer_USD,
    #                          _enable_exchange_operation_UAH_USD):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32084
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateExchangeUnavail'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Unavailable exchange from UAH to USD'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='BCHABC', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['code'] == -32084
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'EStateExchangeUnavail'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == \
    #            'Unavailable exchange from BCHABC to USD'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_wrong_payout_61(self): # указана неверная платежная система
        """ invalid payment system specified
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'test', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32081
        assert user1.resp_delegate['message'] == 'EParamPaywayInvalid'
        assert user1.resp_delegate['data']['field'] == 'payway'
        assert user1.resp_delegate['data']['reason'] == 'Invalid payway name'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_62(self): # указана неверная платежная система
        """ invalid payment system specified
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='test', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        assert user1.merchant1.resp_payout_create['error']['code'] == -32081
        assert user1.merchant1.resp_payout_create['error']['message'] == 'EParamPaywayInvalid'
        assert user1.merchant1.resp_payout_create['error']['data']['field'] == 'payway'
        assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Invalid payway name'

    def test_wrong_payout_63(self, _activate_kuna): # указана неактивная платежная система (is_active=False)
        """ inactive payment system specified (is_active = False)
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        admin.set_payways(name='kuna', is_active=False)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidPayway'
        assert user1.resp_delegate['data']['reason'] == 'kuna is inactive'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_64(self, _activate_payeer): # указана неактивная платежная система (is_active=False)
        """ inactive payment system specified (is_active = False)
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))
        admin.set_payways(name='payeer', is_active=False)
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'
        assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'payeer is inactive'

    def test_wrong_payout_65(self, _activate_kuna): # указана отключенная платежная система (is_disabled=True)
        """ disabled payment system specified (is_disabled=True)
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        admin.set_payways(name='kuna', is_disabled=True)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidPayway'
        assert user1.resp_delegate['data']['reason'] == 'kuna is disabled'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_66(self, _activate_payeer): # указана отключенная платежная система (is_disabled=True)
        """ disabled payment system specified (is_disabled=True)
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))
        admin.set_payways(name='payeer', is_disabled=True)
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'
        assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'payeer is disabled'

    def test_wrong_payout_67(self):
        # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='TEST')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidField'
        assert user1.merchant1.resp_payout_create['error']['data']['reason'] == \
               'Check arguments required to pass as userdata for current payway'

    def test_wrong_payout_68(self):
        # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': 'TEST'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidField'
        assert user1.resp_delegate['data']['reason'] == \
               'Check arguments required to pass as userdata for current payway'

    def test_wrong_payout_69(self):
        # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'privat24', 'amount': '10', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidField'
        assert user1.resp_delegate['data']['reason'] == \
               'Check arguments required to pass as userdata for current payway'

    def test_wrong_payout_70(self, _activate_payeer):
        # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(1), tech_max=bl(15))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
                               'm_lid': str(user1.merchant1.lid), 'contact': 'TEST'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidField'
        assert user1.resp_delegate['data']['reason'] == \
               'Check arguments required to pass as userdata for current payway'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['cash_kiev']['id'], is_active=False)

    # @pytest.mark.skip
    def test_wrong_payout_71(self, _activate_payeer):
        # отсутствие контактных данных [cash: phone либо telegram, неверный payee для карты - номер буквами]
        """ lack of contact details [cash: phone or telegram, wrong payee for the card - number by letters]
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(1), tech_max=bl(15))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'cash_kiev', 'amount': '10', 'out_curr': 'USD',
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidField'
        assert user1.resp_delegate['data']['reason'] == \
               'Check arguments required to pass as userdata for current payway'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['cash_kiev']['id'], is_active=False)


class TestParams:
    """ Testing payout params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    # def test_params_1(self):
    #     """ Getting params for payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.01'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '98'
    #     assert user1.resp_delegate['max_by_balance'] == '0.01'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.01'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] ==  {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['payway'] == 'visamc'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_2(self):
    #     """ Getting params for payout to kuna UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'kuna', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.01'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '98'
    #     assert user1.resp_delegate['max_by_balance'] == '0.01'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.01'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['payway'] == 'kuna'
    #     assert user1.resp_delegate['pwtp'] == 'cheque'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_3(self):
    #     """ Getting params for payout to payeer RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '3.36'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['min'] == '1'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '1'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == {}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'payeer'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #
    # def test_params_4(self):
    #     """ Getting params for payout to btc BTC: BTC to BTC by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
    #                   payway_id=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
    #                   payway_id=admin.payway['btc']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.99999))
    #     user1.merchant1.payout_params(payway='btc', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'BTC'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '0.99999'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '0.99999'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '0.99999'
    #     assert user1.merchant1.resp_payout_params['min'] == '0.001'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '0.001'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'BTC'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == {}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'btc'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'crypto'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #
    # def test_params_5(self):
    #     """ Getting params for payout to privat24 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
    #     admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(10), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'privat24', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '11.5'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '100'
    #     assert user1.resp_delegate['max_by_balance'] == '10'
    #     assert user1.resp_delegate['min'] == '10'
    #     assert user1.resp_delegate['min_balance_limit'] == '11.5'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.15'}
    #     assert user1.resp_delegate['payway'] == 'privat24'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=False)
    #
    # def test_params_6(self):
    #     """ Getting params for payout to LTC: LTC to LTC by MERCHANT with common absolute fee 0.001 LTC for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=True,
    #                                  tech_min=bl(0.5), tech_max=bl(0.6))
    #     user1.merchant1.payout_params(payway='ltc', out_curr='LTC')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'LTC'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '1'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '0.6'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '0.999'
    #     assert user1.merchant1.resp_payout_params['min'] == '0.5'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '0.501'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'LTC'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '0.001', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'ltc'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'crypto'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=False,
    #                                  tech_min=bl(0.002), tech_max=bl(0.01349))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=False)
    #
    # def test_params_7(self):
    #     """ Getting params for payout to RUB: RUB to RUB by OWNER with common percent fee 5.5% for payout
    #      and common absolute fee 1 RUB for payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(10), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'qiwi', 'out_curr': 'RUB',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'RUB'
    #     assert user1.resp_delegate['in_curr_balance'] == '15'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '100'
    #     assert user1.resp_delegate['max_by_balance'] == '13.27'
    #     assert user1.resp_delegate['min'] == '10'
    #     assert user1.resp_delegate['min_balance_limit'] == '11.55'
    #     assert user1.resp_delegate['out_curr'] == 'RUB'
    #     assert user1.resp_delegate['out_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.055'}
    #     assert user1.resp_delegate['payway'] == 'qiwi'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=False)
    #
    # def test_params_8(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for payout to USD: USD to USD by MERCHANT with personal percent fee 5.5% for transfer
    #     and with personal absolute fee 1 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['perfect']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(10), tech_max=bl(15))
    #     user1.merchant1.payout_params(payway='perfect', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'USD'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '15'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '15'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '13.27'
    #     assert user1.merchant1.resp_payout_params['min'] == '10'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '11.55'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.055'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'perfect'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(2.24))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['perfect']['id'], is_active=False)
    #
    # def test_params_9(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for payout to USD: USD to USD by OWNER
    #     with common percent fee 10% for payout and with common absolute fee 2 USD for payout
    #     with personal percent fee 5.5% for payout and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(10), tech_max=bl(15))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'cash_kiev', 'out_curr': 'USD',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'USD'
    #     assert user1.resp_delegate['in_curr_balance'] == '15'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '15'
    #     assert user1.resp_delegate['max_by_balance'] == '13.27'
    #     assert user1.resp_delegate['min'] == '10'
    #     assert user1.resp_delegate['min_balance_limit'] == '11.55'
    #     assert user1.resp_delegate['out_curr'] == 'USD'
    #     assert user1.resp_delegate['out_fee'] == {'add': '1', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.055'}
    #     assert user1.resp_delegate['payway'] == 'cash_kiev'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(1))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_params_10(self):
    #     """ Getting params for payout to paymer RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(10), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
    #                            'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['from_in_curr_balance'] == '53.33'
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '20'
    #     assert user1.resp_delegate['in_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['is_convert'] == True
    #     assert user1.resp_delegate['max'] == '50'
    #     assert user1.resp_delegate['max_by_balance'] == '53.33'
    #     assert user1.resp_delegate['min'] == '10'
    #     assert user1.resp_delegate['min_balance_limit'] == '10'
    #     assert user1.resp_delegate['out_curr'] == 'RUB'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['payway'] == 'paymer'
    #     assert user1.resp_delegate['pwtp'] == 'cheque'
    #     assert user1.resp_delegate['rate'] == ['1', '2.6666']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_params_11(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for payout to webmoney USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(10))
    #     user1.merchant1.payout_params(payway='webmoney', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['from_in_curr_balance'] == '8.72'
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'UAH'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '250'
    #     assert user1.merchant1.resp_payout_params['in_fee'] ==\
    #            {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_payout_params['is_convert'] == True
    #     assert user1.merchant1.resp_payout_params['max'] == '10'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '8.72'
    #     assert user1.merchant1.resp_payout_params['min'] == '1'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '1'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'webmoney'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['28.637', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_params_12(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for payout to exmo USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(15), tech_max=bl(50))
    #     user1.merchant1.payout_params(payway='exmo', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['from_in_curr_balance'] == '17.55'
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'UAH'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '505'
    #     assert user1.merchant1.resp_payout_params['in_fee'] ==\
    #            {'add': '57.53', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.035'}
    #     assert user1.merchant1.resp_payout_params['is_convert'] == True
    #     assert user1.merchant1.resp_payout_params['max'] == '50'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '15.02'
    #     assert user1.merchant1.resp_payout_params['min'] == '15'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '17.53'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '2', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.035'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'exmo'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'cheque'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['28.7639', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_params_13(self, _disable_st_value):
    #     """ Getting params for payout
    #     Payments in the entire system are blocked
    #     Payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.01'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '98'
    #     assert user1.resp_delegate['max_by_balance'] == '0.01'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.01'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['payway'] == 'visamc'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_14(self, _disable_st_value):
    #     """ Getting params for payout
    #     Payments in the entire system are blocked
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1.02), tech_max=bl(3000))
    #     user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '3000'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['min'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'payeer'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
    #
    # def test_params_15(self, _enable_merchant_payout_allowed):
    #     """ Getting params for payout
    #     Sender's payout is blocked
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.01'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '98'
    #     assert user1.resp_delegate['max_by_balance'] == '0.01'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.01'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['payway'] == 'visamc'
    #     assert user1.resp_delegate['pwtp'] == 'sci'
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #     assert user1.resp_delegate['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_16(self, _enable_merchant_payout_allowed):
    #     """ Getting params for payout
    #     Sender's payout is blocked
    #     Payout to payeer RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1.02), tech_max=bl(3000))
    #     user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['in_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['in_curr_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['is_convert'] == False
    #     assert user1.merchant1.resp_payout_params['max'] == '3000'
    #     assert user1.merchant1.resp_payout_params['max_by_balance'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['min'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['min_balance_limit'] == '1.02'
    #     assert user1.merchant1.resp_payout_params['out_curr'] == 'RUB'
    #     assert user1.merchant1.resp_payout_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_payout_params['payway'] == 'payeer'
    #     assert user1.merchant1.resp_payout_params['pwtp'] == 'sci'
    #     assert user1.merchant1.resp_payout_params['rate'] == ['1', '1']
    #     assert user1.merchant1.resp_payout_params['uaccount'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
    #
    # def test_params_17(self):
    #     """ Getting params for payout
    #     Payout by non-existing merchant
    #     Payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': '1234567890'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'NotFound'
    #     assert user1.resp_delegate['data']['reason'] == 'Merchant with lid 1234567890 was not found'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_18(self, _enable_merchant_is_active):
    #     """ Getting params for payout
    #     Payout by an active merchant
    #     Payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidMerchant'
    #     assert user1.resp_delegate['data']['reason'] == f'Active merchant with lid {user1.merchant1.lid} was not found'
    #     assert user1.resp_delegate['data']['reason'] == \
    #            'Active merchant with lid {} was not found'.format(user1.merchant1.lid)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_19(self):
    #     """ Getting params for payout
    #     Payout of non-existing out_curr currency delegate
    #     Payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'TST',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'TST'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_20(self):
    #     """ Getting params for payout
    #     Payout of non-existing out_curr currency payout_create
    #     Payout to payeer RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1.02), tech_max=bl(3.36))
    #     user1.merchant1.payout_params(payway='payeer', out_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'TST'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
    #
    # def test_params_21(self, _enable_currency):
    #     """ Getting params for payout
    #     Payout inactive currency out_curr delegate
    #     Payout to visamc UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InactiveCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'UAH'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_22(self, _enable_currency):
    #     """ Getting params for payout
    #     Payout inactive currency out_curr payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1.02), tech_max=bl(3.36))
    #     user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InactiveCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'RUB'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
    #
    # def test_params_23(self):
    #     """ Getting params for payout
    #     Payout of non-existing in_curr currency delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
    #                            'in_curr': 'TST', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'TST'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_params_24(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for payout
    #     Payout of non-existing in_curr currency payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_params(payway='webmoney', out_curr='USD', in_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'TST'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_params_25(self, _enable_currency):
    #     """ Getting params for payout
    #     Payout inactive currency in_curr delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
    #                            'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InactiveCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'UAH'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_params_26(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):
    #     """ Getting params for payout
    #     Payout inactive currency in_curr payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_params(payway='exmo', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InactiveCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'UAH'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_params_27(self, _enable_currency):
    #     """ Getting params for payout
    #     Currency out_curr off delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InactiveCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'UAH'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_28(self, _enable_currency):
    #     """ Getting params for payout
    #     Currency out_curr off payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_params(payway='payeer', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InactiveCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'RUB'
    #
    # def test_params_29(self, _enable_currency):
    #     """ Getting params for payout
    #     Currency in_curr off delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
    #                            'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InactiveCurrency'
    #     assert user1.resp_delegate['data']['reason'] == 'UAH'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_params_30(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):
    #     """ Getting params for payout
    #     Currency in_curr off payout_create
    #     Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.payout_params(payway='exmo', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InactiveCurrency'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'UAH'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_params_31(self):
    #     """ Getting params for payout
    #     Request without out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     assert user1.resp_delegate['data']['reason'] == "method 'merchant.delegate' missing 1 argument: 'out_curr'"
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_32(self): # Запрос без out_curr (не передан)
    #     """ Getting params for payout
    #     Request without out_curr payout.create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.params',
    #             'params': {'payway': 'payeer'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #     assert loads(r.text)['error']['data']['reason'] == "method 'payout.params' missing 1 argument: 'out_curr'"
    #
    # def test_params_33(self):
    #     """ Getting params for payout
    #     Request without out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': None,
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     assert user1.resp_delegate['data']['reason'] == "method payout.calc' missing 1 argument: 'out_curr'"
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_34(self):
    #     """ Getting params for payout
    #     Request out_curr = None
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     user1.merchant1.payout_params(payway='payeer', out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_payout_params)
    #     assert user1.merchant1.resp_payout_params['error']['message'] == 'InvalidInputParams'
    #     assert user1.merchant1.resp_payout_params['error']['data']['reason'] == \
    #            "method payout.calc' missing 1 argument: 'out_curr'"
    #
    # def test_params_35(self):
    #     """ Getting params for payout
    #     Request with extra parameter 'par': '123' delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     assert user1.resp_delegate['data']['reason'] == "method 'merchant.delegate' received a redundant argument 'par'"
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_params_36(self): # Запрос с лишним параметром 'par': '123'
    #     """ Getting params for payout
    #     Request with extra parameter 'par': '123' payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.params',
    #             'params': {'payway': 'payeer', 'out_curr': 'UAH', 'par': '123'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #     assert loads(r.text)['error']['data']['reason'] == "method 'payout.params' received a redundant argument 'par'"
    #
    # def test_params_37(self): # Запрос без подписи
    #     """ Getting params for payout
    #     Unsigned request
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.params',
    #             'params': {'payway': 'payeer', 'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == 'Add x-signature to headers'

    def test_params_38(self): # Запрос с невалидной подписью
        """ Getting params for payout
        Request with invalid sign
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'payout.params',
                'params': {'payway': 'payeer', 'out_curr': 'RUB'},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['message'] == 'InvalidSign'
        assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'

    def test_params_39(self, _enable_exchange_operation_UAH_RUB):
        # передан in_curr и неактивно направление конвертации из in_curr в out_curr
        """ Getting params for payout
        inactive exchange direction from in_curr to out_curr
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
                               'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'UnavailExchange'
        assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange for UAH to RUB'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))

    def test_params_40(self): # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
        """ Getting params for payout
        there is no conversion direction from in_curr to out_curr
        Payout to paymer 50 RUB: USD to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='USD', out_currency='RUB')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'params', 'payway': 'paymer', 'out_curr': 'RUB',
                               'in_curr': 'USD', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'UnavailExchange'
        assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange for USD to RUB'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))

    def test_params_41(self, _custom_fee, _disable_personal_operation_fee_transfer_USD,
                             _enable_exchange_operation_UAH_USD):
        # передан in_curr и неактивно направление конвертации из in_curr в out_curr
        """ Getting params for payout
        there is no conversion direction from in_curr to out_curr
        Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_params(payway='webmoney', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_params)
        assert user1.merchant1.resp_payout_params['error']['message'] == 'UnavailExchange'
        assert user1.merchant1.resp_payout_params['error']['data']['reason'] == 'Unavailable exchange for UAH to USD'
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_params_42(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
        """ Getting params for payout
        there is no conversion direction from in_curr to out_curr
        Payout to webmoney 8.33 USD: BCHABC to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='BCHABC', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BCHABC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_params(payway='webmoney', out_curr='USD', in_curr='BCHABC')
        # pprint.pprint(user1.merchant1.resp_payout_params)
        assert user1.merchant1.resp_payout_params['error']['message'] == 'UnavailExchange'
        assert user1.merchant1.resp_payout_params['error']['data']['reason'] == \
               'Unavailable exchange for BCHABC to USD'
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)


class TestInCurrList:
    """ Testing payout in_curr_list method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)
        admin.set_wallet_amount(balance=bl(2000), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1000), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(3000), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(300), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(250), currency='ETH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(100), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(200), currency='USDT', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(150), currency='LTC', merch_lid=user1.merchant1.lid)

    def test_InCurrList_visamc_UAH(self):
        """ Getting payout in_curr_list visamc UAH """
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=False, currency='UAH',
                                     is_active=True, tech_min=bl(10), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(93.97))
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43))
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(278907.43607), fee=0, in_currency='BTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(0.35851), is_active=False)
        admin.set_rate_exchange(rate=bl(6683.841), fee=0, in_currency='ETH', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(24.50656), fee=0, in_currency='USDT', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(4084.3), is_active=False)
        admin.set_rate_exchange(rate=bl(2542.69187), fee=0, in_currency='LTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='visamc', out_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'visamc': ['UAH', 'RUB', 'USD']}

    def test_InCurrList_visamc_RUB(self):
        """ Getting payout in_curr_list visamc RUB """
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=False, currency='RUB',
                                     is_active=True, tech_min=bl(10), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(101))
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04))
        admin.set_rate_exchange(rate=bl(724715.12064), fee=0, in_currency='BTC', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(0.13794), is_active=False)
        admin.set_rate_exchange(rate=bl(17065.28255), fee=0, in_currency='ETH', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(5.85537), is_active=False)
        admin.set_rate_exchange(rate=bl(62.65277), fee=0, in_currency='USDT', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(1596.89), is_active=False)
        admin.set_rate_exchange(rate=bl(6516.86546), fee=0, in_currency='LTC', out_currency='RUB',
                                tech_min=bl(0.002), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='visamc', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'visamc': ['UAH', 'RUB']}

    def test_InCurrList_payeer_RUB(self):
        """ Getting payout in_curr_list payeer RUB """
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=False, currency='RUB',
                                     is_active=True, tech_min=bl(10), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(101))
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04))
        admin.set_rate_exchange(rate=bl(724715.12064), fee=0, in_currency='BTC', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(0.13794), is_active=False)
        admin.set_rate_exchange(rate=bl(17065.28255), fee=0, in_currency='ETH', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(5.85537), is_active=False)
        admin.set_rate_exchange(rate=bl(62.65277), fee=0, in_currency='USDT', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(1596.89), is_active=False)
        admin.set_rate_exchange(rate=bl(6516.86546), fee=0, in_currency='LTC', out_currency='RUB',
                                tech_min=bl(0.002), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='payeer', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'payeer': ['UAH', 'RUB']}

    def test_InCurrList_btc_BTC(self):
        """ Getting payout in_curr_list btc BTC """
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=False, currency='BTC',
                                     is_active=True, tech_min=bl(10), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC',
                                     is_active=True, tech_min=bl(1), tech_max=bl(101))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.0005), in_currency='USD', out_currency='BTC',
                                tech_min=bl(1), tech_max=bl(2000), is_active=False)
        admin.set_rate_exchange(rate=bl(732822.1641), fee=0, in_currency='RUB', out_currency='BTC',
                                tech_min=bl(769.46), tech_max=bl(3869.63), is_active=False)
        admin.set_rate_exchange(rate=bl(280305.46835), fee=0, in_currency='UAH', out_currency='BTC',
                                tech_min=bl(294.32), tech_max=bl(1630.07), is_active=False)
        admin.set_rate_exchange(rate=bl(42.51193), fee=0, in_currency='ETH', out_currency='BTC',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(11580.45087), fee=0, in_currency='USDT', out_currency='BTC',
                                tech_min=bl(12.15), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(111.57669), fee=0, in_currency='LTC', out_currency='BTC',
                                tech_min=bl(0.0105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='btc', out_curr='BTC')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'btc': ['BTC']}

    def test_InCurrList_privat24_UAH(self):
        """ Getting payout in_curr_list privat24 UAH """
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=False, currency='UAH',
                                     is_active=True, tech_min=bl(10), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(93.97))
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43))
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(278907.43607), fee=0, in_currency='BTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(0.35851), is_active=False)
        admin.set_rate_exchange(rate=bl(6683.841), fee=0, in_currency='ETH', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(24.50656), fee=0, in_currency='USDT', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(4084.3), is_active=False)
        admin.set_rate_exchange(rate=bl(2542.69187), fee=0, in_currency='LTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='privat24', out_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'privat24': ['UAH', 'RUB', 'USD']}

    def test_InCurrList_ltc_LTC(self):
        """ Getting payout in_curr_list ltc LTC """
        admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=False, currency='LTC',
                                     is_active=True, tech_min=bl(0.002), tech_max=bl(3))
        admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC',
                                     is_active=True, tech_min=bl(0.002), tech_max=bl(0.87627))
        admin.set_rate_exchange(rate=bl(104.8214), fee=0, in_currency='USD', out_currency='LTC',
                                tech_min=bl(0.11), tech_max=bl(61.45), is_active=False)
        admin.set_rate_exchange(rate=bl(6588.8146), fee=0, in_currency='RUB', out_currency='LTC',
                                tech_min=bl(13.2), tech_max=bl(65982.96), is_active=False)
        admin.set_rate_exchange(rate=bl(2784.58981), fee=0, in_currency='UAH', out_currency='LTC',
                                tech_min=bl(2.92), tech_max=bl(1631.31), is_active=False)
        admin.set_rate_exchange(rate=bl(110.86209), fee=0, in_currency='BTC', out_currency='LTC',
                                tech_min=bl(0.00009), tech_max=bl(0.09018), is_active=False)
        admin.set_rate_exchange(rate=bl(2.61242), fee=0, in_currency='ETH', out_currency='LTC',
                                tech_min=bl(0.0105), tech_max=bl(3.82964), is_active=False)
        admin.set_rate_exchange(rate=bl(120.41), fee=0, in_currency='USDT', out_currency='LTC',
                                tech_min=bl(0.12), tech_max=bl(35.75), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='ltc', out_curr='LTC')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'ltc': ['LTC']}

    def test_InCurrList_perfect_USD(self):
        """ Getting payout in_curr_list perfect USD """
        admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=False, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(2.24))
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.04), in_currency='RUB', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.03), in_currency='BTC', out_currency='USD',
                                tech_min=0, tech_max=bl(3), is_active=False)
        admin.set_rate_exchange(rate=bl(273.49892), fee=0, in_currency='ETH', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(1.005), fee=0, in_currency='USDT', out_currency='USD',
                                tech_min=bl(0.02), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(104.01284), fee=0, in_currency='LTC', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='perfect', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'perfect': ['UAH', 'USD']}

    def test_InCurrList_paymer_RUB(self):
        """ Getting payout in_curr_list paymer RUB """
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=False, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04))
        admin.set_rate_exchange(rate=bl(724715.12064), fee=0, in_currency='BTC', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(0.13794), is_active=False)
        admin.set_rate_exchange(rate=bl(17065.28255), fee=0, in_currency='ETH', out_currency='RUB',
                                tech_min=bl(0.00105), tech_max=bl(5.85537), is_active=False)
        admin.set_rate_exchange(rate=bl(62.65277), fee=0, in_currency='USDT', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(1596.89), is_active=False)
        admin.set_rate_exchange(rate=bl(6516.86546), fee=0, in_currency='LTC', out_currency='RUB',
                                tech_min=bl(0.002), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='paymer', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'paymer': ['UAH', 'RUB']}

    def test_InCurrList_exmo_UAH(self):
        """ Getting payout in_curr_list exmo UAH """
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=False, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(15.48))
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43))
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(278907.43607), fee=0, in_currency='BTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(0.35851), is_active=False)
        admin.set_rate_exchange(rate=bl(6683.841), fee=0, in_currency='ETH', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(24.50656), fee=0, in_currency='USDT', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(4084.3), is_active=False)
        admin.set_rate_exchange(rate=bl(2542.69187), fee=0, in_currency='LTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='exmo', out_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'exmo': ['UAH', 'RUB', 'USD']}

    def test_InCurrList_exmo_USD(self):
        """ Getting payout in_curr_list exmo USD """
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=False, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(2))
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(2))
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.04), in_currency='RUB', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.03), in_currency='BTC', out_currency='USD',
                                tech_min=0, tech_max=bl(3), is_active=False)
        admin.set_rate_exchange(rate=bl(273.49892), fee=0, in_currency='ETH', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(1.005), fee=0, in_currency='USDT', out_currency='USD',
                                tech_min=bl(0.02), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(104.01284), fee=0, in_currency='LTC', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='exmo', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'exmo': ['UAH', 'USD']}

    def test_InCurrList_kuna_UAH(self):
        """ Getting payout in_curr_list kuna UAH """
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=False, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43))
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(278907.43607), fee=0, in_currency='BTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(0.35851), is_active=False)
        admin.set_rate_exchange(rate=bl(6683.841), fee=0, in_currency='ETH', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(24.50656), fee=0, in_currency='USDT', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(4084.3), is_active=False)
        admin.set_rate_exchange(rate=bl(2542.69187), fee=0, in_currency='LTC', out_currency='UAH',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='kuna', out_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list == {'kuna': ['UAH', 'RUB', 'USD']}

    def test_InCurrList_UnavailPayway_inactive_for_merchant(self):
        """ Getting payout in_curr_list UnavailPayway (inactive for merchant) """
        admin.set_pwcurrency_min_max(payway=admin.payway['nixmoney']['id'], is_out=False, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(2))
        admin.set_pwcurrency_min_max(payway=admin.payway['nixmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(2))
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.04), in_currency='RUB', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.03), in_currency='BTC', out_currency='USD',
                                tech_min=0, tech_max=bl(3), is_active=False)
        admin.set_rate_exchange(rate=bl(273.49892), fee=0, in_currency='ETH', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(1.005), fee=0, in_currency='USDT', out_currency='USD',
                                tech_min=bl(0.02), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(104.01284), fee=0, in_currency='LTC', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['nixmoney']['id'], is_active=False)
        user1.merchant1.payout_in_curr_list(payway='nixmoney', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list['error']['message'] == 'UnavailPayway'
        assert user1.merchant1.resp_payout_in_curr_list['error']['data']['reason'] == 'Payway nixmoney is inactive for merchant'

    def test_InCurrList_InvalidPayway_not_existing(self):
        """ Getting payout in_curr_list UnavailPayway (not existing) """
        user1.merchant1.payout_in_curr_list(payway='test', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list['error']['message'] == 'InvalidPayway'
        assert user1.merchant1.resp_payout_in_curr_list['error']['data']['reason'] == 'test'

    def test_InCurrList_InvalidPayway_inactive_for_system(self):
        """ Getting payout in_curr_list UnavailPayway (inactive for system) """
        user1.merchant1.payout_in_curr_list(payway='cash', out_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list['error']['message'] == 'InvalidPayway'
        assert user1.merchant1.resp_payout_in_curr_list['error']['data']['reason'] == 'cash'

    def test_InCurrList_InvalidCurrency_inactive(self):
        """ Getting payout in_curr_list InvalidCurrency (inactive) """
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=False, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.04), in_currency='RUB', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000))
        admin.set_rate_exchange(rate=bl(3580.6541), fee=bl(0.03), in_currency='BTC', out_currency='USD',
                                tech_min=0, tech_max=bl(3), is_active=False)
        admin.set_rate_exchange(rate=bl(273.49892), fee=0, in_currency='ETH', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_rate_exchange(rate=bl(1.005), fee=0, in_currency='USDT', out_currency='USD',
                                tech_min=bl(0.02), tech_max=bl(10000), is_active=False)
        admin.set_rate_exchange(rate=bl(104.01284), fee=0, in_currency='LTC', out_currency='USD',
                                tech_min=bl(0.00105), tech_max=bl(10), is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        user1.merchant1.payout_in_curr_list(payway='payeer', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list['error']['message'] == 'InvalidCurrency'

    def test_InCurrList_InvalidCurrency_not_existing(self):
        """ Getting payout in_curr_list InvalidCurrency (not existing) """
        user1.merchant1.payout_in_curr_list(payway='payeer', out_curr='TST')
        # pprint.pprint(user1.merchant1.resp_payout_in_curr_list)
        assert user1.merchant1.resp_payout_in_curr_list['error']['message'] == 'InvalidCurrency'
        assert user1.merchant1.resp_payout_in_curr_list['error']['data']['reason'] == 'TST'


class TestGetCheque:
    """ Testing payout get_cheque method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    """ 1. Включить аплинк
        2. Выполнить test_GetCheque_0
        3. Взять lid ордера из админки (подрядт test_GetCheque_1-2 выполниться не успевают - ордер не успевает изменить статус)
        4. Подставить lid в test_GetCheque_1-2 и 5-6
        5. Запустить test_GetCheque_1-2
        6. Выключить аплинк
        7. Запустить test_GetCheque_00...test_GetCheque_3-6"""

    def test_GetCheque_0(self): # Создание чека
        """ Payout to kuna 100 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(1000))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '100', 'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # print('lid', user1.merchant1.lid)
        pprint.pprint(user1.resp_delegate['lid'])
        # assert user1.resp_delegate['status'] == 'done'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_GetCheque_1(self):
        """ Getting payout get_cheque"""
        # user1.merchant1.payout_in_curr_list(payway='payeer', out_curr='RUB')
        user1.merchant1.payout_get_cheque(lid=19337)#user1.resp_delegate['lid'])
        assert user1.merchant1.resp_payout_get_cheque['cheque']['amount']== '100'
        assert user1.merchant1.resp_payout_get_cheque['cheque']['currency']== 'UAH'
        assert user1.merchant1.resp_payout_get_cheque['in_amount']== '100'
        assert user1.merchant1.resp_payout_get_cheque['in_curr']== 'UAH'
        assert user1.merchant1.resp_payout_get_cheque['in_fee_amount']== '0'
        assert user1.merchant1.resp_payout_get_cheque['orig_amount']== '100'
        assert user1.merchant1.resp_payout_get_cheque['out_amount']== '100'
        assert user1.merchant1.resp_payout_get_cheque['out_curr']== 'UAH'
        assert user1.merchant1.resp_payout_get_cheque['out_fee_amount']== '0'
        assert user1.merchant1.resp_payout_get_cheque['payway_name']== 'kuna'
        assert user1.merchant1.resp_payout_get_cheque['rate']== None
        assert user1.merchant1.resp_payout_get_cheque['reqdata']['amount']== '100'
        assert user1.merchant1.resp_payout_get_cheque['reqdata']['in_curr']== None
        assert user1.merchant1.resp_payout_get_cheque['reqdata']['out_curr']== 'UAH'
        assert user1.merchant1.resp_payout_get_cheque['reqdata']['payway']== 'kuna'
        assert user1.merchant1.resp_payout_get_cheque['reqdata']['userdata']== {}
        assert user1.merchant1.resp_payout_get_cheque['status']== 'done'
        assert user1.merchant1.resp_payout_get_cheque['tp']== 'payout'
        assert user1.merchant1.resp_payout_get_cheque['userdata']==  {'payee': ''}

    def test_GetCheque_2(self):
        """ Getting payout get_cheque"""
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'get_cheque', 'lid': '19337',#str(user1.resp_delegate['lid']),
                               'm_lid': str(user1.merchant1.lid)})
        assert user1.resp_delegate['cheque']['amount']== '100'
        assert user1.resp_delegate['cheque']['currency']== 'UAH'
        assert user1.resp_delegate['in_amount']== '100'
        assert user1.resp_delegate['in_curr']== 'UAH'
        assert user1.resp_delegate['in_fee_amount']== '0'
        assert user1.resp_delegate['orig_amount']== '100'
        assert user1.resp_delegate['out_amount']== '100'
        assert user1.resp_delegate['out_curr']== 'UAH'
        assert user1.resp_delegate['out_fee_amount']== '0'
        assert user1.resp_delegate['payway_name']== 'kuna'
        assert user1.resp_delegate['rate']== None
        assert user1.resp_delegate['reqdata']['amount']== '100'
        assert user1.resp_delegate['reqdata']['in_curr']== None
        assert user1.resp_delegate['reqdata']['out_curr']== 'UAH'
        assert user1.resp_delegate['reqdata']['payway']== 'kuna'
        assert user1.resp_delegate['reqdata']['userdata']== {}
        assert user1.resp_delegate['status']== 'done'
        assert user1.resp_delegate['tp']== 'payout'
        assert user1.resp_delegate['userdata']==  {'payee': ''}

    def test_GetCheque_00(self): # Создание чека
        """ Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(39.99))

    def test_GetCheque_3(self):
        """ Getting payout get_cheque"""
        user1.merchant1.payout_get_cheque(lid=user1.resp_delegate['lid'])
        assert user1.merchant1.resp_payout_get_cheque['message']== 'NotFound'

    def test_GetCheque_4(self):
        """ Getting payout get_cheque"""
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'get_cheque', 'lid': str(user1.resp_delegate['lid']),
                               'm_lid': str(user1.merchant1.lid)})
        assert user1.resp_delegate['message']== 'NotFound'

    def test_GetCheque_5(self):
        """ Getting payout get_cheque"""
        # user1.merchant1.payout_in_curr_list(payway='payeer', out_curr='RUB')
        user1.merchant1.payout_get_cheque(lid=19337)#user1.resp_delegate['lid'])
        assert user1.merchant1.resp_payout_get_cheque['data']['reason']== 'Missing report from core'
        assert user1.merchant1.resp_payout_get_cheque['message']== 'ApiError'

    def test_GetCheque_6(self):
        """ Getting payout get_cheque"""
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'get_cheque', 'lid': '19337',#str(user1.resp_delegate['lid']),
                               'm_lid': str(user1.merchant1.lid)})
        assert user1.resp_delegate['data']['reason']== 'Missing report from core'
        assert user1.resp_delegate['message']== 'ApiError'


class TestPayoutGet:
    """ Testing payout get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_get_payout_1(self):
        """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        # print('o_lid', user1.resp_delegate['lid'])
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'get', 'o_lid': user1.resp_delegate['lid'],
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['owner'] == str(user1.merchant1.lid)
        assert user1.resp_delegate['payway_name'] == 'visamc'
        assert user1.resp_delegate['rate'] == None
        assert user1.resp_delegate['ref'] == None
        assert user1.resp_delegate['renumeration'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.resp_delegate['status'] == 'new'
        assert user1.resp_delegate['tp'] == 'payout'
        assert user1.resp_delegate['userdata'] == {'payee': '4731185613244273'}
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_get_payout_2(self):
        """ Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # time.sleep(2)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        user1.merchant1.payout_get(o_lid=user1.merchant1.resp_payout_create['result']['lid'])
        # pprint.pprint(user1.merchant1.resp_payout_get)
        assert user1.merchant1.resp_payout_get['account_amount'] == '1.02'
        assert user1.merchant1.resp_payout_get['in_amount'] == '1.02'
        assert user1.merchant1.resp_payout_get['in_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_get['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_get['out_amount'] == '1.02'
        assert user1.merchant1.resp_payout_get['out_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_get['out_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_get['owner'] == str(user1.merchant1.lid)
        assert user1.merchant1.resp_payout_get['payway_name'] == 'payeer'
        assert user1.merchant1.resp_payout_get['reqdata']['userdata'] == {'payee': 'P14812343'}

    def test_get_payout_3(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 4% for exchange and with personal fee 2% for exchange
        with common percent fee 5% for payout and with common absolute fee 5 USD for payout
        with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
        admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
        admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
        user1.merchant1.payout_create(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # assert user1.merchant1.resp_payout_create['result']['status'] == 'done'
        user1.merchant1.payout_get(o_lid=user1.merchant1.resp_payout_create['result']['lid'])
        # pprint.pprint(user1.merchant1.resp_payout_get)
        assert user1.merchant1.resp_payout_get['account_amount'] == '504.24'
        assert user1.merchant1.resp_payout_get['in_amount'] == '431.46'
        assert user1.merchant1.resp_payout_get['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_get['in_fee_amount'] == '72.78'
        assert user1.merchant1.resp_payout_get['out_amount'] == '15'
        assert user1.merchant1.resp_payout_get['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_get['out_fee_amount'] == '2.53'
        assert user1.merchant1.resp_payout_get['rate'] == ['28.7639', '1']
        assert user1.merchant1.resp_payout_get['reqdata']['amount'] == '15'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['exmo']['id'], is_active=False)

    def test_get_payout_4(self):
        """ NotFound    не найден ордер c соответствующим o_lid """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'get', 'o_lid': 99999,
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'NotFound'
        assert user1.resp_delegate['data']['reason'] == 'Not found order with params'

    def test_get_payout_5(self):
        """ InvalidParam    передан o_lid несоответствующего формата """
        user1.merchant1.payout_get(o_lid='test')
        # pprint.pprint(user1.merchant1.resp_payout_get)
        assert user1.merchant1.resp_payout_get['message'] == 'InvalidParam'
        assert user1.merchant1.resp_payout_get['data']['reason'] == 'test'


class TestPayoutList:
    """ Testing payout list method.

        Перед запуском TestPayoutList запустить TestPayout"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_payout_list_1(self):
        """ All """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)

    def test_payout_list_2(self):
        """ All """
        user1.merchant1.payout_list()
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.resp_delegate['total'] == user1.merchant1.resp_payout_list['total']

    def test_payout_list_3(self):
        """ count = 12 """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'count': '12'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['count'] == 12

    def test_payout_list_4(self):
        """ count = 12 """
        user1.merchant1.payout_list(count='12')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['count'] == 12

    def test_payout_list_5(self):
        """ first """
        first = user1.resp_delegate['total']-12
        # print('\n', 'first', first)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'first': str(first)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['first'] == first

    def test_payout_list_6(self):
        """ first """
        first = user1.merchant1.resp_payout_list['total']-12
        # print('\n', 'first', first)
        user1.merchant1.payout_list(first=str(first))
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['first'] == first

    def test_payout_list_7(self):
        """ visamc """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'payway': 'visamc'})
        first = user1.resp_delegate['total']-1
        # print('\n', 'first', first)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'first': str(first), 'payway': 'visamc'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['data'][0]['payway_name'] == 'visamc'
        assert user1.resp_delegate['data'][0]['reqdata']['payway'] == 'visamc'

    def test_payout_list_8(self):
        """ payeer """
        user1.merchant1.payout_list(payway='payeer')
        first = user1.merchant1.resp_payout_list['total']-1
        # print('\n', 'first', first)
        user1.merchant1.payout_list(first=str(first), payway='payeer')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['data'][0]['payway_name'] == 'payeer'
        assert user1.merchant1.resp_payout_list['data'][0]['reqdata']['payway'] == 'payeer'

    def test_payout_list_9(self):
        """ 'out_curr': 'UAH' """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'first': '0', 'count': '5', 'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['data'][0]['in_curr'] == 'UAH'
        assert user1.resp_delegate['data'][0]['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][0]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][0]['reqdata']['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][1]['in_curr'] == 'UAH'
        assert user1.resp_delegate['data'][1]['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][1]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][1]['reqdata']['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][2]['in_curr'] == 'UAH'
        assert user1.resp_delegate['data'][2]['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][2]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][2]['reqdata']['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][3]['in_curr'] == 'UAH'
        assert user1.resp_delegate['data'][3]['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][3]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][3]['reqdata']['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][4]['in_curr'] == 'UAH'
        assert user1.resp_delegate['data'][4]['out_curr'] == 'UAH'
        assert user1.resp_delegate['data'][4]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][4]['reqdata']['out_curr'] == 'UAH'

    def test_payout_list_10(self):
        """ out_curr='USD' """
        user1.merchant1.payout_list(first='0', count='4', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['data'][0]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][0]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][0]['reqdata']['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][0]['reqdata']['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][1]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][1]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][1]['reqdata']['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][1]['reqdata']['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][2]['in_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][2]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][2]['reqdata']['in_curr'] == None
        assert user1.merchant1.resp_payout_list['data'][2]['reqdata']['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][3]['in_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][3]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][3]['reqdata']['in_curr'] == None
        assert user1.merchant1.resp_payout_list['data'][3]['reqdata']['out_curr'] == 'USD'

    def test_payout_list_11(self):
        """ in_curr': 'RUB' """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'first': '0', 'count': '2', 'in_curr': 'RUB'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['data'][0]['in_curr'] == 'RUB'
        assert user1.resp_delegate['data'][0]['out_curr'] == 'RUB'
        assert user1.resp_delegate['data'][0]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][0]['reqdata']['out_curr'] == 'RUB'
        assert user1.resp_delegate['data'][1]['in_curr'] == 'RUB'
        assert user1.resp_delegate['data'][1]['out_curr'] == 'RUB'
        assert user1.resp_delegate['data'][1]['reqdata']['in_curr'] == None
        assert user1.resp_delegate['data'][1]['reqdata']['out_curr'] == 'RUB'

    def test_payout_list_12(self):
        """ in_curr='UAH' """
        user1.merchant1.payout_list(first='0', count='6', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['data'][0]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][0]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][0]['reqdata']['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][0]['reqdata']['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][1]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][1]['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][1]['reqdata']['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][1]['reqdata']['out_curr'] == 'USD'
        assert user1.merchant1.resp_payout_list['data'][2]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][2]['out_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_list['data'][2]['reqdata']['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][2]['reqdata']['out_curr'] == 'RUB'
        assert user1.merchant1.resp_payout_list['data'][3]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][3]['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][3]['reqdata']['in_curr'] == None
        assert user1.merchant1.resp_payout_list['data'][3]['reqdata']['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][4]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][4]['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][4]['reqdata']['in_curr'] == None
        assert user1.merchant1.resp_payout_list['data'][4]['reqdata']['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][5]['in_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][5]['out_curr'] == 'UAH'
        assert user1.merchant1.resp_payout_list['data'][5]['reqdata']['in_curr'] == None
        assert user1.merchant1.resp_payout_list['data'][5]['reqdata']['out_curr'] == 'UAH'

    def test_payout_list_13(self):
        """ in_curr': 'TST' """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'in_curr': 'TST'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidCurrency'
        assert user1.resp_delegate['data']['reason'] == 'TST'

    def test_payout_list_14(self):
        """ out_curr': 'TST' """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'out_curr': 'TST'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidCurrency'
        assert user1.resp_delegate['data']['reason'] == 'TST'

    def test_payout_list_15(self):
        """ in_curr='TST' """
        user1.merchant1.payout_list(first='0', count='6', in_curr='TST')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['message'] == 'InvalidCurrency'
        assert user1.merchant1.resp_payout_list['data']['reason'] == 'TST'

    def test_payout_list_16(self):
        """ out_curr='TST' """
        user1.merchant1.payout_list(first='0', count='6', out_curr='TST')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['message'] == 'InvalidCurrency'
        assert user1.merchant1.resp_payout_list['data']['reason'] == 'TST'

    def test_payout_list_17(self):
        """ 'payway': 'test' """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'payway': 'test'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidPayway'
        assert user1.resp_delegate['data']['reason'] == 'pw_name'

    def test_payout_list_18(self):
        """ payway='test' """
        user1.merchant1.payout_list(payway='test')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['message'] == 'InvalidPayway'
        assert user1.merchant1.resp_payout_list['data']['reason'] == 'pw_name'

    def test_payout_list_19(self):
        """ first='-1' """
        user1.merchant1.payout_list(first='-1', count='6', in_curr='LTC')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['message'] == 'InvalidParam'
        assert user1.merchant1.resp_payout_list['data']['reason'] == 'first: - has to be a positive number'

    def test_payout_list_20(self):
        """ first='1.5' """
        user1.merchant1.payout_list(first='1.5', count='6', out_curr='BTC')
        # pprint.pprint(user1.merchant1.resp_payout_list)
        assert user1.merchant1.resp_payout_list['message'] == 'InvalidParam'
        assert user1.merchant1.resp_payout_list['data']['reason'] == 'first - has to be an Integer'

    def test_payout_list_21(self):
        """ count = 12 """
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'list', 'm_lid': str(user1.merchant1.lid),
                               'count': 12})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidParam'
        assert user1.resp_delegate['data']['reason'] == "Key 'count' must not be of 'int' type"


@pytest.mark.usefixtures('_payout_fee', '_personal_exchange_fee')
class TestPayoutCalc:
    """ Testing payout calc method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    # def test_payout_calc_1(self): # Вывод суммы равной сумме на счету списания
    #                          # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Calc payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc',
    #                            'amount': '0.01', 'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # def test_payout_calc_2(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
    #     """ Calc payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'kuna',
    #                            'amount': '0.01', 'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(98))
    #
    # # @pytest.mark.skip
    # def test_payout_calc_3(self): # Перевод суммы равной сумме на счету списания
    #     """ Calc payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '1.02'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0'
    #
    # def test_payout_calc_4(self): # Вывод суммы равной техническому максимуму по таблице pwcurrency
    #     """ Calc payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
    #                   payway_id=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
    #                   payway_id=admin.payway['btc']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.99999))
    #     user1.merchant1.payout_calc(payway='btc', amount='0.99999', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '0.99999'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
    #                                  tech_min=bl(0.001), tech_max=bl(0.00463))
    #
    # def test_payout_calc_5(self):
    #     """ Calc payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
    #     admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'privat24',
    #                            'amount': '10', 'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '11.5'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.5'
    #     assert user1.resp_delegate['orig_amount'] == '10'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.5'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['privat24']['id'], is_active=False)
    #
    # def test_payout_calc_6(self):
    #     """ Calc payout to ltc 0.5 LTC: LTC to LTC by MERCHANT with common absolute fee 0.001 LTC for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=bl(0.001), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=True,
    #                                  tech_min=bl(0.002), tech_max=bl(0.6))
    #     user1.merchant1.payout_calc(payway='ltc', amount='0.5', out_curr='LTC')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '0.501'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '0.5'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0.001'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '0.5'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '0.5'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0.001'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['ltc']['id'], is_out=True, currency='LTC', is_active=False,
    #                                  tech_min=bl(0.002), tech_max=bl(0.01349))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['LTC'],
    #                   payway_id=admin.payway['ltc']['id'], is_active=False)
    #
    # # @pytest.mark.skip
    # def test_payout_calc_7(self):
    #     """ Calc payout to qiwi 10 RUB: RUB to RUB by OWNER with common percent fee 5.5% for payout
    #      and common absolute fee 1 RUB for payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=True,
    #                                  tech_min=bl(1), tech_max=bl(100))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'qiwi', 'amount': '10',
    #                            'out_curr': 'RUB', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['orig_amount'] == '10'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['qiwi']['id'], is_out=True, currency='RUB', is_active=False,
    #                                  tech_min=bl(1), tech_max=bl(10))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['qiwi']['id'], is_active=False)
    #
    # def test_payout_calc_8(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc payout to perfect 10 USD: USD to USD by MERCHANT with personal percent fee 5.5% for transfer
    #     and with personal absolute fee 1 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['perfect']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['perfect']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(15))
    #     user1.merchant1.payout_calc(payway='perfect', amount='10', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '11.55'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '10'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '1.55'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '10'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '10'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '1.55'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['perfect']['id'], is_out=True, currency='USD', is_active=True,
    #                                  tech_min=bl(0.01), tech_max=bl(2.24))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['perfect']['id'], is_active=False)
    #
    # def test_payout_calc_9(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
    #     and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
    #     and with personal absolute fee 1 USD  payout."""
    #     admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(15))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'cash_kiev', 'amount': '10',
    #                            'out_curr': 'USD', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '11.55'
    #     assert user1.resp_delegate['in_amount'] == '10'
    #     assert user1.resp_delegate['in_fee_amount'] == '1.55'
    #     assert user1.resp_delegate['orig_amount'] == '10'
    #     assert user1.resp_delegate['out_amount'] == '10'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.55'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(1))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['cash_kiev']['id'], is_active=False)
    #
    # def test_payout_calc_10(self):
    #     """ Calc payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
    #                            'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '18.76'
    #     assert user1.resp_delegate['in_amount'] == '18.76'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '50'
    #     assert user1.resp_delegate['out_amount'] == '50'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['1', '2.6666']
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_payout_calc_11(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_calc(payway='webmoney', amount='8.33', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '238.55'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '8.33'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '8.33'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_payout_calc['rate'] == ['28.637', '1']
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_payout_calc_12(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 4% for exchange and with personal fee 2% for exchange
    #     with common percent fee 5% for payout and with common absolute fee 5 USD for payout
    #     with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
    #     admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
    #     admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
    #                   currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
    #     user1.merchant1.payout_calc(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['account_amount'] == '504.24'
    #     assert user1.merchant1.resp_payout_calc['in_amount'] == '431.46'
    #     assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '72.78'
    #     assert user1.merchant1.resp_payout_calc['orig_amount'] == '15'
    #     assert user1.merchant1.resp_payout_calc['out_amount'] == '15'
    #     assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '2.53'
    #     assert user1.merchant1.resp_payout_calc['rate'] == ['28.7639', '1']
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['exmo']['id'], is_active=False)
    #
    # def test_wrong_payout_calc_1(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Calc payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.02',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32056
    #     assert user1.resp_delegate['message'] == 'EStateInsufficientFunds'
    #     assert user1.resp_delegate['data']['reason'] == 'Balance 0.01 less then amount 0.02'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_2(self):# Вывод суммы больше чем на счету списания
    #     """ Payout amount more than debit account
    #     Calc payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_calc(payway='payeer', amount='3.02', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32056
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EStateInsufficientFunds'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Balance 1.02 less then amount 3.02'
    #
    # def test_wrong_payout_calc_3(self):# Вывод суммы не существующим мерчантом
    #     """ Payout by non-existing merchant
    #     Calc payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': '1234567890'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32090
    #     assert user1.resp_delegate['message'] == 'EParamNotFound'
    #     assert user1.resp_delegate['data']['field'] == 'm_lid'
    #     assert user1.resp_delegate['data']['reason'] == 'Not found'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_4(self, _enable_merchant_is_active):# Вывод суммы не активным мерчантом
    #     """ Payout by an active merchant
    #     Calc payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'm_lid'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_5(self):# Вывод без суммы (amount = None)
    #     """ amount = None  delegate
    #     Calc payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': None,
    #                             'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_6(self):# Вывод без суммы (amount = None)
    #     """ amount = None  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True,  tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_calc(payway='payeer', amount=None, out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32002
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Should be provided'
    #
    # def test_wrong_payout_calc_7(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_8(self):# Вывод без суммы (amount не передан)
    #     """ Payout without amount (amount not transferred)
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.calc',
    #             'params': {'in_curr': None, 'out_curr': 'RUB', 'payway': 'payeer', 'contact': None, 'region': None,
    #                        'payer': None},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['data']['field'] == 'amount'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should be provided'
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #
    # def test_wrong_payout_calc_9(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True,  tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': 'Test', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be a Number'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_10(self):# Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='payeer', amount='Test', out_curr='RUB', payee='P1007817628')
    #     user1.merchant1.payout_calc(payway='payeer', amount='Test', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32002
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Should be a Number'
    #
    # def test_wrong_payout_calc_11(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.111',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_12(self):# Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_calc(payway='payeer', amount='0.111', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32082
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'amount'
    #
    # def test_wrong_payout_calc_13(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'TST',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_14(self):# Вывод несуществующей валюты out_curr
    #     """ Payout of non-existing out_curr currency payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32014
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Invalid currency name'
    #
    # def test_wrong_payout_calc_15(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
    #     # print(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_calc_16(self, _enable_currency):# Вывод неактивной валюты out_curr
    #     """ Payout inactive currency out_curr payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
    #     user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32033
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Inactive'
    #
    # def test_wrong_payout_calc_17(self):# Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency delegate
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
    #                            'out_curr': 'RUB', 'in_curr': 'TST', 'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_calc_18(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     # Вывод несуществующей валюты in_curr
    #     """ Payout of non-existing in_curr currency payout_create
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB', in_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_payout_calc)
    #     assert user1.merchant1.resp_payout_calc['code'] == -32014
    #     assert user1.merchant1.resp_payout_calc['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_payout_calc['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Invalid currency name'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_wrong_payout_calc_19(self, _enable_currency):# Вывод неактивной валюты in_curr
        """ Payout inactive currency in_curr delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc',  'payway': 'paymer', 'amount': '50',
                               'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32033
        assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
        assert user1.resp_delegate['data']['field'] == 'curr'
        assert user1.resp_delegate['data']['reason'] == 'Inactive'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))

    def test_wrong_payout_calc_20(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):
        # Вывод неактивной валюты in_curr
        """ Payout inactive currency in_curr payout_create
        Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 4% for exchange and with personal fee 2% for exchange
        with common percent fee 5% for payout and with common absolute fee 5 USD for payout
        with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
        admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
        admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        user1.merchant1.payout_calc(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['code'] == -32033
        assert user1.merchant1.resp_payout_calc['message'] == 'EStateCurrencyInactive'
        assert user1.merchant1.resp_payout_calc['data']['field'] == 'curr'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Inactive'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['exmo']['id'], is_active=False)

    def test_wrong_payout_calc_21(self, _enable_currency):# Вывод отключенной валюты out_curr
        """ Currency out_curr off delegate
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.01',
                               'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # print(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32033
        assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
        assert user1.resp_delegate['data']['field'] == 'curr'
        assert user1.resp_delegate['data']['reason'] == 'Inactive'
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_calc_22(self, _enable_currency):# Вывод отключенной валюты out_curr
        """ Currency out_curr off payout_create
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))
        admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
        user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB')
        pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'InactiveCurrency'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == 'RUB'

    def test_wrong_payout_calc_23(self, _enable_currency):# Вывод отключенной валюты in_curr
        """ Currency in_curr off delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
                               'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # print(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InactiveCurrency'
        assert user1.resp_delegate['data']['reason'] == 'UAH'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))

    def test_wrong_payout_calc_24(self, _custom_fee, _disable_personal_operation_fee_transfer_USD, _enable_currency):
        # Вывод отключенной валюты in_curr
        """ Currency in_curr off payout_create
        Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 4% for exchange and with personal fee 2% for exchange
        with common percent fee 5% for payout and with common absolute fee 5 USD for payout
        with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
        admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
        admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.merchant1.payout_calc(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'InactiveCurrency'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == 'UAH'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['exmo']['id'], is_active=False)

    def test_wrong_payout_calc_25(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
        """ Amount payout below the technical minimum in the pwcurrency table delegate
        Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.02), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'kuna', 'amount': '0.01',
                               'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # print(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooSmall'
        assert user1.resp_delegate['data']['reason'] == '0.01'
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_calc_26(self): # Вывод суммы ниже технического минимума по таблице pwcurrency
        """ Amount payout below the technical minimum in the pwcurrency table payout_create
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(2), tech_max=bl(3.36))
        user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'AmountTooSmall'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == '1.02'
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))

    def test_wrong_payout_calc_27(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout of the amount equal to the technical minimum in the pwcurrency table payout_create
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1.02), tech_max=bl(3.36))
        user1.merchant1.payout_calc(payway='payeer', amount='1.02', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['in_amount'] == '1.02'
        assert user1.merchant1.resp_payout_calc['out_amount'] == '1.02'
        assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_calc['account_amount'] == '1.02'
        assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0'
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(3.36))

    def test_wrong_payout_calc_28(self): # Вывод суммы выше технического максимума по таблице pwcurrency
        """ Payout above technical maximum in pwcurrency table payout_create
        Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['BTC'],
                      payway_id=admin.payway['btc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC', is_active=True,
                                     tech_min=bl(0.001), tech_max=bl(0.00463))
        user1.merchant1.payout_calc(payway='btc', amount='0.99999', out_curr='BTC')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'AmountTooBig'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == '0.99999'

    def test_wrong_payout_calc_29(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы выше технического максимума по таблице pwcurrency
        Payout above technical maximum in pwcurrency table delegate
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(1), tech_max=bl(1))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'cash_kiev', 'amount': '10',
                               'out_curr': 'USD', 'm_lid': str(user1.merchant1.lid)})
        # print(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooBig'
        assert user1.resp_delegate['data']['reason'] == '10'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['cash_kiev']['id'], is_active=False)

    def test_wrong_payout_calc_30(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы равной техническому максимуму по таблице pwcurrency
        Payout of the amount equal to the technical minimum in the pwcurrency table delegate
        Payout to cash_kiev  10 USD: USD to USD by OWNER with common percent fee 10% for payout
        and with common absolute fee 2 USD for payout with personal percent fee 5.5% for payout
        and with personal absolute fee 1 USD  payout."""
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=bl(0.055), add=bl(1), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.1), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(1), tech_max=bl(10))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'cash_kiev', 'amount': '10',
                               'out_curr': 'USD', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '11.55'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.55'
        assert user1.resp_delegate['orig_amount'] == '10'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_fee_amount'] == '1.55'
        admin.set_pwcurrency_min_max(payway=admin.payway['cash_kiev']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(1))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['cash_kiev']['id'], is_active=False)

    def test_wrong_payout_calc_31(self): # Вывод суммы ниже технического минимума по таблице exchange
        """ Amount payout below the technical minimum in the exchange table delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(20), tech_max=bl(40650.07))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
                               'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooSmall'
        assert user1.resp_delegate['data']['reason'] == '18.76'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40650.07))

    def test_wrong_payout_calc_32(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы ниже технического минимума по таблице exchange
        Amount payout below the technical minimum in the exchange table payout_create
        Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(250), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_calc(payway='webmoney', amount='8.33', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'AmountTooSmall'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == '238.55'
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_wrong_payout_calc_33(self): # Вывод суммы равной техническому минимуму по таблице exchange
        """ Payout of the amount equal to the technical minimum in the exchange table delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(18.76), tech_max=bl(40650.07))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
                               'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '18.76'
        assert user1.resp_delegate['in_amount'] == '18.76'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '50'
        assert user1.resp_delegate['out_amount'] == '50'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['rate'] == ['1', '2.6666']
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40650.07))

    def test_wrong_payout_calc_34(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы равной техническому минимуму по таблице exchange
        Payout of the amount equal to the technical minimum in the exchange table payout_create
        Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(238.55), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_calc(payway='webmoney', amount='8.33', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['in_amount'] == '238.55'
        assert user1.merchant1.resp_payout_calc['out_amount'] == '8.33'
        assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_calc['orig_amount'] == '8.33'
        assert user1.merchant1.resp_payout_calc['account_amount'] == '238.55'
        assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '0'
        assert user1.merchant1.resp_payout_calc['rate'] == ['28.637', '1']
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_wrong_payout_calc_35(self): # Вывод суммы выше технического максимума по таблице exchange
        """ Amount payout above the technical maximum in the exchange table delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(15))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'paymer', 'amount': '50',
                               'out_curr': 'RUB', 'in_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooBig'
        assert user1.resp_delegate['data']['reason'] == '18.76'
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40650.07))

    def test_wrong_payout_calc_36(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы выше технического максимума по таблице exchange
        Amount payout above the technical maximum in the exchange table payout_create
        Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
        admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
                                is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(10))
        user1.merchant1.payout_calc(payway='webmoney', amount='8.33', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'AmountTooBig'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == '238.55'
        admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
                                     is_active=False, tech_min=bl(1), tech_max=bl(0.97))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['webmoney']['id'], is_active=False)

    def test_wrong_payout_calc_37(self): # Вывод суммы равной техническому максимуму по таблице exchange
        """ Payout of the amount equal to the technical maximum in the exchange table delegate
        Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
        and without fee for exchange. """
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.1), tech_max=bl(18.76))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(50))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'contact': '380965781066'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '18.76'
        assert user1.resp_delegate['in_amount'] == '18.76'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['orig_amount'] == '50'
        assert user1.resp_delegate['out_amount'] == '50'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['rate'] == ['1', '2.6666']
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
        admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_wrong_payout_calc_38(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Вывод суммы равной техническому максимуму по таблице exchange
        Payout of the amount equal to the technical maximum in the exchange table payout_create
        Payout to exmo 15 USD: UAH to USD by MERCHANT with internal exchange
        and with common fee 4% for exchange and with personal fee 2% for exchange
        with common percent fee 5% for payout and with common absolute fee 5 USD for payout
        with personal percent fee 3.5% for payout and with personal absolute fee 2 USD  payout. """
        admin.set_wallet_amount(balance=bl(505), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(431.46))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=20000000)
        admin.set_fee(mult=bl(0.05), add=bl(5), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'],
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.035), add=bl(2), _min=0, _max=0, around='ceil', tp=10,
                      currency_id=admin.currency['USD'], payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(17.82))
        user1.merchant1.payout_calc(payway='exmo', amount='15', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['in_amount'] == '431.46'
        assert user1.merchant1.resp_payout_calc['orig_amount'] == '15'
        assert user1.merchant1.resp_payout_calc['out_amount'] == '15'
        assert user1.merchant1.resp_payout_calc['in_fee_amount'] == '72.78'
        assert user1.merchant1.resp_payout_calc['account_amount'] == '504.24'
        assert user1.merchant1.resp_payout_calc['out_fee_amount'] == '2.53'
        assert user1.merchant1.resp_payout_calc['rate'] == ['28.7639', '1']
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
                      payway_id=admin.payway['exmo']['id'], is_active=False)
        admin.set_rate_exchange(rate=28199900000, fee=40000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_wrong_payout_calc_39(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
        """ Payout with the amount parameter, the value of which is less than the out_curr currency grain delegate
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc', 'payway': 'visamc', 'amount': '0.009',
                               'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
        assert user1.resp_delegate['data']['reason'] == 'Invalid format 0.009 for UAH'
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_calc_40(self): # Вывод с параметром amount, значение которого меньше зерна валюты out_curr
        """ Payout with the amount parameter, the value of which is less than the out_curr currency grain payout_create
        Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        user1.merchant1.payout_calc(payway='payeer', amount='0.009', out_curr='RUB')
        # pprint.pprint(user1.merchant1.resp_payout_calc)
        assert user1.merchant1.resp_payout_calc['message'] == 'InvalidAmountFormat'
        assert user1.merchant1.resp_payout_calc['data']['reason'] == 'Invalid format 0.009 for RUB'

    def test_wrong_payout_45(self): # Запрос без out_curr (не передан)
        """ Request without out_curr delegate
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'm_lid': str(user1.merchant1.lid),
                               'payee': '4731185613244273'})
        pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        assert user1.resp_delegate['data']['reason'] == "method 'merchant.delegate' missing 1 argument: 'out_curr'"
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    def test_wrong_payout_calc_41(self): # Запрос без out_curr (не передан)
        """ Request without out_curr delegate
        Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'calc',  'payway': 'visamc', 'amount': '0.01',
                               'm_lid': str(user1.merchant1.lid)})
        pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        assert user1.resp_delegate['data']['reason'] == "method payout.calc' missing 1 argument: 'out_curr'"
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(98))

    # def test_wrong_payout_46(self): # Запрос без out_curr (не передан)
    #     """ Request without out_curr payout.create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #     assert loads(r.text)['error']['data']['reason'] == "method 'payout.create' missing 1 argument: 'out_curr'"
    #
    # def test_wrong_payout_47(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': None,
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidCurrency'
    #     assert user1.resp_delegate['data']['reason'] == None
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_48(self):# Запрос без out_curr (out_curr = None)
    #     """ Request out_curr = None
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'],
    #                             is_active=True)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr=None, payee='P1007817628')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidCurrency'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == None
    #
    # def test_wrong_payout_49(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273', 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     assert user1.resp_delegate['data']['reason'] == "method 'merchant.delegate' received a redundant argument 'par'"
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_50(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #     assert loads(r.text)['error']['data']['reason'] == \
    #            "method 'payout.create' received a redundant argument 'par'"
    #
    # def test_wrong_payout_51(self): # Запрос без externalid
    #     """ Request without externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'payway': 'visamc', 'amount': '0.01',
    #                            'out_curr': 'UAH', 'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidInputParams'
    #     assert user1.resp_delegate['data']['reason'] == "method 'merchant.delegate' missing 1 argument: 'externalid'"
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_52(self): # Запрос без externalid
    #     """ Request without externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidInputParams'
    #     assert loads(r.text)['error']['data']['reason'] == \
    #            "method 'payout.create' missing 1 argument: 'externalid'"
    #
    # def test_wrong_payout_53(self): # Запрос с существующим externalid
    #     """ Request with existing externalid delegate
    #     Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     tmp_ex_id = user1.ex_id()
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'Unique'
    #     assert user1.resp_delegate['data']['reason'] == 'Duplicated key for externalid'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_54(self): # Запрос с существующим externalid
    #     """ Request with existing externalid payout_create
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
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
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'Unique'
    #     assert loads(r.text)['error']['data']['reason'] == 'Duplicated key for externalid'
    #
    # def test_wrong_payout_55(self): # Запрос без подписи
    #     """ Unsigned request
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidHeaders'
    #     assert loads(r.text)['error']['data']['reason'] == 'Add x-signature to headers'
    #
    # def test_wrong_payout_56(self): # Запрос с невалидной подписью
    #     """ Request with invalid sign
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'payout.create',
    #             'params': {'amount': '1.02', 'payway': 'payeer', 'externalid': ex_id, 'payee': 'P14812343',
    #                        'out_curr': 'RUB'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # print(r.text)
    #     assert loads(r.text)['error']['message'] == 'InvalidSign'
    #     assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'
    #
    # def test_wrong_payout_57(self, _enable_exchange_operation_UAH_RUB):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ inactive exchange direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: UAH to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': 'R378259361317'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'UnavailExchange'
    #     assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange for UAH to RUB'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_58(self): # передан in_curr и отсутствует направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to paymer 50 RUB: USD to RUB by OWNER with internal exchange
    #     and without fee for exchange. """
    #     admin.set_wallet_amount(balance=bl(20), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='USD', out_currency='RUB')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(50))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'paymer', 'amount': '50', 'out_curr': 'RUB', 'in_curr': 'USD',
    #                            'm_lid': str(user1.merchant1.lid), 'contact': 'R378259361317'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'UnavailExchange'
    #     assert user1.resp_delegate['data']['reason'] == 'Unavailable exchange for USD to RUB'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(39.99))
    #
    # def test_wrong_payout_59(self, _custom_fee, _disable_personal_operation_fee_transfer_USD,
    #                          _enable_exchange_operation_UAH_USD):
    #     # передан in_curr и неактивно направление конвертации из in_curr в out_curr
    #     """ there is no conversion direction from in_curr to out_curr
    #     Payout to webmoney 8.33 USD: UAH to USD by MERCHANT with internal exchange
    #     and with common fee 3% for exchange and with personal fee 1.55 % for exchange. """
    #     admin.set_wallet_amount(balance=bl(250), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=30000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000), is_active=False)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=15500000)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='UAH', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'Unavailable exchange for UAH to USD'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
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
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'],
    #                             is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(10))
    #     user1.merchant1.payout_create(payway='webmoney', amount='8.33', out_curr='USD',
    #                                   in_curr='BCHABC', payee='Z123456789012')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'UnavailExchange'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == \
    #            'Unavailable exchange for BCHABC to USD'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['webmoney']['id'], is_out=True, currency='USD',
    #                                  is_active=False, tech_min=bl(1), tech_max=bl(0.97))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['USD'],
    #                   payway_id=admin.payway['webmoney']['id'], is_active=False)
    #
    # def test_wrong_payout_61(self): # указана неверная платежная система
    #     """ invalid payment system specified
    #     Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'test', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '5363542305527674'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidPayway'
    #     assert user1.resp_delegate['data']['reason'] == 'test is unknown'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_62(self): # указана неверная платежная система
    #     """ invalid payment system specified
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     user1.merchant1.payout_create(payway='test', amount='1.02', out_curr='RUB', payee='P14812343')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'test is unknown'
    #
    # def test_wrong_payout_63(self, _activate_kuna): # указана неактивная платежная система (is_active=False)
    #     """ inactive payment system specified (is_active = False)
    #     Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
    #                   payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(0.01), tech_max=bl(98))
    #     admin.set_payways(name='kuna', is_active=False)
    #     user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['message'] == 'InvalidPayway'
    #     assert user1.resp_delegate['data']['reason'] == 'kuna is inactive'
    #     admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(98))
    #
    # def test_wrong_payout_64(self, _activate_payeer): # указана неактивная платежная система (is_active=False)
    #     """ inactive payment system specified (is_active = False)
    #     Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
    #     admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
    #                   payway_id=admin.payway['payeer']['id'], is_active=False)
    #     admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    #     admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
    #                                  is_active=True, tech_min=bl(1), tech_max=bl(3.36))
    #     admin.set_payways(name='payeer', is_active=False)
    #     user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
    #     # pprint.pprint(user1.merchant1.resp_payout_create)
    #     assert user1.merchant1.resp_payout_create['error']['message'] == 'InvalidPayway'
    #     assert user1.merchant1.resp_payout_create['error']['data']['reason'] == 'payeer is inactive'


