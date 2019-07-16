import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint


class TestTransfer:
    """ Create transfer. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_transfer_1(self): # Перевод суммы равной сумме на счету списания
        # Перевод суммы равной техническому минимуму по таблице currency
        # Запрос без in_curr
        """  Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='UAH') == '0'
        # print('\n', 'balance(UAH)', user1.merchant1.resp_balance['UAH'])

    def test_transfer_2(self): # Перевод суммы равной сумме на счету списания
        # Перевод суммы равной техническому минимуму по таблице currency
        # Запрос без in_curr
        """  Transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # print("user1.merchant1.resp_transfer")
        # pprint.pprint(user1.merchant1.resp_transfer)
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='USD') == '0'
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)

    def test_transfer_3(self): # Перевод суммы равной сумме на счету списания
        """ Transfer 0.00999 BTC the same owner: BTC to BTC by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.00999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=False)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='0.00999', out_curr='BTC')
        # print("user1.merchant1.resp_transfer")
        # pprint.pprint(user1.merchant1.resp_transfer)
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '0.00999'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.00999'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '0.00999'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='BTC') == '0'

    def test_transfer_4(self):
        """ Transfer 5 USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
        and with common absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '5', 'out_curr': 'USD'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '5'
        assert user1.resp_delegate['out_amount'] == '5'
        assert user1.resp_delegate['in_fee_amount'] == '0.55'
        assert user1.resp_delegate['reqdata']['amount'] == '5'
        assert user1.resp_delegate['out_fee_amount'] == '0.55'
        assert user1.merchant1.balance(curr='USD') == '4.45'

    def test_transfer_5(self):
        """ Transfer 0.003 BTC to another owner: BTC to BTC by MERCHANT with common absolute fee 0.0001 BTC for transfer. """
        admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=100000, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.003', out_curr='BTC')
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '0.003'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.003'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0.0001'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '0.0031'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.0001'
        assert user1.merchant1.balance(curr='BTC') == '0.0009'

    def test_transfer_6(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Transfer 5 USD the same owner: USD to USD by MERCHANT with common percent fee 2% for transfer
        and with common absolute fee 1 USD for transfer with personal percent fee 1% for transfer
        and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=10000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=20000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0.55'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5.55'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.55'
        assert user1.merchant1.balance(curr='USD') == '4.45'

    def test_transfer_7(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
        """ Transfer 0.003 BTC to another owner: BTC to BTC by OWNER with common percent fee 5% for transfer
        and with common absolute fee 0.0002 BTC for transfer with personal percent fee 3% for transfer
        and with personal absolute fee 0.0001 BTC for transfer. """
        admin.set_wallet_amount(balance=bl(0.004), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=30000000, add=100000, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=50000000, add=200000, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '0.003', 'out_curr': 'BTC'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '0.003'
        assert user1.resp_delegate['out_amount'] == '0.003'
        assert user1.resp_delegate['in_fee_amount'] == '0.00019'
        assert user1.resp_delegate['reqdata']['amount'] == '0.003'
        assert user1.resp_delegate['out_fee_amount'] == '0.00019'
        assert user1.merchant1.balance(curr='BTC') == '0.00081'

    def test_transfer_8(self):
        """ Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=bl(0.01), in_currency='UAH', out_currency='USD')
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
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

    def test_transfer_9(self):
        """ Transfer 0.43 BTC the same owner: USD to BTC by OWNER with internal exchange
        and with common percent fee 0.05% for exchange. """
        admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=3580654100000, fee=500000, in_currency='USD', out_currency='BTC',
                                tech_min=bl(1), tech_max=bl(2000))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=False, merchant_id=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.43', 'in_curr': 'USD', 'out_curr': 'BTC'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['in_amount'] == '1540.46'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['out_amount'] == '0.43'
        assert user1.resp_delegate['rate'] == ['3582.44443', '1']
        assert user1.resp_delegate['reqdata']['amount'] == '0.43'
        # user1.merchant1.balance(curr='USD')
        # assert user1.merchant1.resp_balance['USD'] == '59.54'
        # time.sleep(2)
        # user1.merchant2.balance(curr='BTC')
        # assert user1.merchant2.resp_balance['BTC'] == '1.43'

    def test_transfer_10(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
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
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)

    def test_transfer_11(self, _custom_fee, _disable_personal_operation_fee_transfer_BTC):
        """ Transfer 0.43 BTC the same owner: USD to BTC by MERCHANT  with internal exchange
        and with common fee 1% for exchange and with personal fee 0.05% for exchange
        and with common percent fee 10% for transfer and with common absolute fee 0.01 BTC for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.005 BTC for transfer. """
        admin.set_wallet_amount(balance=bl(1800), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=3580654100000, fee=10000000, in_currency='USD', out_currency='BTC')
        admin.set_rate_exchange(rate=3580654100000, fee=0, in_currency='USD', out_currency='BTC')
        admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=500000)
        admin.set_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=500000)
        admin.set_fee(mult=100000000, add=10000000, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=True)
        admin.set_fee(mult=50000000, add=5000000, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='0.43', in_curr='USD', out_curr='BTC')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '1540.46'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '0.43'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '94.94'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '1635.4'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0.0265'
        assert user1.merchant1.resp_transfer_create['result']['rate'] == ['3582.44443', '1']
        assert user1.merchant1.resp_transfer_create['result']['reqdata']['amount'] == '0.43'
        # user1.merchant1.balance(curr='USD')
        # assert user1.merchant1.resp_balance['result']['USD'] == '164.6'
        # time.sleep(2)
        # user1.merchant2.balance(curr='BTC')
        # assert user1.merchant2.resp_balance['result']['BTC'] == '1.43'
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=False)

    @pytest.mark.skip
    def test_transfer_12(self, _disable_2type): # Перевод с включенным двухфакторным подтверждением без конвертации
                                                # и без комисии за операцию перевода
        """ Transfer twostepauth 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.set_2type(tp=0)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.lid)

    @pytest.mark.skip
    def test_transfer_13(self, _disable_2type): # Перевод с включенным двухфакторным подтверждением без конвертации
                                                # и без комисии за операцию перевода
        """Transfer twostepauth 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.set_2type(tp=0)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        # print("user1.merchant1.resp_transfer")
        # pprint.pprint(user1.merchant1.resp_transfer)
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.rbalance(curr='USD') == '0'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_14(self, _disable_st_value): # Выплаты во всей системе заблокированы
        """ Payments in the entire system are blocked
        Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=10000000, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_st_value(name='out_is_blocked', value=True)
        # print(admin.resp_st_value)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message']== 'UnavailableOutPay'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_15(self, _disable_st_value): # Выплаты во всей системе заблокированы
        """ Payments in the entire system are blocked
        Transfer 5 USD to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_st_value(name='out_is_blocked', value=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'UnavailableOutPay'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_16(self, _enable_merchant_payout_allowed): # Вывод для данного пользователя заблокирован (payout_allowed)
        """ Sender's payout is blocked
        Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=10000000, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'UnavailableOutPay'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.lid)

    def test_transfer_17(self, _enable_merchant_payout_allowed): # Вывод для получателя заблокирован (payout_allowed)
        """ Recipient payout is blocked
        Transfer 0.01 UAH the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=10000000, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                       is_active=True, merchant_id=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_merchant(lid=user1.merchant2.id, payout_allowed=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['account_amount'] == '0.01'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='UAH') == '0'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.lid)

    def test_transfer_18(self, _enable_merchant_payout_allowed): # Вывод для данного пользователя заблокирован (payout_allowed)
        """ Sender's payout is blocked
        Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_merchant(lid=user1.merchant1.lid, payout_allowed=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'UnavailableOutPay'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_19(self, _enable_merchant_payout_allowed): # Вывод для получателя заблокирован (payout_allowed)
        """ Recipient payout is blocked
        Transfer 5 USD to non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_merchant(lid=user2.merchant1.lid, payout_allowed=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='USD') == '0'
        admin.set_merchant(lid=user1.merchant1.id, is_active=True)
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_20(self): # Перевод суммы больше чем на счету списания
        """ Transfer 0.02 UAH with 0.01 UAH in the wallet the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.02', 'out_curr': 'UAH'})        # pprint.pprint(resp_delegate)
        assert user1.resp_delegate['message'] == 'InsufficientFunds'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_21(self): # Перевод суммы больше чем на счету списания
        """ Transfer 10 USD with 5 USD in the wallet to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='10', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InsufficientFunds'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_22(self): # Перевод суммы не существующему мерчанту
        """ Transfer 0.01 UAH to non-existent merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': '11111',
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_23(self): # Перевод суммы не существующему мерчанту
        """ Transfer 5 USD to non-existent merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt='11111', amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_24(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
        """ Transfer 0.01 UAH by non-active merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_25(self, _enable_merchant_is_active): # Перевод суммы не активному мерчанту
        """ Transfer 0.01 UAH to non-active merchant the same owner: UAH to UAN by OWNER without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_merchant(lid=user1.merchant2.lid, is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_26(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
        """ Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_merchant(lid=user2.merchant1.lid, is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_26_1(self, _enable_merchant_is_active): # Перевод суммы не активным мерчантом
        """ Transfer 5 USD by non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidMerchant'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_27(self, _enable_merchant_is_active): # Перевод суммы не активному мерчанту
        """ Transfer 5 USD to non-active merchant to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_merchant(lid=user2.merchant1.lid, is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_28(self): # Перевод без суммы (amount = None)
        """ amount = None  delegate """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': None, 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_29(self): # Перевод без суммы (amount = None)
        """ amount = None  transfer """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount=None, out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_30(self): # Неверное значение параметра amount (буква вместо цифры)
        """ amount = 'Test'  delegate """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': 'Test', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_31(self): # Неверное значение параметра amount (буква вместо цифры)
        """ amount = 'Test'  transfer """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='Test', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_32(self): # Неверный формат параметра amount (фиатная 0.111)
        """ amount = 0.111  delegate """
        admin.set_wallet_amount(balance=bl(0.2), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.111', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_33(self): # Неверный формат параметра amount (фиатная 0.111)
        """ amount = 0.111  transfer """
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.111', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_34(self): # Перевод по несуществующей валюте out_curr
        """ Transfer for non-existent currency out_curr """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'TST'})
        assert user1.resp_delegate['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_35(self): # Перевод по несуществующей валюте out_curr
        """ Transfer for non-existent currency out_curr """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='TST')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_36(self, _enable_currency): # Перевод по неактивной валюте out_curr
        """ Currency out_curr off """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_37(self, _enable_currency): # Перевод по неактивной валюте out_curr
        """ Currency out_curr off """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_38(self, _enable_currency): # Валюта out_curr выкл
        """ Currency out_curr off """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_39(self, _enable_currency): # Валюта out_curr выкл
        """ Currency out_curr off """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_40(self): # Перевод по несуществующей валюте in_curr
        """ Transfer for non-existent currency in_curr """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'TST'})
        assert user1.resp_delegate['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_41(self): # Перевод по несуществующей валюте in_curr
        """ Transfer for non-existent currency in_curr """
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='TST')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_42(self, _enable_currency): # Перевод по неактивной валюте in_curr
        """ Currency in_curr off """
        admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH', 'in_curr': 'USD'})
        assert user1.resp_delegate['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_43(self, _enable_currency): # Перевод по неактивной валюте in_curr
        """ Currency in_curr off """
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=True, merchant_id=user1.merchant1.id)

    def test_transfer_44(self, _enable_currency): # Валюта in_curr выкл
        """ Currency in_curr off """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.01), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'USD', 'in_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_45(self, _enable_currency): # Валюта in_curr выкл
        """ Currency in_curr off """
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD', in_curr='UAH')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InactiveCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_46(self): # Перевод суммы ниже технического минимума по таблице currency
        """ Amount transfer below the technical minimum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.02), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'AmountTooSmall'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_47(self): # Перевод суммы ниже технического минимума по таблице currency
        """ Amount transfer below the technical minimum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(10), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'AmountTooSmall'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_48(self): # Перевод суммы выше технического максимума по таблице currency
        """ Transfer of the amount above the technical maximum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '5', 'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooBig'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_49(self): # Перевод суммы выше технического максимума по таблице currency
        """ Transfer of the amount above the technical maximum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'AmountTooBig'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_50(self): # Перевод суммы равной техническому максимуму по таблице currency
        """ Transfer of the amount equal to the technical maximum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant2.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '5', 'out_curr': 'UAH'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '5'
        assert user1.resp_delegate['out_amount'] == '5'
        assert user1.resp_delegate['in_fee_amount'] == '0'
        assert user1.resp_delegate['account_amount'] == '5'
        assert user1.resp_delegate['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='UAH') == '5'
        time.sleep(2)
        assert user1.merchant2.balance(curr='UAH') == '15'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_51(self): # Перевод суммы равной техническому максимуму по таблице currency
        """ Transfer of the amount equal to the technical maximum in the currency table """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(5), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['result']['status'] == 'done'
        assert user1.merchant1.resp_transfer_create['result']['in_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['in_fee_amount'] == '0'
        assert user1.merchant1.resp_transfer_create['result']['account_amount'] == '5'
        assert user1.merchant1.resp_transfer_create['result']['out_fee_amount'] == '0'
        assert user1.merchant1.balance(curr='USD') == '5'
        time.sleep(2)
        assert user2.merchant1.balance(curr='USD') == '15'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_52(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
        """ Transfer with the amount parameter, the value of which is less than the out_curr currency grain delegate """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.009', 'out_curr': 'UAH'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_53(self): # Перевод с параметром amount, значение которого меньше зерна валюты out_curr
        """ Transfer with the amount parameter, the value of which is less than the out_curr currency grain transfer_create """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.009', out_curr='USD')
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidAmountFormat'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)

    def test_transfer_54(self): # Запрос без out_curr
        """ Request without out_curr """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid, 'amount': '0.009'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_55(self): # Запрос без out_curr
        """ Request without out_curr """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '0.009', 'in_curr': None, 'tgt': str(user2.merchant1.lid), 'externalid': ex_id},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_56(self): # Запрос out_curr = None
        """ Request out_curr = None """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid, 'amount': '0.009',
                               'out_curr': None})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_57(self): # Запрос out_curr = None
        """ Request out_curr = None """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=user2.merchant1.lid, amount='0.009', out_curr=None)
        # pprint.pprint(user1.merchant1.resp_transfer_create)
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidCurrency'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_58(self): # Запрос с лишним параметром 'par': '123'
        """ Request with extra parameter 'par': '123' """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid, 'amount': '0.01',
                               'out_curr': 'UAH', 'par': '123'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_59(self): # Запрос с лишним параметром 'par': '123'
        """ Request with extra parameter 'par': '123' """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid), 'externalid': ex_id, 'par': '123'},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_60(self): # Запрос без externalid
        """ Request without externalid delegate """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'out_curr': 'UAH',
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid, 'amount': '0.01'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_61(self): # Запрос без externalid
        """ Request without externalid transfer.create """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid)},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_62(self): # Запрос с существующим externalid
        """ Request with existing externalid delegate """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=True)
        tmp_ex_id=user1.ex_id()
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': tmp_ex_id,
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': tmp_ex_id,
                               'm_lid': user1.merchant1.lid, 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'Unique'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_63(self): # Запрос с существующим externalid
        """ Request with existing externalid transfer.create """
        admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
                           'externalid': ex_id},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['message'] == 'Unique'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_64(self): # Запрос без подписи
        """ Unsigned request """
        admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
                           'externalid': ex_id},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['message'] == 'InvalidHeaders'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_65(self): # Запрос с невалидной подписью
        """ Request with invalid sign """
        admin.set_wallet_amount(balance=bl(100), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'tgt': str(user2.merchant1.lid),
                           'externalid': ex_id},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['message'] == 'InvalidSign'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_66(self): # Перевод суммы не существующим мерчантом
        """ Transfer of non-existent merchant """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': '11111', 'tgt': user1.merchant2.lid,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'NotFound'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_67(self): # Запрос tgt=None
        """ tgt=None """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': None,
                               'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InvalidParam'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_68(self): # Запрос tgt=None
        """ tgt=None """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.merchant1.transfer_create(tgt=None, amount='5', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'InvalidParam'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_69(self): # Запрос без tgt
        """ Request without tgt """
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'amount': '0.01', 'out_curr': 'UAH'})
        assert user1.resp_delegate['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_70(self): # Запрос без tgt
        """ Request without tgt """
        admin.set_wallet_amount(balance=5000000000, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        ex_id = user1.merchant1._id()
        data = {'method': 'transfer.create',
                'params': {'amount': '5', 'out_curr': 'USD', 'externalid': ex_id},
                'jsonrpc': 2.0, 'id': ex_id}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                            headers={'x-merchant': str(user1.merchant1.lid),
                                    'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                    'x-utc-now-ms': time_sent}, verify=False)
        # pprint.pprint(loads(r.text))
        assert loads(r.text)['error']['message'] == 'InvalidInputParams'
        admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

    def test_transfer_71(self): # Перевод суммы ниже технического минимума по таблице exchange
        """ Amount transfer below the technical minimum in the exchange table transfer_create
        Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(30), tech_max=bl(10000))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'AmountTooSmall'
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_72(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы ниже технического минимума по таблице exchange
        Amount transfer below the technical minimum in the exchange table delegate
        Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(400), tech_max=bl(10000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        assert user1.resp_delegate['message'] == 'AmountTooSmall'
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_73(self): # Перевод суммы выше технического максимума по таблице exchange
        """ Amount transfer above the technical maximum in the exchange table transfer_create
        Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(20))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
        user1.merchant1.transfer_create(tgt=user1.merchant2.lid, amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_transfer_create['error']['message'] == 'AmountTooBig'
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_74(self, _custom_fee, _disable_personal_operation_fee_transfer_USD):
        """ Перевод суммы выше технического максимума по таблице exchange
        Amount transfer above the technical maximum in the exchange table delegate
        Transfer 10.05 USD to another owner: UAH to USD by OWNER  with internal exchange
        and with common fee 5% for exchange and with personal fee 3.5 % for exchange
        and with common percent fee 10% for transfer and with common absolute fee 1 USD for transfer
        and with personal percent fee 5% for transfer and with personal absolute fee 0.5 USD for transfer. """
        admin.set_wallet_amount(balance=bl(400), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user2.merchant1.lid)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(200))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=35000000)
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
        # pprint.pprint(user1.resp_delegate)
        assert user1.resp_delegate['message'] == 'AmountTooBig'
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

    def test_transfer_75(self): # Перевод суммы равной техническому минимуму по таблице exchange
        """ Transfer of the amount equal to the technical maximum in the exchange table transfer_create
        Transfer 1 USD the same owner: UAH to USD by MERCHANT with internal exchange
        and with common percent fee 1% for exchange. """
        admin.set_wallet_amount(balance=bl(30), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant2.lid)
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(28.49), tech_max=bl(10000))
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
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
        admin.set_rate_exchange(rate=28199900000, fee=10000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))

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
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
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
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
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
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
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
        admin.set_fee(mult=100000000, add=1000000000, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        admin.set_fee(mult=50000000, add=500000000, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=True, merchant_id=user1.merchant1.id)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '10.05', 'in_curr': 'UAH', 'out_curr': 'USD'})
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
        # admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
        admin.set_rate_exchange(rate=28199900000, fee=50000000, in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.1), tech_max=bl(10000))



