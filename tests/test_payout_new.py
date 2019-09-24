import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import pprint
from users.merchant import Merchant


@pytest.mark.usefixtures('_payout_fee', '_personal_exchange_fee', '_payout_payway_fee')
class TestPayoutPayway:
    """ Output """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_payout_1_1(self): # Вывод суммы равной сумме на счету списания
                             # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(2.01), currency='UAH', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True, merchant_id=user1.pwmerchant_VISAMC.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.pwmerchant_VISAMC.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.pwmerchant_VISAMC.lid), 'payee': '4731185613244273'})
        print('lid', user1.pwmerchant_VISAMC.lid)
        pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.pwmerchant_VISAMC.balance(curr='UAH') == '0'

    def test_payout_1_3(self): # Вывод суммы равной сумме на счету списания
                             # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to visamc 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.pwmerchant_KUNA.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.pwmerchant_KUNA.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.pwmerchant_KUNA.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'visamc', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.pwmerchant_KUNA.lid), 'payee': '4731185613244273'})
        # print('lid', user1.merchant1.lid)
        # pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.pwmerchant_KUNA.balance(curr='UAH') == '0'

    def test_payout_2_1(self): # Вывод суммы равной техническому минимуму по таблице pwcurrency
        """ Payout to kuna 0.01 UAH: UAH to UAN by OWNER without fee for payout. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.pwmerchant_KUNA.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.pwmerchant_KUNA.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.pwmerchant_KUNA.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(0.01), tech_max=bl(98))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'kuna', 'amount': '0.01', 'out_curr': 'UAH',
                               'm_lid': str(user1.pwmerchant_KUNA.lid), 'payee': '5363542305527674'})
        print('lid', user1.merchant1.lid)
        pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.pwmerchant_KUNA.balance(curr='UAH') == '0'

    # @pytest.mark.skip
    def test_payout_3_1(self): # Перевод суммы равной сумме на счету списания
        """ Payout to payeer 1.02 RUB: RUB to RUB by MERCHANT without fee for payout. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.pwmerchant_PAYEER.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False, merchant_id=user1.pwmerchant_PAYEER.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['RUB'],
                      payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.pwmerchant_PAYEER.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB', is_active=True,
                                     tech_min=bl(1), tech_max=bl(3.36))
        user1.merchant1.payout_create(payway='payeer', amount='1.02', out_curr='RUB', payee='P14812343')
        # pprint.pprint(user1.merchant1.resp_payout_create)
        # time.sleep(2)
        # assert user1.pwmerchant_PAYEER.resp_payout_create['result']['status'] == 'done'
        assert user1.pwmerchant_PAYEER.resp_payout_create['result']['in_amount'] == '1.02'
        assert user1.pwmerchant_PAYEER.resp_payout_create['result']['out_amount'] == '1.02'
        assert user1.pwmerchant_PAYEER.resp_payout_create['result']['in_fee_amount'] == '0'
        assert user1.pwmerchant_PAYEER.resp_payout_create['result']['account_amount'] == '1.02'
        assert user1.pwmerchant_PAYEER.resp_payout_create['result']['out_fee_amount'] == '0'
        assert user1.pwmerchant_PAYEER.balance(curr='RUB') == '0'

    def test_payout_4_1(self): # Вывод суммы равной техническому максимуму по таблице pwcurrency
        """ Payout to btc 0.99999 BTC: BTC to BTC by MERCHANT without fee for payout. """
        merchants = admin.get_merchants(owner_id=user1.id, payway_id=admin.payway['btc']['id'])
        user1.merchant1 = Merchant(next(merchants))
        # print('lid', user1.merchant1.lid)
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

    def test_payout_5_1(self):
        """ Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
        merchants = admin.get_merchants(owner_id=user1.id, payway_id=admin.payway['privat24']['id'])
        user1.merchant1 = Merchant(next(merchants))
        # print('lid', user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.15), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True, is_bound=True)
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
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)

    def test_payout_5_3(self):
        """ Payout to privat24 10 UAH: UAH to UAN by OWNER with common percent fee 15% for payout. """
        merchants = admin.get_merchants(owner_id=user1.id, payway_id=admin.payway['kuna']['id'])
        user1.merchant1 = Merchant(next(merchants))
        # print('lid', user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=0, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=pers(15), add=0, _min=0, _max=0, around='ceil', tp=0, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=pers(0), add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['privat24']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(100))
        user1.delegate(params={'merch_model': 'payout', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'payway': 'privat24', 'amount': '10', 'out_curr': 'UAH',
                               'm_lid': str(user1.merchant1.lid), 'payee': '4731185613244273'})
        pprint.pprint(user1.resp_delegate)
        # assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['account_amount'] == '11.5'
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_fee_amount'] == '1.5'
        assert user1.resp_delegate['out_amount'] == '10'
        assert user1.resp_delegate['out_fee_amount'] == '1.5'
        assert user1.resp_delegate['reqdata']['amount'] == '10'
        assert user1.merchant1.balance(curr='UAH') == '0'
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=0, currency_id=admin.currency['UAH'],
        #               payway_id=admin.payway['privat24']['id'], is_active=False)
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=10, currency_id=admin.currency['UAH'],
        #               payway_id=admin.payway['kuna']['id'], is_active=False)

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

    # @pytest.mark.skip
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
        admin.set_payways(name='cash_kiev')
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
