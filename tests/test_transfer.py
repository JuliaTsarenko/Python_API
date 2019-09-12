import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint


@pytest.mark.usefixtures('_transfer_fee', '_personal_exchange_fee')
class TestTransfer:
    """ Create transfer. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    # def test_transfer_1(self): # Перевод суммы равной сумме на счету списания
    #     # Перевод суммы равной техническому минимуму по таблице currency
    #     # Запрос без in_curr
    #     """  Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     # print('\n', 'balance(UAH)', user1.merchant1.resp_balance['UAH'])
    #
    # def test_transfer_2(self): # Перевод суммы равной сумме на счету списания
    #     # Перевод суммы равной техническому минимуму по таблице currency
    #     # Запрос без in_curr
    #     """  Transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # print("user1.merchant1.resp_transfer")
    #     # pprint.pprint(user1.merchant1.resp_transfer)
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='USD') == '0'
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_3(self): # Перевод суммы равной сумме на счету списания
    #     """ Transfer 0.00999 BTC the same owner: BTC to BTC by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.00999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='0.00999', out_curr='BTC')
    #     # print("user1.merchant1.resp_transfer")
    #     # pprint.pprint(user1.merchant1.resp_transfer)
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='BTC') == '0'
    #
    # def test_transfer_4(self):
    #     """ Transfer 5 USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
    #     and with common absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
    #                            'amount': '5', 'out_curr': 'USD'})
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '5'
    #     assert user1.resp_delegate['out_amount'] == '5'
    #     assert user1.resp_delegate['in_fee_amount'] == '0.55'
    #     assert user1.resp_delegate['reqdata']['amount'] == '5'
    #     assert user1.resp_delegate['out_fee_amount'] == '0.55'
    #     assert user1.merchant1.balance(curr='USD') == '4.45'
    #
    # def test_transfer_5(self):
    #     """ Transfer 0.003 BTC to another owner: BTC to BTC by MERCHANT with common absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=100000, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.003', out_curr='BTC')
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '0.003'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.003'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0.0001'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '0.0031'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.0001'
    #     assert user1.merchant1.balance(curr='BTC') == '0.0009'
    #
    # def test_transfer_6(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Transfer 5 USD the same owner: USD to USD by MERCHANT with common percent fee 2% for transfer
    #     and with common absolute fee 1 USD for transfer with personal percent fee 1% for transfer
    #     and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.02), add=bl(1), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0.55'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5.55'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.55'
    #     assert user1.merchant1.balance(curr='USD') == '4.45'
    #
    # def test_transfer_7(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Transfer 0.003 BTC to another owner: BTC to BTC by OWNER with common percent fee 5% for transfer
    #     and with common absolute fee 0.0002 BTC for transfer with personal percent fee 3% for transfer
    #     and with personal absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=30000000, add=100000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=50000000, add=200000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'],  is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
    #                            'amount': '0.003', 'out_curr': 'BTC'})
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '0.003'
    #     assert user1.resp_delegate['out_amount'] == '0.003'
    #     assert user1.resp_delegate['in_fee_amount'] == '0.00019'
    #     assert user1.resp_delegate['reqdata']['amount'] == '0.003'
    #     assert user1.resp_delegate['out_fee_amount'] == '0.00019'
    #     assert user1.merchant1.balance(curr='BTC') == '0.00081'
    #
    # def test_transfer_8(self):
    #     """ Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '1'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['rate'] == ['28.4819', '1']
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'new'
    #     assert user1.merchant1.balance(curr='UAH') == '1.51'
    #     # user1.merchant1.order_get(o_lid=user1.merchant1.resp_transfer_create['id'])
    #     # time.sleep(2)
    #     # assert user1.merchant2.balance(curr='USD') == '2'
    #
    # def test_transfer_9(self):
    #     """ Transfer 0.43 BTC the same owner: USD to BTC by OWNER with internal exchange
    #     and with common percent fee 0.05% for exchange. """
    #     admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=500000, in_currency='USD', out_currency='BTC',
    #                             tech_min=bl(1), tech_max=bl(2000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.43', 'in_curr': 'USD', 'out_curr': 'BTC'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_amount'] == '1540.46'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['out_amount'] == '0.43'
    #     assert user1.resp_delegate['rate'] == ['3582.44443', '1']
    #     assert user1.resp_delegate['reqdata']['amount'] == '0.43'
    #     # user1.merchant1.balance(curr='USD')
    #     # assert user1.merchant1.resp_balance['USD'] == '59.54'
    #     # time.sleep(2)
    #     # user1.merchant2.balance(curr='BTC')
    #     # assert user1.merchant2.resp_balance['BTC'] == '1.43'
    #
    # def test_transfer_10(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
    #     and with common fee 5% for exchange and with personal fee 3.5 % for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
    #     admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
    #                            'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
    #     assert user1.resp_delegate['account_amount'] == '322.81'
    #     assert user1.resp_delegate['in_amount'] == '293.33'
    #     assert user1.resp_delegate['in_fee_amount'] == '29.48'
    #     assert user1.resp_delegate['out_amount'] == '10.05'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.01'
    #     assert user1.resp_delegate['rate'] == ['29.1869', '1']
    #     assert user1.resp_delegate['reqdata']['amount'] == '10.05'
    #     assert user1.merchant1.balance(curr='UAH') == '77.19'
    #     # time.sleep(2)
    #     # assert user2.merchant1.balance(curr='USD') == '20.05'
    #     # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=False)
    #
    # def test_transfer_11(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Transfer 0.43 BTC the same owner: USD to BTC by MERCHANT  with internal exchange
    #     and with common fee 1% for exchange and with personal fee 0.05% for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 0.01 BTC for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.005 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(1800), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=10000000, in_currency='USD', out_currency='BTC')
    #     admin.set_rate_exchange(rate=3580654100000, fee=0, in_currency='USD', out_currency='BTC')
    #     admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_fee(mult=100000000, add=10000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True)
    #     admin.set_fee(mult=50000000, add=5000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='0.43', in_curr='USD', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '1540.46'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.43'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '94.94'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '1635.4'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.0265'
    #     assert user1.merchant1.resp_transfer_create['result']['rate'] == ['3582.44443', '1']
    #     assert user1.merchant1.resp_transfer_create['result']['reqdata']['amount'] == '0.43'
    #     # user1.merchant1.balance(curr='USD')
    #     # assert user1.merchant1.resp_balance['USD'] == '164.6'
    #     # time.sleep(2)
    #     # user1.merchant2.balance(curr='BTC')
    #     # assert user1.merchant2.resp_balance['BTC'] == '1.43'
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #
    # @pytest.mark.skip
    # def test_transfer_12(self, _disable_2type): # Перевод с включенным двухфакторным подтверждением без конвертации
    #                                             # и без комисии за операцию перевода
    #     """ Transfer twostepauth 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.set_2type(tp=0)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     admin.set_fee(tp=30, currency_id='UAH', is_active=False, merchant_id=user1.merchant1.lid)
    #
    # @pytest.mark.skip
    # def test_transfer_13(self, _disable_2type): # Перевод с включенным двухфакторным подтверждением без конвертации
    #                                             # и без комисии за операцию перевода
    #     """Transfer twostepauth 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=True)
    #     user1.set_2type(tp=0)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
    #     # print("user1.merchant1.resp_transfer")
    #     # pprint.pprint(user1.merchant1.resp_transfer)
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.rbalance(curr='USD') == '0'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_14(self, _disable_st_value): # Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     # print(admin.resp_st_value)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32036
    #     assert user1.resp_delegate['message'] == 'EStateOutPayUnavailable'
    #     assert user1.resp_delegate['data']['reason'] == 'Out pay is blocked'
    #
    # def test_transfer_15(self, _disable_st_value): # Выплаты во всей системе заблокированы
    #     """ Payments in the entire system are blocked
    #     Transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_st_value(name='out_is_blocked', value=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32036
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateOutPayUnavailable'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Out pay is blocked'
    #
    # def test_transfer_16(self, _enable_merchant_payout_allowed):
    #     # Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32036
    #     assert user1.resp_delegate['message'] == 'EStateOutPayUnavailable'
    #     assert user1.resp_delegate['data']['reason'] == 'Out pay is blocked'
    #
    # def test_transfer_17(self, _enable_merchant_payout_allowed): # Вывод для получателя заблокирован (payout_allowed)
    #     """ Recipient payout is blocked
    #     Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=10000000, currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                    is_active=True, merchant_id=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user1.merchant2.id, payout_allowed=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='UAH') == '0'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.lid)
    #
    # def test_transfer_18(self, _enable_merchant_payout_allowed):
    #     # Вывод для данного пользователя заблокирован (payout_allowed)
    #     """ Sender's payout is blocked
    #     Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32036
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateOutPayUnavailable'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Out pay is blocked'
    #
    # def test_transfer_19(self, _enable_merchant_payout_allowed): # Вывод для получателя заблокирован (payout_allowed)
    #     """ Recipient payout is blocked
    #     Transfer 5 USD to non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user2.merchant1.lid, payout_allowed=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='USD') == '0'
    #     admin.set_merchant(lid=user1.merchant1.id, is_active=True)
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_20(self): # Перевод суммы больше чем на счету списания
    #     """ Transfer 0.02 UAH with 0.01 UAH in the wallet the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.02', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32056
    #     assert user1.resp_delegate['message'] == 'EStateInsufficientFunds'
    #     assert user1.resp_delegate['data']['reason'] == 'Balance 0.01 less then amount 0.02'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_21(self): # Перевод суммы больше чем на счету списания
    #     """ Transfer 10 USD with 5 USD in the wallet to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='10', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32056
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateInsufficientFunds'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Balance 5 less then amount 10'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_22(self): # Перевод суммы не существующему мерчанту
    #     """ Transfer 0.01 UAH to non-existent merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': '11111',
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32090
    #     assert user1.resp_delegate['message'] == 'EParamNotFound'
    #     assert user1.resp_delegate['data']['field'] == 'tgt'
    #     assert user1.resp_delegate['data']['reason'] == 'Not found'
    #
    # def test_transfer_23(self): # Перевод суммы не существующему мерчанту
    #     """ Transfer 5 USD to non-existent merchant to another owner: USD to USD by MERCHANT
    #     without fee for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=False)
    #     user1.merchant1.transfer_create(tgt='11111', amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32090
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamNotFound'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'tgt'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Not found'
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_24(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Transfer 0.01 UAH by non-active merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'merchant'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #
    # def test_transfer_25(self, _enable_merchant_is_active): # Перевод суммы не активному мерчанту
    #     """ Transfer 0.01 UAH to non-active merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=False)
    #     admin.set_merchant(lid=user1.merchant2.lid, is_active=False)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'tgt'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #
    # def test_transfer_26(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user2.merchant1.lid, is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32015
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamMerchantInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'tgt'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Improper merchant'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_26_1(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32015
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamMerchantInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'x-merchant'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Merchant inactive'
    #
    # def test_transfer_27(self, _enable_merchant_is_active): # Перевод суммы не активному мерчанту
    #     """ Transfer 5 USD to non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user2.merchant1.lid, is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32015
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamMerchantInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'tgt'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Improper merchant'
    #
    # def test_transfer_28(self): # Перевод без суммы (amount = None)
    #     """ amount = None  delegate """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': None, 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_29(self): # Перевод без суммы (amount = None)
    #     """ amount = None  transfer """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount=None, out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_30(self): # Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  delegate """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': 'Test', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be a Number'
    #
    # def test_transfer_31(self): # Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  transfer """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='Test', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Should be a Number'
    #
    # def test_transfer_32(self): # Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  delegate """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.111', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #
    # def test_transfer_33(self): # Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  transfer """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.111', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32082
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #
    # def test_transfer_34(self): # Перевод по несуществующей валюте out_curr
    #     """ Transfer for non-existent currency out_curr """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #
    # def test_transfer_35(self): # Перевод по несуществующей валюте out_curr
    #     """ Transfer for non-existent currency out_curr """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32014
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Invalid currency name'
    #
    # def test_transfer_36(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_transfer_37(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_transfer_38(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_transfer_39(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_transfer_40(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #
    # def test_transfer_41(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32014
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Invalid currency name'
    #
    # def test_transfer_42(self, _enable_currency): # Перевод по неактивной валюте in_curr
    #     """ Currency in_curr off """
    #     admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_transfer_43(self, _enable_currency): # Перевод по неактивной валюте in_curr
    #     """ Currency in_curr off """
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_transfer_44(self, _enable_currency): # Валюта in_curr выкл
    #     """ Currency in_curr off """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'USD', 'in_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #
    # def test_transfer_45(self, _enable_currency): # Валюта in_curr выкл
    #     """ Currency in_curr off """
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Inactive'
    #
    # def test_transfer_46(self): # Перевод суммы ниже технического минимума по таблице currency
    #     """ Amount transfer below the technical minimum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.02), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32074
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
    #     assert user1.resp_delegate['data']['value'] == '0.01'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_47(self): # Перевод суммы ниже технического минимума по таблице currency
    #     """ Amount transfer below the technical minimum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(10), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32074
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Amount is too small'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_48(self): # Перевод суммы выше технического максимума по таблице currency
    #     """ Transfer of the amount above the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '5', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32073
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
    #     assert user1.resp_delegate['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_49(self): # Перевод суммы выше технического максимума по таблице currency
    #     """ Transfer of the amount above the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32073
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountTooBig'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Amount is too big'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_50(self): # Перевод суммы равной техническому максимуму по таблице currency
    #     """ Transfer of the amount equal to the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant2.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '5', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['status'] == 'done'
    #     assert user1.resp_delegate['in_amount'] == '5'
    #     assert user1.resp_delegate['out_amount'] == '5'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['account_amount'] == '5'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='UAH') == '5'
    #     time.sleep(2)
    #     assert user1.merchant2.balance(curr='UAH') == '15'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_51(self): # Перевод суммы равной техническому максимуму по таблице currency
    #     """ Transfer of the amount equal to the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.balance(curr='USD') == '5'
    #     time.sleep(2)
    #     assert user2.merchant1.balance(curr='USD') == '15'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_52(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Transfer with the amount parameter, the value of which is less than the out_curr currency grain delegate """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.009', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #
    # def test_transfer_53(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Transfer with the amount parameter, the value of which is less than the out_curr currency grain transfer_create """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.009', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32082
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'amount'
    #
    # def test_transfer_54(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid), 'amount': '0.009'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_55(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '0.009', 'in_curr': None, 'tgt': str(user2.merchant1.lid), 'externalid': ex_id},
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
    # def test_transfer_56(self): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid), 'amount': '0.009',
    #                            'out_curr': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_57(self): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.009', out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32002
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_58(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid), 'amount': '0.01',
    #                            'out_curr': 'UAH', 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'par'
    #     assert user1.resp_delegate['data']['reason'] == 'Should not be provided'
    #
    # def test_transfer_59(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid), 'externalid': ex_id, 'par': '123'},
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
    # def test_transfer_60(self): # Запрос без externalid
    #     """ Request without externalid delegate """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'out_curr': 'UAH',
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid), 'amount': '0.01'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'externalid'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_61(self): # Запрос без externalid
    #     """ Request without externalid transfer.create """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid)},
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
    # def test_transfer_62(self): # Запрос с существующим externalid
    #     """ Request with existing externalid delegate """
    #     admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     tmp_ex_id=user1.ex_id()
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': tmp_ex_id,
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32091
    #     assert user1.resp_delegate['message'] == 'EParamUnique'
    #     assert user1.resp_delegate['data']['field'] == 'externalid'
    #     assert user1.resp_delegate['data']['reason'] == 'Such externalid already present'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_63(self): # Запрос с существующим externalid
    #     """ Request with existing externalid transfer.create """
    #     admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
    #                        'externalid': ex_id},
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
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32091
    #     assert loads(r.text)['error']['message'] == 'EParamUnique'
    #     assert loads(r.text)['error']['data']['field'] == 'externalid'
    #     assert loads(r.text)['error']['data']['reason'] == 'Such externalid already present'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_64(self): # Запрос без подписи
    #     """ Unsigned request """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
    #                        'externalid': ex_id},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32012
    #     assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'x-signature'
    #     assert loads(r.text)['error']['data']['reason'] == 'Not present'
    #
    # def test_transfer_65(self): # Запрос с невалидной подписью
    #     """ Request with invalid sign """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
    #                        'externalid': ex_id},
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
    # def test_transfer_66(self): # Перевод суммы не существующим мерчантом
    #     """ Transfer of non-existent merchant """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': '11111', 'tgt': str(user1.merchant2.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32090
    #     assert user1.resp_delegate['message'] == 'EParamNotFound'
    #     assert user1.resp_delegate['data']['field'] == 'merchant'
    #     assert user1.resp_delegate['data']['reason'] == 'Not found'
    #
    # def test_transfer_67(self): # Запрос tgt=None
    #     """ tgt=None """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': None,
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'tgt'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_68(self): # Запрос tgt=None
    #     """ tgt=None """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_create(tgt=None, amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32003
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamType'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'tgt'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Should be an Integer'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_69(self): # Запрос без tgt
    #     """ Request without tgt """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'tgt'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_70(self): # Запрос без tgt
    #     """ Request without tgt """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'externalid': ex_id},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                         headers={'x-merchant': str(user1.merchant1.lid),
    #                                 'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
    #                                 'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32002
    #     assert loads(r.text)['error']['message'] == 'EParamInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'tgt'
    #     assert loads(r.text)['error']['data']['reason'] == 'Should be provided'
    #
    # def test_transfer_71(self): # Перевод суммы ниже технического минимума по таблице exchange
    #     """ Amount transfer below the technical minimum in the exchange table transfer_create
    #     Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(30), tech_max=bl(10000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32074
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'in_amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Amount is too small'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['value'] == '28.49'
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_transfer_72(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Перевод суммы ниже технического минимума по таблице exchange
    #     Amount transfer below the technical minimum in the exchange table delegate
    #     Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
    #     and with common fee 5% for exchange and with personal fee 3.5 % for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(400), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
    #     admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
    #                            'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32074
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
    #     assert user1.resp_delegate['data']['field'] == 'in_amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
    #     assert user1.resp_delegate['data']['value'] == '293.33'
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_transfer_73(self): # Перевод суммы выше технического максимума по таблице exchange
    #     """ Amount transfer above the technical maximum in the exchange table transfer_create
    #     Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(20))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['error']['code'] == -32073
    #     assert user1.merchant1.resp_transfer_create['error']['message'] == 'EParamAmountTooBig'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['field'] == 'in_amount'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['reason'] == 'Amount is too big'
    #     assert user1.merchant1.resp_transfer_create['error']['data']['value'] == '28.49'
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_transfer_74(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Перевод суммы выше технического максимума по таблице exchange
    #     Amount transfer above the technical maximum in the exchange table delegate
    #     Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
    #     and with common fee 5% for exchange and with personal fee 3.5 % for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(200))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
    #     admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
    #                            'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
    #                            'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32073
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
    #     assert user1.resp_delegate['data']['field'] == 'in_amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
    #     assert user1.resp_delegate['data']['value'] == '293.33'
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #
    # def test_transfer_75(self): # Перевод суммы равной техническому минимуму по таблице exchange
    #     """ Transfer of the amount equal to the technical maximum in the exchange table transfer_create
    #     Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(28.49), tech_max=bl(10000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_create)
    #     assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '1'
    #     assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_create['result']['rate'] == ['28.4819', '1']
    #     assert user1.merchant1.resp_transfer_create['result']['status'] == 'new'
    #     assert user1.merchant1.balance(curr='UAH') == '1.51'
    #     # user1.merchant1.order_get(o_lid=user1.merchant1.resp_transfer_create['id'])
    #     # time.sleep(2)
    #     # assert user1.merchant2.balance(curr='USD') == '2'
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_76(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы равной техническому минимуму по таблице exchange
        Transfer of the amount equal to the technical maximum in the exchange table delegate
        Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(293.33), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '322.81'
        assert user1.resp_delegate['in_amount'] == '293.33'
        assert user1.resp_delegate['in_fee_amount'] == '29.48'
        assert user1.resp_delegate['out_amount'] == '10.05'
        assert user1.resp_delegate['out_fee_amount'] == '1.01'
        assert user1.resp_delegate['rate'] == ['29.1869', '1']
        assert user1.resp_delegate['reqdata']['amount'] == '10.05'
        assert user1.merchant1.balance(curr='UAH') == '77.19'
        # time.sleep(2)
        # assert user2.merchant1.balance(curr='USD') == '20.05'
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
        # is_active=False)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_77(self): # Перевод суммы равной техническому максимуму по таблице exchange
        """ Transfer of the amount equal to the technical maximum in the exchange table transfer_create
        Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(28.49))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '1'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['rate'] == ['28.4819', '1']
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'new'
        assert user1.merchant1.balance(curr='UAH') == '1.51'
        # user1.merchant1.order_get(o_lid=user1.merchant1.resp_transfer_create['id'])
        # time.sleep(2)
        # assert user1.merchant2.balance(curr='USD') == '2'
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_78(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы равной техническому максимуму по таблице exchange
        Transfer of the amount equal to the technical maximum in the exchange table delegate
        Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(293.33))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': str(user1.merchant1.lid), 'tgt': str(user2.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '322.81'
        assert user1.resp_delegate['in_amount'] == '293.33'
        assert user1.resp_delegate['in_fee_amount'] == '29.48'
        assert user1.resp_delegate['out_amount'] == '10.05'
        assert user1.resp_delegate['out_fee_amount'] == '1.01'
        assert user1.resp_delegate['rate'] == ['29.1869', '1']
        assert user1.resp_delegate['reqdata']['amount'] == '10.05'
        assert user1.merchant1.balance(curr='UAH') == '77.19'
        # time.sleep(2)
        # assert user2.merchant1.balance(curr='USD') == '20.05'
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
        # is_active=False)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

@pytest.mark.usefixtures('_transfer_fee', '_personal_exchange_fee')
class TestParams:
    """ Testing transfer params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    # def test_params_1(self):
    #     """ Getting params for transfer UAH the same owner: UAH to UAN by OWNER without fee for transfer"""
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.01'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '3000'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.01'
    #     assert user1.resp_delegate['out_curr'] == 'UAH'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': None, 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #
    # def test_params_2(self):
    #     """ Getting params for transfer USD to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #     is_active=False)
    #     user1.merchant1.transfer_params(out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '5'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == False
    #     assert user1.merchant1.resp_transfer_params['max'] == '3000'
    #     assert user1.merchant1.resp_transfer_params['min'] == '5'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '5'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': None, 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']
    #
    # def test_params_3(self):
    #     """ Getting params for transfer BTC the same owner: BTC to BTC by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.00999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'], is_active=False)
    #     user1.merchant1.transfer_params(out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'BTC'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == False
    #     assert user1.merchant1.resp_transfer_params['max'] == '3'
    #     assert user1.merchant1.resp_transfer_params['min'] == '0.000001'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '0.000001'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'BTC'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': None, 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']
    #
    # def test_params_4(self):
    #     """ Getting params for transfer USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
    #     and with common absolute fee 0.5 USD for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #     currency_id=admin.currency['USD'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid), 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'USD'
    #     assert user1.resp_delegate['in_curr_balance'] == '10'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '3000'
    #     assert user1.resp_delegate['min'] == '5'
    #     assert user1.resp_delegate['min_balance_limit'] == '5.55'
    #     assert user1.resp_delegate['out_curr'] == 'USD'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0.5', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.01'}
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #
    # def test_params_5(self):
    #     """ Getting params for transfer BTC to another owner: BTC to BTC by MERCHANT
    #     with common absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=100000, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'], is_active=True)
    #     user1.merchant1.transfer_params(out_curr='BTC')
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'BTC'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '0.004'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == False
    #     assert user1.merchant1.resp_transfer_params['max'] == '3'
    #     assert user1.merchant1.resp_transfer_params['min'] == '0.000001'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '0.000101'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'BTC'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == \
    #            {'add': '0.0001', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']
    #
    # def test_params_6(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for transfer USD the same owner: USD to USD by MERCHANT
    #     with common percent fee 2% for transfer and with common absolute fee 1 USD for transfer
    #     with personal percent fee 1% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.02), add=bl(1), _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=True)
    #     user1.merchant1.transfer_params(out_curr='USD')
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '10'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == False
    #     assert user1.merchant1.resp_transfer_params['max'] == '3000'
    #     assert user1.merchant1.resp_transfer_params['min'] == '5'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '5.55'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == \
    #            {'add': '0.5', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.01'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']
    #
    # def test_params_7(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Getting params for transfer BTC to another owner: BTC to BTC by OWNER
    #     with common percent fee 5% for transfer and with common absolute fee 0.0002 BTC for transfer
    #     with personal percent fee 3% for transfer and with personal absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=30000000, add=100000, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=50000000, add=200000, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'BTC'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['in_curr'] == 'BTC'
    #     assert user1.resp_delegate['in_curr_balance'] == '0.004'
    #     assert user1.resp_delegate['is_convert'] == False
    #     assert user1.resp_delegate['max'] == '3'
    #     assert user1.resp_delegate['min'] == '0.000001'
    #     assert user1.resp_delegate['min_balance_limit'] == '0.00010103'
    #     assert user1.resp_delegate['out_curr'] == 'BTC'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0.0001', 'max': '0', 'method': 'ceil', 'min': '0', 'mult': '0.03'}
    #     assert user1.resp_delegate['rate'] == ['1', '1']
    #
    # def test_params_8(self):
    #     """ Getting params for transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000), extfee=bl(0))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_params(in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['from_in_curr_balance'] == '1.05'
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'UAH'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '30'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == True
    #     assert user1.merchant1.resp_transfer_params['max'] == '105.33'
    #     assert user1.merchant1.resp_transfer_params['min'] == '0.01'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '2.85'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == \
    #            {'add': '0', 'max': '0', 'method': None, 'min': '0', 'mult': '0'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['28.4819', '1']
    #
    # def test_params_9(self):
    #     """ Getting params for transfer BTC the same owner: USD to BTC by OWNER with internal exchange
    #     and with common percent fee 0.05% for exchange. """
    #     admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=500000, in_currency='USD', out_currency='BTC',
    #                             tech_min=bl(1), tech_max=bl(2000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'in_curr': 'USD', 'out_curr': 'BTC'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['from_in_curr_balance'] == '0.44662241'
    #     assert user1.resp_delegate['in_curr'] == 'USD'
    #     assert user1.resp_delegate['in_curr_balance'] == '1600'
    #     assert user1.resp_delegate['is_convert'] == True
    #     assert user1.resp_delegate['max'] == '0.00083741'
    #     assert user1.resp_delegate['min'] == '0.00027914'
    #     assert user1.resp_delegate['min_balance_limit'] == '3582.44443'
    #     assert user1.resp_delegate['out_curr'] == 'BTC'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0', 'max': '0', 'method': None, 'min': '0', 'mult': '0'}
    #     assert user1.resp_delegate['rate'] == ['3582.44443', '1']
    #
    # def test_params_10(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Getting params for transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
    #     and with common fee 5% for exchange and with personal fee 3.5 % for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.05), in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=bl(0.035))
    #     admin.set_fee(mult=bl(0.1), add=bl(1), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     admin.set_fee(mult=bl(0.05), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'in_curr': 'UAH', 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['from_in_curr_balance'] == '13.7'
    #     assert user1.resp_delegate['in_curr'] == 'UAH'
    #     assert user1.resp_delegate['in_curr_balance'] == '400'
    #     assert user1.resp_delegate['is_convert'] == True
    #     assert user1.resp_delegate['max'] == '102.78'
    #     assert user1.resp_delegate['min'] == '0.01'
    #     assert user1.resp_delegate['min_balance_limit'] == '15.18'
    #     assert user1.resp_delegate['out_curr'] == 'USD'
    #     assert user1.resp_delegate['out_fee'] == {'add': '0.5',
    #                                              'max': '0',
    #                                              'method': 'ceil',
    #                                              'min': '0',
    #                                              'mult': '0.05'}
    #     assert user1.resp_delegate['rate'] == ['29.1869', '1']
    #
    # def test_params_11(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Getting params for transfer 0.43 BTC the same owner: USD to BTC by MERCHANT  with internal exchange
    #     and with common fee 1% for exchange and with personal fee 0.05% for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 0.01 BTC for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.005 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(1800), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=10000000, in_currency='USD', out_currency='BTC')
    #     admin.set_rate_exchange(rate=3580654100000, fee=0, in_currency='USD', out_currency='BTC')
    #     admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_fee(mult=100000000, add=10000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True)
    #     admin.set_fee(mult=50000000, add=5000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.merchant1.transfer_params(in_curr='USD', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['from_in_curr_balance'] == '0.50245022'
    #     assert user1.merchant1.resp_transfer_params['in_curr'] == 'USD'
    #     assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '1800'
    #     assert user1.merchant1.resp_transfer_params['is_convert'] == True
    #     assert user1.merchant1.resp_transfer_params['max'] == '0.00083741'
    #     assert user1.merchant1.resp_transfer_params['min'] == '0.00027914'
    #     assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '3582.44443'
    #     assert user1.merchant1.resp_transfer_params['out_curr'] == 'BTC'
    #     assert user1.merchant1.resp_transfer_params['out_fee'] == {'add': '0.005',
    #                                                              'max': '0',
    #                                                              'method': 'ceil',
    #                                                              'min': '0',
    #                                                              'mult': '0.05'}
    #     assert user1.merchant1.resp_transfer_params['rate'] == ['3582.44443', '1']
    #
    # def test_params_12(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Getting params for transfer 0.01 UAH by non-active merchant the same owner:
    #     UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'merchant'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_13(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Getting params for transfer 5 USD by non-active merchant to another owner:
    #     USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.merchant1.transfer_params(out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32031
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EStateMerchantInactive'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'x-merchant'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Merchant inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_params_14(self): # Перевод по несуществующей валюте out_curr
    #     """ Getting params for transfer for non-existent currency out_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_15(self): # Перевод по несуществующей валюте out_curr
    #     """ Getting params for transfer for non-existent currency out_curr """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_params(out_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32014
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_16(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_17(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_params(out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_params_18(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_19(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_params(out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_params_20(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH', 'in_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_21(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_params(out_curr='USD', in_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32014
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_params_22(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH', 'in_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_23(self, _enable_currency): # Перевод по неактивной валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_params(out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_params_24(self, _enable_currency): # Валюта in_curr выкл
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'USD', 'in_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_25(self, _enable_currency): # Валюта in_curr выкл
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_params(out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32033
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_26(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid)})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_27(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.params',
    #             'params': {'in_curr': None},
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
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_28(self): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_params_29(self, _enable_currency): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     user1.merchant1.transfer_params(out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_transfer_params)
    #     assert user1.merchant1.resp_transfer_params['error']['code'] == -32002
    #     assert user1.merchant1.resp_transfer_params['error']['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_params['error']['data']['reason'] == 'Should be provided'
    #
    # def test_params_30(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': str(user1.merchant1.lid),
    #                            'out_curr': 'UAH', 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'par'
    #     assert user1.resp_delegate['data']['reason'] == 'Should not be provided'
    #
    # def test_params_31(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.params',
    #             'params': {'out_curr': 'USD', 'par': '123'},
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
    # def test_params_32(self): # Запрос без подписи
    #     """ Unsigned request """
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.params',
    #             'params': {'out_curr': 'USD'},
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

    def test_params_33(self): # Запрос с невалидной подписью
        """ Request with invalid sign """
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.params',
                'params': {'out_curr': 'USD'},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # print(r.text)
        assert loads(r.text)['error']['code'] == -32010
        assert loads(r.text)['error']['message'] == 'EParamSignInvalid'
        assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'

    def test_params_34(self): # Перевод суммы не существующим мерчантом
        """ Transfer of non-existent merchant """
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': '11111',
                               'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32090
        assert user1.resp_delegate['message'] == 'EParamNotFound'
        assert user1.resp_delegate['data']['field'] == 'merchant'
        assert user1.resp_delegate['data']['reason'] == 'Not found'

class TestTransferGet:
    """ Testing transfer get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_get_transfer_1(self):
        """  Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': str(user1.merchant1.lid), 'tgt': str(user1.merchant2.lid),
                               'amount': '0.01', 'out_curr': 'UAH'})
        # print('o_lid', user1.resp_delegate['lid'])
        # pprint.pprint(user1.resp_delegate)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'get', 'o_lid': str(user1.resp_delegate['lid']),
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
        assert user1.resp_delegate['payway_name'] == None
        assert user1.resp_delegate['rate'] == None
        assert user1.resp_delegate['ref'] == None
        assert user1.resp_delegate['renumeration'] == '0'
        assert user1.resp_delegate['reqdata']['amount'] == '0.01'
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['tp'] == 'transfer'
        assert user1.resp_delegate['userdata'] == {}
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH', is_active=True,
                                     tech_min=bl(1), tech_max=bl(98))

    def test_get_transfer_2(self):
        """  Transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # print("user1.merchant1.resp_transfer")
        # pprint.pprint(user1.merchant1.resp_transfer)
        user1.merchant1.transfer_get(o_lid=user1.merchant1.resp_transfer_create['result']['lid'])
        # pprint.pprint(user1.merchant1.resp_transfer_get)
        assert user1.merchant1.resp_transfer_get['account_amount'] == '5'
        assert user1.merchant1.resp_transfer_get['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_get['in_curr'] == 'USD'
        assert user1.merchant1.resp_transfer_get['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_get['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_get['out_curr'] == 'USD'
        assert user1.merchant1.resp_transfer_get['out_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_get['owner'] == str(user1.merchant1.lid)
        assert user1.merchant1.resp_transfer_get['payway_name'] == None
        assert user1.merchant1.resp_transfer_get['reqdata']['in_curr'] == 'USD'

    def test_get_transfer_3(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        user1.merchant1.transfer_get(o_lid=user1.merchant1.resp_transfer_create['result']['lid'])
        # pprint.pprint(user1.merchant1.resp_transfer_get)
        assert user1.merchant1.resp_transfer_get['account_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_get['in_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_get['in_curr'] == 'UAH'
        assert user1.merchant1.resp_transfer_get['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_get['out_amount'] == '1'
        assert user1.merchant1.resp_transfer_get['out_curr'] == 'USD'
        assert user1.merchant1.resp_transfer_get['out_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_get['rate'] == ['28.4819', '1']
        assert user1.merchant1.resp_transfer_get['reqdata']['amount'] == '1'

    def test_get_transfer_4(self):
        """ NotFound    не найден ордер c соответствующим o_lid """
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'get', 'o_lid': 99999,
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32003
        assert user1.resp_delegate['message'] == 'EParamType'
        assert user1.resp_delegate['data']['field'] == 'o_lid'
        assert user1.resp_delegate['data']['reason'] == "'o_lid' must not be of 'int' type"
        assert user1.resp_delegate['data']['value'] == 99999

    def test_get_transfer_5(self):
        """ NotFound    не найден ордер c соответствующим o_lid """
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'get', 'o_lid': '99999',
                               'm_lid': str(user1.merchant1.lid)})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32090
        assert user1.resp_delegate['message'] == 'EParamNotFound'
        assert user1.resp_delegate['data']['field'] == 'order'
        assert user1.resp_delegate['data']['reason'] == 'Not found'

    def test_get_transfer_6(self):
        """ InvalidParam    передан o_lid несоответствующего формата """
        user1.merchant1.transfer_get(o_lid='test')
        # pprint.pprint(user1.merchant1.resp_transfer_get)
        assert user1.merchant1.resp_transfer_get['code'] == -32003
        assert user1.merchant1.resp_transfer_get['message'] == 'EParamType'
        assert user1.merchant1.resp_transfer_get['data']['field'] == 'o_lid'
        assert user1.merchant1.resp_transfer_get['data']['reason'] == 'Should be a Number'
        assert user1.merchant1.resp_transfer_get['data']['value'] == 'test'

@pytest.mark.usefixtures('_transfer_fee', '_personal_exchange_fee')
class TestTransferCalc:
    """ Testing transfer calc method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    # def test_transfer_calc_1(self): # Перевод суммы равной сумме на счету списания
    #     # Перевод суммы равной техническому минимуму по таблице currency
    #     # Запрос без in_curr
    #     """  Calc transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0.01'
    #     assert user1.resp_delegate['in_amount'] == '0.01'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '0.01'
    #     assert user1.resp_delegate['out_amount'] == '0.01'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #
    # def test_transfer_calc_2(self): # Перевод суммы равной сумме на счету списания
    #     # Перевод суммы равной техническому минимуму по таблице currency
    #     # Запрос без in_curr
    #     """  Calc transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'], is_active=False)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_3(self): # Перевод суммы равной сумме на счету списания
    #     """ Calc transfer 0.00999 BTC the same owner: BTC to BTC by MERCHANT without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.00999), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #     user1.merchant1.transfer_calc(amount='0.00999', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '0.00999'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
    #
    # def test_transfer_calc_4(self):
    #     """ Calc transfer 5 USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
    #     and with common absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '5', 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '5.55'
    #     assert user1.resp_delegate['in_amount'] == '5'
    #     assert user1.resp_delegate['in_fee_amount'] == '0.55'
    #     assert user1.resp_delegate['orig_amount'] == '5'
    #     assert user1.resp_delegate['out_amount'] == '5'
    #     assert user1.resp_delegate['out_fee_amount'] == '0.55'
    #
    # def test_transfer_calc_5(self):
    #     """ Calc transfer 0.003 BTC to another owner: BTC to BTC by MERCHANT with common absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=100000, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='0.003', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '0.0031'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '0.003'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0.0001'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '0.003'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '0.003'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0.0001'
    #
    # def test_transfer_calc_6(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc transfer 5 USD the same owner: USD to USD by MERCHANT with common percent fee 2% for transfer
    #     and with common absolute fee 1 USD for transfer with personal percent fee 1% for transfer
    #     and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=bl(0.02), add=bl(1), _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '5.55'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0.55'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0.55'
    #
    # def test_transfer_calc_7(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Calc transfer 0.003 BTC to another owner: BTC to BTC by OWNER with common percent fee 5% for transfer
    #     and with common absolute fee 0.0002 BTC for transfer with personal percent fee 3% for transfer
    #     and with personal absolute fee 0.0001 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=30000000, add=100000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=50000000, add=200000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'],  is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.003', 'out_curr': 'BTC'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '0.00319'
    #     assert user1.resp_delegate['in_amount'] == '0.003'
    #     assert user1.resp_delegate['in_fee_amount'] == '0.00019'
    #     assert user1.resp_delegate['orig_amount'] == '0.003'
    #     assert user1.resp_delegate['out_amount'] == '0.003'
    #     assert user1.resp_delegate['out_fee_amount'] == '0.00019'
    #
    # def test_transfer_calc_8(self):
    #     """ Calc transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD')
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_calc(amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '28.49'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '1'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '1'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_calc['rate'] == ['28.4819', '1']
    #
    # def test_transfer_calc_9(self):
    #     """ Calc transfer 0.43 BTC the same owner: USD to BTC by OWNER with internal exchange
    #     and with common percent fee 0.05% for exchange. """
    #     admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=500000, in_currency='USD', out_currency='BTC',
    #                             tech_min=bl(1), tech_max=bl(2000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False, merchant_id=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.43', 'in_curr': 'USD', 'out_curr': 'BTC'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '1540.46'
    #     assert user1.resp_delegate['in_amount'] == '1540.46'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '0.43'
    #     assert user1.resp_delegate['out_amount'] == '0.43'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     assert user1.resp_delegate['rate'] == ['3582.44443', '1']
    #
    # def test_transfer_calc_10(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
    #     """ Calc transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
    #     and with common fee 5% for exchange and with personal fee 3.5 % for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
    #     admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
    #     admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True)
    #     admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '322.81'
    #     assert user1.resp_delegate['in_amount'] == '293.33'
    #     assert user1.resp_delegate['in_fee_amount'] == '29.48'
    #     assert user1.resp_delegate['orig_amount'] == '10.05'
    #     assert user1.resp_delegate['out_amount'] == '10.05'
    #     assert user1.resp_delegate['out_fee_amount'] == '1.01'
    #     assert user1.resp_delegate['rate'] == ['29.1869', '1']
    #
    # def test_transfer_calc_11(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
    #     """ Calc transfer 0.43 BTC the same owner: USD to BTC by MERCHANT  with internal exchange
    #     and with common fee 1% for exchange and with personal fee 0.05% for exchange
    #     and with common percent fee 10% for transfer and with common absolute fee 0.01 BTC for transfer
    #     and with personal percent fee 5% for transfer and with personal absolute fee 0.005 BTC for transfer. """
    #     admin.set_wallet_amount(balance=bl(1800), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=3580654100000, fee=10000000, in_currency='USD', out_currency='BTC')
    #     admin.set_rate_exchange(rate=3580654100000, fee=0, in_currency='USD', out_currency='BTC')
    #     admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
    #                                     is_active=True, merchant_id=user1.merchant1.id, fee=500000)
    #     admin.set_fee(mult=100000000, add=10000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True)
    #     admin.set_fee(mult=50000000, add=5000000, _min=0, _max=0, around='ceil', tp=30,
    #                   currency_id=admin.currency['BTC'], is_active=True, merchant_id=user1.merchant1.id)
    #     user1.merchant1.transfer_calc(amount='0.43', in_curr='USD', out_curr='BTC')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '1635.4'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '1540.46'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '94.94'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '0.43'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '0.43'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0.0265'
    #     assert user1.merchant1.resp_transfer_calc['rate'] == ['3582.44443', '1']
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['BTC'],
    #                   is_active=False)
    #
    # def test_transfer_calc_12(self): # Перевод суммы больше чем на счету списания
    #     """ Calc transfer 0.02 UAH with 0.01 UAH in the wallet the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.02', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32056
    #     assert user1.resp_delegate['message'] == 'EStateInsufficientFunds'
    #     assert user1.resp_delegate['data']['reason'] == 'Balance 0.01 less then amount 0.02'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_13(self): # Перевод суммы больше чем на счету списания
    #     """ Calc transfer 10 USD with 5 USD in the wallet to another owner: USD to USD by MERCHANT
    #     without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='10', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32056
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateInsufficientFunds'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Balance 5 less then amount 10'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_14(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Calc transfer 0.01 UAH by non-active merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32015
    #     assert user1.resp_delegate['message'] == 'EParamMerchantInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'merchant'
    #     assert user1.resp_delegate['data']['reason'] == 'Improper merchant'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_15(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
    #     """ Calc transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT
    #     without fee for transfer. """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32031
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateMerchantInactive'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'x-merchant'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Merchant inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_16(self): # Перевод без суммы (amount = None)
    #     """ amount = None  delegate """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': None, 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_17(self): # Перевод без суммы (amount = None)
    #     """ amount = None  transfer """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount=None, out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32002
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_18(self): # Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  delegate """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': 'Test', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be a Number'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_19(self): # Неверное значение параметра amount (буква вместо цифры)
    #     """ amount = 'Test'  transfer """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='Test', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32002
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Should be a Number'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_20(self): # Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  delegate """
    #     admin.set_wallet_amount(balance=bl(0.2), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.111', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_21(self): # Неверный формат параметра amount (фиатная 0.111)
    #     """ amount = 0.111  transfer """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='0.111', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32082
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_22(self): # Перевод по несуществующей валюте out_curr
    #     """ Calc transfer for non-existent currency out_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_23(self): # Перевод по несуществующей валюте out_curr
    #     """ Calc transfer for non-existent currency out_curr """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32014
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_24(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_25(self, _enable_currency): # Перевод по неактивной валюте out_curr
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32033
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_26(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_27(self, _enable_currency): # Валюта out_curr выкл
    #     """ Currency out_curr off """
    #     admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32033
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_28(self): # Перевод по несуществующей валюте in_curr
    #     """ Transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'TST'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32014
    #     assert user1.resp_delegate['message'] == 'EParamCurrencyInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'in_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_29(self): # Перевод по несуществующей валюте in_curr
    #     """ Calc transfer for non-existent currency in_curr """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD', in_curr='TST')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32014
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamCurrencyInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'in_curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Invalid currency name'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_30(self, _enable_currency): # Перевод по неактивной валюте in_curr
    #     """ Currency in_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'USD'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_31(self, _enable_currency): # Перевод по неактивной валюте in_curr
    #     """ Currency in_curr off """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32033
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_32(self, _enable_currency): # Валюта in_curr выкл
    #     """ Currency in_curr off """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'USD', 'in_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32033
    #     assert user1.resp_delegate['message'] == 'EStateCurrencyInactive'
    #     assert user1.resp_delegate['data']['field'] == 'curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_33(self, _enable_currency): # Валюта in_curr выкл
    #     """ Currency in_curr off """
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD', in_curr='UAH')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32033
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EStateCurrencyInactive'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Inactive'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_34(self): # Перевод суммы ниже технического минимума по таблице currency
    #     """ Amount transfer below the technical minimum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.02), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32074
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
    #     assert user1.resp_delegate['data']['value'] == '0.01'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_35(self): # Перевод суммы ниже технического минимума по таблице currency
    #     """ Amount transfer below the technical minimum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(10), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32074
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Amount is too small'
    #     assert user1.merchant1.resp_transfer_calc['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_36(self): # Перевод суммы выше технического максимума по таблице currency
    #     """ Transfer of the amount above the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '5', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32073
    #     assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
    #     assert user1.resp_delegate['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_37(self): # Перевод суммы выше технического максимума по таблице currency
    #     """ Calc transfer of the amount above the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32073
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountTooBig'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Amount is too big'
    #     assert user1.merchant1.resp_transfer_calc['data']['value'] == '5'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_38(self): # Перевод суммы равной техническому максимуму по таблице currency
    #     """ Calc transfer of the amount equal to the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant2.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '5', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['account_amount'] == '5'
    #     assert user1.resp_delegate['in_amount'] == '5'
    #     assert user1.resp_delegate['in_fee_amount'] == '0'
    #     assert user1.resp_delegate['orig_amount'] == '5'
    #     assert user1.resp_delegate['out_amount'] == '5'
    #     assert user1.resp_delegate['out_fee_amount'] == '0'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_39(self): # Перевод суммы равной техническому максимуму по таблице currency
    #     """ Calc transfer of the amount equal to the technical maximum in the currency table """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='5', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['account_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['in_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
    #     assert user1.merchant1.resp_transfer_calc['orig_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_amount'] == '5'
    #     assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_40(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Calc transfer with the amount parameter, the value of which is less than the out_curr currency grain delegate """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.009', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32082
    #     assert user1.resp_delegate['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'amount'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_41(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
    #     """ Calc transfer with the amount parameter, the value of which is less than the out_curr currency grain transfer_create """
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0), admin_max=bl(3000), precision=2)
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='0.009', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32082
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountFormatInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'amount'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
    #
    # def test_transfer_calc_42(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.009'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_43(self): # Запрос без out_curr
    #     """ Request without out_curr """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.calc',
    #             'params': {'amount': '0.009', 'in_curr': None},
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
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_44(self): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'], is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.009', 'out_curr': None})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'out_curr'
    #     assert user1.resp_delegate['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_45(self): # Запрос out_curr = None
    #     """ Request out_curr = None """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     user1.merchant1.transfer_calc(amount='0.009', out_curr=None)
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32002
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamInvalid'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'out_curr'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Should be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_46(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
    #                            'amount': '0.01', 'out_curr': 'UAH', 'par': '123'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32002
    #     assert user1.resp_delegate['message'] == 'EParamInvalid'
    #     assert user1.resp_delegate['data']['field'] == 'par'
    #     assert user1.resp_delegate['data']['reason'] == 'Should not be provided'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_47(self): # Запрос с лишним параметром 'par': '123'
    #     """ Request with extra parameter 'par': '123' """
    #     admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.calc',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'par': '123'},
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
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_48(self): # Запрос без подписи
    #     """ Unsigned request """
    #     admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.calc',
    #             'params': {'amount': '5', 'out_curr': 'USD'},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32012
    #     assert loads(r.text)['error']['message'] == 'EParamHeadersInvalid'
    #     assert loads(r.text)['error']['data']['field'] == 'x-signature'
    #     assert loads(r.text)['error']['data']['reason'] == 'Not present'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_49(self): # Запрос с невалидной подписью
    #     """ Request with invalid sign """
    #     admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=True)
    #     ex_id = user1.merchant1._id()
    #     data = {'method': 'transfer.create',
    #             'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
    #                        'externalid': ex_id},
    #             'jsonrpc': 2.0, 'id': ex_id}
    #     time_sent = user1.merchant1.time_sent()
    #     r = requests.post(url=user1.merchant1.japi_url, json=data,
    #                       headers={'x-merchant': str(user1.merchant1.lid),
    #                                'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
    #                                'x-utc-now-ms': time_sent}, verify=False)
    #     # pprint.pprint(loads(r.text))
    #     assert loads(r.text)['error']['code'] == -32010
    #     assert loads(r.text)['error']['message'] == 'EParamSignInvalid'
    #     assert loads(r.text)['error']['data']['reason'] == 'Invalid signature'
    #     admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_50(self): # Перевод суммы не существующим мерчантом
    #     """ Transfer of non-existent merchant """
    #     admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['UAH'],
    #                   is_active=True)
    #     user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': '11111',
    #                            'amount': '0.01', 'out_curr': 'UAH'})
    #     # pprint.pprint(user1.resp_delegate)
    #     assert user1.resp_delegate['code'] == -32090
    #     assert user1.resp_delegate['message'] == 'EParamNotFound'
    #     assert user1.resp_delegate['data']['field'] == 'merchant'
    #     assert user1.resp_delegate['data']['reason'] == 'Not found'
    #     admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)
    #
    # def test_transfer_calc_51(self): # Перевод суммы ниже технического минимума по таблице exchange
    #     """ Amount transfer below the technical minimum in the exchange table transfer_create
    #     Calc transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
    #     and with common percent fee 1% for exchange. """
    #     admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
    #     admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(30), tech_max=bl(10000))
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False, merchant_id=user1.merchant1.id)
    #     admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
    #                   is_active=False)
    #     user1.merchant1.transfer_calc(amount='1', in_curr='UAH', out_curr='USD')
    #     # pprint.pprint(user1.merchant1.resp_transfer_calc)
    #     assert user1.merchant1.resp_transfer_calc['code'] == -32074
    #     assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountTooSmall'
    #     assert user1.merchant1.resp_transfer_calc['data']['field'] == 'in_amount'
    #     assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Amount is too small'
    #     assert user1.merchant1.resp_transfer_calc['data']['value'] == '28.49'
    #     admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
    #                             tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_52(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы ниже технического минимума по таблице exchange
        Amount transfer below the technical minimum in the exchange table delegate
        Calc transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(400), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32074
        assert user1.resp_delegate['message'] == 'EParamAmountTooSmall'
        assert user1.resp_delegate['data']['field'] == 'in_amount'
        assert user1.resp_delegate['data']['reason'] == 'Amount is too small'
        assert user1.resp_delegate['data']['value'] == '293.33'
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_53(self): # Перевод суммы выше технического максимума по таблице exchange
        """ Amount transfer above the technical maximum in the exchange table transfer_create
        Calc transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(20))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False)
        user1.merchant1.transfer_calc(amount='1', in_curr='UAH', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_calc)
        assert user1.merchant1.resp_transfer_calc['code'] == -32073
        assert user1.merchant1.resp_transfer_calc['message'] == 'EParamAmountTooBig'
        assert user1.merchant1.resp_transfer_calc['data']['field'] == 'in_amount'
        assert user1.merchant1.resp_transfer_calc['data']['reason'] == 'Amount is too big'
        assert user1.merchant1.resp_transfer_calc['data']['value'] == '28.49'
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_54(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы выше технического максимума по таблице exchange
        Amount transfer above the technical maximum in the exchange table delegate
        Calc transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['code'] == -32073
        assert user1.resp_delegate['message'] == 'EParamAmountTooBig'
        assert user1.resp_delegate['data']['field'] == 'in_amount'
        assert user1.resp_delegate['data']['reason'] == 'Amount is too big'
        assert user1.resp_delegate['data']['value'] == '293.33'
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_55(self): # Перевод суммы равной техническому минимуму по таблице exchange
        """ Calc transfer of the amount equal to the technical maximum in the exchange table transfer_create
        Calc transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(28.49), tech_max=bl(10000))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False)
        user1.merchant1.transfer_calc(amount='1', in_curr='UAH', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_calc)
        assert user1.merchant1.resp_transfer_calc['account_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_calc['in_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_calc['orig_amount'] == '1'
        assert user1.merchant1.resp_transfer_calc['out_amount'] == '1'
        assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_calc['rate'] == ['28.4819', '1']
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_56(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы равной техническому минимуму по таблице exchange
        Calc transfer of the amount equal to the technical maximum in the exchange table delegate
        Calc transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(293.33), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '322.81'
        assert user1.resp_delegate['in_amount'] == '293.33'
        assert user1.resp_delegate['in_fee_amount'] == '29.48'
        assert user1.resp_delegate['orig_amount'] == '10.05'
        assert user1.resp_delegate['out_amount'] == '10.05'
        assert user1.resp_delegate['out_fee_amount'] == '1.01'
        assert user1.resp_delegate['rate'] == ['29.1869', '1']
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_57(self): # Перевод суммы равной техническому максимуму по таблице exchange
        """ Calc transfer of the amount equal to the technical maximum in the exchange table transfer_create
        Calc transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(28.49))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency_id=admin.currency['USD'],
                      is_active=False)
        user1.merchant1.transfer_calc(amount='1', in_curr='UAH', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_calc)
        assert user1.merchant1.resp_transfer_calc['account_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_calc['in_amount'] == '28.49'
        assert user1.merchant1.resp_transfer_calc['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_calc['orig_amount'] == '1'
        assert user1.merchant1.resp_transfer_calc['out_amount'] == '1'
        assert user1.merchant1.resp_transfer_calc['out_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_calc['rate'] == ['28.4819', '1']
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_calc_58(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы равной техническому максимуму по таблице exchange
        Calc transfer of the amount equal to the technical maximum in the exchange table delegate
        Calc transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(293.33))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30,
                      currency_id=admin.currency['USD'], is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'calc', 'm_lid': str(user1.merchant1.lid),
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['account_amount'] == '322.81'
        assert user1.resp_delegate['in_amount'] == '293.33'
        assert user1.resp_delegate['in_fee_amount'] == '29.48'
        assert user1.resp_delegate['orig_amount'] == '10.05'
        assert user1.resp_delegate['out_amount'] == '10.05'
        assert user1.resp_delegate['out_fee_amount'] == '1.01'
        assert user1.resp_delegate['rate'] == ['29.1869', '1']
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

class TestTransferList:
    """ Testing transfer list method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success no filter list test. """
        admin_count = int(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': '30'})[0]['count'])
        assert admin_count == user1.merchant1.transfer_list()['total']

    def test_2(self):
        """ Success in_curr filter test. """
        curr = 'USD'
        r = user1.merchant1.transfer_list(in_curr=curr)['data'][0]
        assert r['in_curr'] == curr, r

    def test_3(self):
        """ Unknown in_curr filter test. """
        curr = 'ГРН'
        r = user1.merchant1.transfer_list(in_curr=curr)
        # pprint.pprint(r)
        assert r['code'] == -32014
        assert r['data']['field'] == 'in_curr'
        assert r['data']['reason'] == 'Invalid currency name'
        assert r['message'] == 'EParamCurrencyInvalid'

    def test_4(self):
        """ Success out_curr filter test. """
        curr = 'USD'
        r = user1.merchant1.transfer_list(out_curr=curr)['data'][0]
        assert r['out_curr'] == curr, r

    def test_5(self):
        """ Unknown out_curr filter test. """
        curr = 'ГРН'
        r = user1.merchant1.transfer_list(out_curr=curr)
        # pprint.pprint(r)
        assert r['code'] == -32014
        assert r['data']['field'] == 'out_curr'
        assert r['data']['reason'] == 'Invalid currency name'
        assert r['message'] == 'EParamCurrencyInvalid'

    def test_6(self):
        """ First filter test. """
        r = user1.merchant1.transfer_list()['data'][1]
        test = user1.merchant1.transfer_list(first='1')['data'][0]
        assert r == test

    def test_7(self):
        """ First filter test. """
        r = user1.merchant1.transfer_list(first=1)
        # pprint.pprint(r)
        assert r['code'] == -32003
        assert r['data']['field'] == 'first'
        assert r['data']['reason'] == "'first' must not be of 'int' type"
        assert r['data']['value'] == 1
        assert r['message'] == 'EParamType'

    def test_8(self):
        """ First filter test. """
        r = user1.merchant1.transfer_list(first='one')
        # pprint.pprint(r)
        assert r['code'] == -32003
        assert r['data']['field'] == 'first'
        assert r['data']['reason'] == 'Should be an Integer'
        assert r['message'] == 'EParamType'

    def test_9(self):
        """ First filter test. """
        r = user1.merchant1.transfer_list(first='9999999')['data']
        assert not r

    def test_10(self):
        """ Count filter test. """
        count = 10
        r = user1.merchant1.transfer_list(count=str(count))
        len = r['data'].__len__()
        assert len == count or len == r['total']

    def test_11(self):
        """ Count filter test. """
        count = 0
        r = user1.merchant1.transfer_list(count=str(count))
        # pprint.pprint(r)
        assert r['code'] == -32002
        assert r['data']['field'] == 'count'
        assert r['data']['reason'] == 'Should be more than zero'
        assert r['message'] == 'EParamInvalid'