class TestParams:
    """ Testing transfer params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency_precision(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000), precision=2)
        admin.set_currency_precision(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3), precision=8)

    def test_params_1(self):
        """ Getting params for transfer UAH the same owner: UAH to UAN by OWNER without fee for transfer"""
        admin.set_wallet_amount(balance=bl(0.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='UAH', is_active=False)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': user1.merchant1.lid, 'out_curr': 'UAH'})
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['in_curr_balance'] == '0.01'
        assert user1.resp_delegate['is_convert'] == False
        assert user1.resp_delegate['max'] == '3000'
        assert user1.resp_delegate['min'] == '0.01'
        assert user1.resp_delegate['min_balance_limit'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['out_fee'] == {}
        assert user1.resp_delegate['rate'] == ['1', '1']

    def test_params_2(self):
        """ Getting params for transfer USD to another owner: USD to USD by MERCHANT without fee for transfer. """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=False)
        user1.merchant1.transfer_params(out_curr='USD')
        assert user1.merchant1.resp_transfer_params['in_curr'] == 'USD'
        assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '5'
        assert user1.merchant1.resp_transfer_params['is_convert'] == False
        assert user1.merchant1.resp_transfer_params['max'] == '3000'
        assert user1.merchant1.resp_transfer_params['min'] == '5'
        assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '5'
        assert user1.merchant1.resp_transfer_params['out_curr'] == 'USD'
        assert user1.merchant1.resp_transfer_params['out_fee'] == {}
        assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']

    def test_params_3(self):
        """ Getting params for transfer BTC the same owner: BTC to BTC by MERCHANT without fee for transfer. """
        admin.set_wallet_amount(balance=bl(0.00999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='BTC', is_active=False)
        user1.merchant1.transfer_params(out_curr='BTC')
        assert user1.merchant1.resp_transfer_params['in_curr'] == 'BTC'
        assert user1.merchant1.resp_transfer_params['in_curr_balance'] == '0.00999'
        assert user1.merchant1.resp_transfer_params['is_convert'] == False
        assert user1.merchant1.resp_transfer_params['max'] == '3'
        assert user1.merchant1.resp_transfer_params['min'] == '0.000001'
        assert user1.merchant1.resp_transfer_params['min_balance_limit'] == '0.000001'
        assert user1.merchant1.resp_transfer_params['out_curr'] == 'BTC'
        assert user1.merchant1.resp_transfer_params['out_fee'] == {}
        assert user1.merchant1.resp_transfer_params['rate'] == ['1', '1']

    def test_transfer_4(self):
        """ Transfer 5 USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
        and with common absolute fee 0.5 USD for transfer. """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'create', 'externalid': user1.ex_id(),
                               'm_lid': user1.merchant1.lid, 'tgt': user2.merchant1.lid,
                               'amount': '5', 'out_curr': 'USD'})
        assert user1.resp_delegate['status'] == 'done'
        assert user1.resp_delegate['in_amount'] == '5'
        assert user1.resp_delegate['out_amount'] == '5'
        assert user1.resp_delegate['in_fee_amount'] == '0.55'
        assert user1.resp_delegate['reqdata']['amount'] == '5'
        assert user1.resp_delegate['out_fee_amount'] == '0.55'
        assert user1.merchant1.balance(curr='USD') == '4.45'

    def test_params_4(self):
        """ Getting params for transfer USD to another owner: USD to USD by OWNER with common percent fee 1% for transfer
        and with common absolute fee 0.5 USD for transfer. """
        admin.set_currency_precision(is_crypto=False, admin_min=bl(5), admin_max=bl(3000), precision=2)
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_fee(mult=0, add=0, _min=0, _max=0, around='ceil', tp=30, currency='USD',
                      is_active=False, merchant_id=user1.merchant1.id)
        admin.set_fee(mult=bl(0.01), add=bl(0.5), _min=0, _max=0, around='ceil', tp=30, currency='USD', is_active=True)
        user1.delegate(params={'merch_model': 'transfer', 'merch_method': 'params',  'm_lid': user1.merchant1.lid, 'out_curr': 'USD'})
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['in_curr_balance'] == '10'
        assert user1.resp_delegate['is_convert'] == False
        assert user1.resp_delegate['max'] == '3000'
        assert user1.resp_delegate['min'] == '5'
        assert user1.resp_delegate['min_balance_limit'] == '5.56'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['out_fee'] == None
        assert user1.resp_delegate['rate'] == ['1', '1']
