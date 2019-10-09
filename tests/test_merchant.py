import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint


class TestMerchantBalance:
    """ Balance """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000))
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3))

    def test_MerchantBalance_1(self):
        """ Balance all. """
        admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='ETH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.99999), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0), currency='USDT', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1), currency='LTC', merch_lid=user1.merchant1.lid)
        wal_list = {dct['currency_id']: float(orig(dct['balance']))
                    for dct in admin.get_model(model='wallet', _filter='merchant_id', value=user1.merchant1.id)}
        user1.merchant1.balance()
        bal_list = {admin.currency[dct[0]]: float(dct[1]) for dct in user1.merchant1.resp_balance.items()}
        # pprint.pprint(wal_list)
        # pprint.pprint(bal_list)
        assert wal_list == bal_list

    def test_MerchantBalance_2(self):
        """ Balance USD. """
        admin.set_wallet_amount(balance=bl(1600), currency='USD', merch_lid=user1.merchant1.lid)
        # print(user1.merchant1.resp_balance)
        assert user1.merchant1.balance(curr='USD') == '1600'

    def test_MerchantBalance_3(self):
        """ Balance UAH. """
        admin.set_wallet_amount(balance=bl(11.5), currency='UAH', merch_lid=user1.merchant1.lid)
        assert user1.merchant1.balance(curr='UAH') == '11.5'

    def test_MerchantBalance_4(self, _enable_currency):
        """ Balance RUB сurrency is inactive. """
        admin.set_wallet_amount(balance=bl(1.02), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
        assert user1.merchant1.balance(curr='RUB') == '1.02'

    def test_MerchantBalance_5(self, _enable_currency):
        """ Balance BCHABC сurrency off. """
        admin.set_wallet_amount(balance=bl(250), currency='BCHABC', merch_lid=user1.merchant1.lid)
        admin.set_currency_activity(name='BCHABC', is_disabled=True, is_active=True)
        assert user1.merchant1.balance(curr='BCHABC') == '250'

    def test_MerchantBalance_6(self):
        """ Balance non-existent currency. """
        assert user1.merchant1.balance(curr='TST')['error']['message'] == 'EParamCurrencyInvalid'
        # pprint.pprint(user1.merchant1.resp_balance)

class TestOrderGet:
    """Order_get"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success order get request """""
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id})[1]['lid'])
        user1.merchant1.order_get(o_lid=lid)
        keys = ['account_amount', 'ctime', 'externalid', 'ftime', 'in_amount', 'in_curr', 'in_fee_amount',
               'lid', 'orig_amount', 'out_amount', 'out_curr', 'out_fee_amount', 'owner', 'payway_name', 'rate',
               'ref', 'renumeration', 'reqdata', 'status', 'tgt', 'token', 'tp', 'userdata']
        r = user1.merchant1.resp_order_get.get('result')
        test_keys = list(r.keys())
        test_keys.sort()
        # pprint.pprint(keys)
        # pprint.pprint(test_keys)
        assert test_keys == keys
        assert str(r['lid']) == lid

    # def test_2(self):
    #     """ Success order get request with enable ibill"""
    #     lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': '100'})[1]['lid'])
    #     user1.merchant1.order_get(o_lid=lid, ibill=True)
    #     keys = ['amount', 'balance', 'ctime' ,'curr' ,'fee' ,'lid' ,'model' ,'oid' ,'other_curr']
    #     r = user1.merchant1.resp_order_get['result']
    #     # test_keys = list(r['balance_changes'][0].keys())
    #     pprint.pprint(user1.merchant1.resp_order_get['result'])
    #     # test_keys.sort()
    #     # pprint.pprint(keys)
    #     assert user1.merchant1.resp_order_get['result']['balance_changes'] == []
    #     assert str(r['lid']) == lid

    def test_3(self):
        """ Success order get request with enable ibill"""
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': '0', 'tp': '0'})[1]['lid'])
        user1.merchant1.order_get(o_lid=lid, ibill=True)
        assert not user1.merchant1.resp_order_get['result']['balance_changes']

    def test_4(self):
        """ Order get request with empty ibill filter"""
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': '0', 'tp': '0'})[1]['lid'])
        user1.merchant1.order_get(o_lid=lid, ibill=None)
        r = user1.merchant1.resp_order_get.get('result')
        assert str(r['lid']) == lid

    def test_5(self):
        """ Order get request with invalidate (int) o_lid filter"""
        user1.merchant1.order_get(o_lid=1290, ibill=False)
        error = user1.merchant1.resp_order_get.get('error')
        assert error == {'code': -32003, 'message': 'EParamType',
                         'data': {'field': 'o_lid', 'reason': "'o_lid' must not be of 'int' type", 'value': 1290}}

    def test_6(self):
        """ Order get request with empty o_lid filter. """
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': '0', 'tp': '0'})[1]['lid'])
        user1.merchant1.order_get(o_lid=None)
        error = user1.merchant1.resp_order_get.get('error')
        assert error == {'code': -32002, 'message': 'EParamInvalid',
                         'data': {'field': 'o_lid', 'reason': 'Should be provided'}}

    def test_7(self):
        """ Order get request with unknown o_lid filter and ibill false. """
        user1.merchant1.order_get(o_lid='999999', ibill=False)
        error = user1.merchant1.resp_order_get.get('error')
        assert error == {'code': -32090, 'message': 'EParamNotFound',
                         'data': {'field': 'o_lid', 'reason': 'Not found'}}

    def test_8(self):
        """ Order get request with unknown o_lid filter and ibill true"""
        user1.merchant1.order_get(o_lid='999999', ibill=True)
        error = user1.merchant1.resp_order_get.get('error')
        assert error == {'code': -32090, 'message': 'EParamNotFound',
                         'data': {'field': 'o_lid', 'reason': 'Not found'}}

class TestIbillHistory:
    """ ibill_history """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Ibill count comparison. """
        admin_count = admin.get_ibill(selector={'merchant_id': user1.merchant1.id})['count']
        assert admin_count == user1.merchant1.ibill_history()['total']

    def test_2(self):
        """ Ibill [0] comparison. """
        ibill = user1.merchant1.ibill_history()['data'][0]
        assert admin.get_ibill(selector={'merchant_id': user1.merchant1.id, 'id': ibill['oid']}) \
               != 'No ibills for this query.'

    def test_3(self):
        """ Begin filter test. Begin = ibill ctime. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_4(self):
        """ Begin filter test. Begin = ibill ctime -1. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_5(self):
        """ Begin filter test. Begin = ibill ctime +1. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_6(self):
        """ End filter test. End = ibill ctime. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_7(self):
        """ End filter test. End = ibill ctime -1. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_8(self):
        """ End filter test. End = ibill ctime +1. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_9(self):
        """ Begin + End filter test. Begin = ibill ctime, end = ibill ctime +1. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time+1))['data'][0]
        test_ibill2 = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=False, begin=str(time), end=str(time+1))['data'][0]
        assert test_ibill['ctime'] <= test_ibill2['ctime'] >= time

    def test_10(self):
        """ Begin + End filter test. Begin = ibill ctime = end. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time))['data']
        assert not test_ibill

    def test_11(self):
        """ Begin filter test. Begin is int value. """
        time = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        r = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, begin=time)
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'begin', 'reason': "'begin' must not be of 'int' type",
                                           'value': time}}, r

    def test_12(self):
        """ End filter test. End is invalidate value. """
        r = user1.merchant1.ibill_history(ord_by='ctime', ord_dir=True, end='now')
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'end', 'reason': "Should be an Integer"}}, r

    def test_13(self):
        """ Success curr filter test. """
        curr = 'USD'
        ibill = user1.merchant1.ibill_history(curr=curr)['data'][0]
        assert ibill['curr'] == curr, ibill

    def test_14(self):
        """ Unknown curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.ibill_history(curr=curr)
        assert ibill['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                  'data': {'field': 'curr', 'reason': 'Invalid currency name'}}

    def test_15(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history()['data'][1]
        test_ibill = user1.merchant1.ibill_history(first='1')['data'][0]
        assert ibill == test_ibill

    def test_16(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first=1)
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                           'value': 1}}

    def test_17(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first='one')
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': "Should be an Integer"}}

    def test_18(self):
        """ First filter test. """
        ibill = user1.merchant1.ibill_history(first='9999999')['data']
        assert not ibill

    def test_19(self):
        """ Count filter test. """
        count = 10
        ibill = user1.merchant1.ibill_history(count=str(count))
        len = ibill['data'].__len__()
        assert len == count or len == ibill['total']

    def test_20(self):
        """ Count filter test. """
        count = 0
        ibill = user1.merchant1.ibill_history(count=str(count))
        assert ibill['error'] == {'code': -32002, 'message': 'EParamInvalid',
                                  'data': {'field': 'count', 'reason': 'Should be more than zero'}}

    def test_21(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = None
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_22(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = False
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_23(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = True
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] <= r[1]['ctime'], r

    def test_24(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'amount'
        ord_dir = None
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['amount']) >= float(r[1]['amount']), r

    def test_25(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'amount'
        ord_dir = False
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['amount']) >= float(r[1]['amount']), r

    def test_26(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'amount'
        ord_dir = True
        r = user1.merchant1.ibill_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['amount']) <= float(r[1]['amount']), r

    def test_27(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'time'
        r = user1.merchant1.ibill_history(ord_by=ord_by)
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'ord_by', 'reason': 'Invalid ord_by value', 'value': 'time'}}, r

    def test_28(self):
        """ ord_by and ord_dir filter test. """
        r = user1.merchant1.ibill_history(ord_dir=123)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'ord_dir','reason': "'ord_dir' must not be of 'int' type",
                                       'value': 123}}, r

    def test_29(self):
        """ Success "inpay" group filter. """
        r = user1.merchant1.ibill_history(group='inpay')['data'][0]
        assert r['tp'] in ['payin', 'autopayin', 'transferreceive']

    def test_30(self):
        """ Success "outpay" group filter. """
        r = user1.merchant1.ibill_history(group='outpay')['data'][0]
        assert r['tp'] in ['payout', 'payoutrenumeration', 'transfer', 'transferrollback']

    def test_31(self):
        """ Success "convert" group filter. """
        r = user1.merchant1.ibill_history(group='convert')['data'][0]
        assert r['tp'] in ['convert', 'convertreceive', 'convertrenumeration']

    def test_32(self):
        """ Wrong group filter. """
        r = user1.merchant1.ibill_history(group='all')
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'group', 'reason': 'Invalid group name'}}

    def test_33(self):
        """ Success lid filter. """
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': 100})[1]['lid'])
        r = user1.merchant1.ibill_history(lid=lid)
        for i in range(r['total']):
            assert r['data'][i]['lid'] == int(lid), r['data'][i]

    def test_34(self):
        """ Wrong lid filter. Order without ibill """
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'status': 0, 'tp': 0})[1]['lid'])
        r = user1.merchant1.ibill_history(lid=lid)
        assert r['total'] == 0

    def test_35(self):
        """ Wrong lid filter. unknown Order  """
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant2.id, 'status': 100, 'tp': 20})[1]['lid'])
        r = user1.merchant1.ibill_history(lid=lid)
        assert r['total'] == 0

    def test_36(self):
        """ Wrong lid filter. unknown Order  """
        r = user1.merchant1.ibill_history(lid=100)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'lid', 'reason': "'lid' must not be of 'int' type", 'value': 100}}

    def test_37(self):
        """ Wrong lid filter. unknown Order  """
        r = user1.merchant1.ibill_history(lid='qwerty')
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'lid', 'reason': 'Should be an Integer'}}

    def test_38(self):
        """ Success amount filter. Amount = 0.01 """
        r = user1.merchant1.ibill_history(filter_amount='0.01')['data'][0]
        assert r['amount'] == '0.01'

    def test_39(self):
        """ Success amount filter. Amount = +0.01 """
        r = user1.merchant1.ibill_history(filter_amount='+0.01')['data'][0]
        assert r['amount'] == '0.01'

    def test_40(self):
        """ Success amount filter. Amount = -0.01 """
        r = user1.merchant1.ibill_history(filter_amount='-0.01')['data'][0]
        assert r['amount'] == '-0.01'

    def test_41(self):
        """ Success amount filter. Amount = =0.01 """
        r = user1.merchant1.ibill_history(filter_amount='=0.01')['data'][0]
        assert r['amount'] == '0.01'

    def test_42(self):
        """ Success amount filter. Amount = =+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='=+0.01')['data'][0]
        assert r['amount'] == '0.01'

    def test_43(self):
        """ Success amount filter. Amount = =-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='=-0.01')['data'][0]
        assert r['amount'] == '-0.01'

    def test_44(self):
        """ Success amount filter. Amount = >=0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>=0.01')['data'][0]
        assert r['amount'] >= '0.01'

    def test_45(self):
        """ Success amount filter. Amount = >=+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>=+0.01')['data'][0]
        assert r['amount'] >= '0.01'

    def test_46(self):
        """ Success amount filter. Amount = >=-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>=-0.01')['data'][0]
        assert float(r['amount']) >= -0.01

    def test_47(self):
        """ Success amount filter. Amount = <=0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<=0.01')['data'][0]
        assert r['amount'] <= '0.01'

    def test_48(self):
        """ Success amount filter. Amount = <=+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<=+0.01')['data'][0]
        assert r['amount'] <= '0.01'

    def test_49(self):
        """ Success amount filter. Amount = <=-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<=-0.01')['data'][0]
        assert float(r['amount']) <= -0.01

    def test_50(self):
        """ Success amount filter. Amount = <0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<0.01')['data'][0]
        assert r['amount'] < '0.01'

    def test_51(self):
        """ Success amount filter. Amount = <+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<+0.01')['data'][0]
        assert r['amount'] < '0.01'

    def test_52(self):
        """ Success amount filter. Amount = <-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='<-0.01')['data'][0]
        assert float(r['amount']) < -0.01

    def test_53(self):
        """ Success amount filter. Amount = >0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>0.01')['data'][0]
        assert r['amount'] > '0.01'

    def test_54(self):
        """ Success amount filter. Amount = >+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>+0.01')['data'][0]
        assert r['amount'] > '0.01'

    def test_55(self):
        """ Success amount filter. Amount = >-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='>-0.01')['data'][0]
        assert float(r['amount']) > -0.01

    def test_56(self):
        """ Success amount filter. Amount = !=0.01 """
        r = user1.merchant1.ibill_history(filter_amount='!=0.01')['data'][0]
        assert r['amount'] != '0.01'

    def test_57(self):
        """ Success amount filter. Amount = !=+0.01 """
        r = user1.merchant1.ibill_history(filter_amount='!=+0.01')['data'][0]
        assert r['amount'] != '0.01'

    def test_58(self):
        """ Success amount filter. Amount = !=-0.01 """
        r = user1.merchant1.ibill_history(filter_amount='!=-0.01')['data'][0]
        assert float(r['amount']) != -0.01

    def test_59(self):
        """ Wrong amount filter. """
        r = user1.merchant1.ibill_history(filter_amount='!=')
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'amount', 'reason': 'Invalid amount value', 'value': '!='}}

    def test_60(self):
        """ Wrong amount filter. """
        r = user1.merchant1.ibill_history(filter_amount='10+5')
        assert r['error'] == {'code': -32016, 'message': 'EParamFieldInvalid',
                              'data': {'reason': 'Format of string has to match the pattern <operand><comma><number>,'
                                                 ' e.g. ">123.45"', 'value': '10+5'}}

    def test_61(self):
        """ Success fee filter. fee = 1.5 """
        r = user1.merchant1.ibill_history(filter_fee='1.5')['data'][0]
        assert r['fee'] == '1.5'

    def test_62(self):
        """ Success fee filter. fee = +1.5 """
        r = user1.merchant1.ibill_history(filter_fee='+1.5')['data'][0]
        assert r['fee'] == '1.5'

    def test_63(self):
        """ Success fee filter. fee = 0 """
        r = user1.merchant1.ibill_history(filter_fee='0')['data'][0]
        assert r['fee'] == '0'

    def test_64(self):
        """ Success fee filter. fee = =1.5 """
        r = user1.merchant1.ibill_history(filter_fee='=1.5')['data'][0]
        assert r['fee'] == '1.5'

    def test_65(self):
        """ Success fee filter. fee = =+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='=+1.5')['data'][0]
        assert r['fee'] == '1.5'

    def test_66(self):
        """ Success fee filter. fee = =0 """
        r = user1.merchant1.ibill_history(filter_fee='=0')['data'][0]
        assert r['fee'] == '0'

    def test_67(self):
        """ Success fee filter. fee = >=1.5 """
        r = user1.merchant1.ibill_history(filter_fee='>=1.5')['data'][0]
        assert r['fee'] >= '1.5'

    def test_68(self):
        """ Success fee filter. fee = >=+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='>=+1.5')['data'][0]
        assert r['fee'] >= '1.5'

    def test_69(self):
        """ Success fee filter. fee = >=0 """
        r = user1.merchant1.ibill_history(filter_fee='>=0')['data'][0]
        assert float(r['fee']) >= 0

    def test_70(self):
        """ Success fee filter. fee = <=1.5 """
        r = user1.merchant1.ibill_history(filter_fee='<=1.5')['data'][0]
        assert r['fee'] <= '1.5'

    def test_71(self):
        """ Success fee filter. fee = <=+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='<=+1.5')['data'][0]
        assert r['fee'] <= '1.5'

    def test_72(self):
        """ Success fee filter. fee = <=0 """
        r = user1.merchant1.ibill_history(filter_fee='<=0')['data'][0]
        assert float(r['fee']) <= 0

    def test_73(self):
        """ Success fee filter. fee = <1.5 """
        r = user1.merchant1.ibill_history(filter_fee='<1.5')['data'][0]
        assert r['fee'] < '1.5'

    def test_74(self):
        """ Success fee filter. fee = <+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='<+1.5')['data'][0]
        assert r['fee'] < '1.5'

    def test_75(self):
        """ Success fee filter. fee = >1.5 """
        r = user1.merchant1.ibill_history(filter_fee='>1.5')['data'][0]
        assert r['fee'] > '1.5'

    def test_76(self):
        """ Success fee filter. fee = >+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='>+1.5')['data'][0]
        assert r['fee'] > '1.5'

    def test_77(self):
        """ Success fee filter. fee = >0 """
        r = user1.merchant1.ibill_history(filter_fee='>0')['data'][0]
        assert float(r['fee']) > 0

    def test_78(self):
        """ Success fee filter. fee = !=1.5 """
        r = user1.merchant1.ibill_history(filter_fee='!=1.5')['data'][0]
        assert r['fee'] != '1.5'

    def test_79(self):
        """ Success fee filter. fee = !=+1.5 """
        r = user1.merchant1.ibill_history(filter_fee='!=+1.5')['data'][0]
        assert r['fee'] != '1.5'

    def test_80(self):
        """ Success fee filter. fee = !=0 """
        r = user1.merchant1.ibill_history(filter_fee='!=0')['data'][0]
        assert float(r['fee']) != 0

    def test_81(self):
        """ Wrong fee filter. """
        r = user1.merchant1.ibill_history(filter_fee='!=')
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'fee', 'reason': 'Invalid fee value', 'value': '!='}}

    def test_82(self):
        """ Wrong fee filter. """
        r = user1.merchant1.ibill_history(filter_fee='10+5')
        assert r['error'] == {'code': -32016, 'message': 'EParamFieldInvalid',
                              'data': {'reason': 'Format of string has to match the pattern <operand><comma><number>,'
                                                 ' e.g. ">123.45"', 'value': '10+5'}}

class TestInpayHistory:
    """ inpay_history """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success request with no filter. """
        r = user1.merchant1.inpay_history()['data'][0]
        assert r['tp'] == 'payin'

    def test_2(self):
        """ Success payway filter. """
        r = user1.merchant1.inpay_history(payway='btc')['data'][0]
        assert r['tp'] == 'payin'
        assert r['payway_name'] == 'btc'

    def test_3(self):
        """ Unknown payway filter. """
        r = user1.merchant1.inpay_history(payway='Termynal')
        assert r['error'] == {'code': -32081, 'message': 'EParamPaywayInvalid',
                              'data': {'field': 'payway', 'reason': 'Invalid payway name'}}

    def test_4(self):
        """ Unknown payway filter. """
        r = user1.merchant1.inpay_history(payway=101)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'payway', 'reason': "'payway' must not be of 'int' type", 'value': 101}}

    def test_5(self):
        """ Success "unfinished" status filter. """
        r = user1.merchant1.inpay_history(status='unfinished')['data'][0]
        assert r['tp'] == 'payin'
        assert r['status'] in ['new', 'prereq', 'pending', 'started', 'accepted', 'wait', 'retry', 'confirmed',
                               'wtf', 'final']

    def test_6(self):
        """ Success "done" status filter. """
        r = user1.merchant1.inpay_history(status='done')['data'][0]
        assert r['tp'] == 'payin'
        assert r['status'] == 'done'

    def test_7(self):
        """ Success "fail" status filter. """
        r = user1.merchant1.inpay_history(status='fail')['data'][0]
        assert r['tp'] == 'payin'
        assert r['status'] in ['fail', 'reject']

    def test_8(self):
        """ Inpay count comparison. """
        admin_count = int(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': 0})[0]['count'])
        assert admin_count == user1.merchant1.inpay_history()['total']

    def test_9(self):
        """ Ibill [0] comparison. """
        ibill = user1.merchant1.inpay_history()['data'][0]
        assert admin.get_order(selector={'merchant_id': user1.merchant1.id, 'lid':ibill['lid'], 'tp': 0}) \
               != 'No ibills for this query.'

    def test_10(self):
        """ Begin filter test. Begin = ibill ctime. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_11(self):
        """ Begin filter test. Begin = ibill ctime -1. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_12(self):
        """ Begin filter test. Begin = ibill ctime +1. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_13(self):
        """ End filter test. End = ibill ctime. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_14(self):
        """ End filter test. End = ibill ctime -1. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_15(self):
        """ End filter test. End = ibill ctime +1. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_16(self):
        """ Begin + End filter test. Begin = ibill ctime, end = ibill ctime +1. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time+1))['data'][0]
        test_ibill2 = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=False, begin=str(time), end=str(time+1))['data'][0]
        assert test_ibill['ctime'] <= test_ibill2['ctime'] >= time

    def test_17(self):
        """ Begin + End filter test. Begin = ibill ctime = end. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time))['data']
        assert not test_ibill

    def test_18(self):
        """ Begin filter test. Begin is int value. """
        time = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        r = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, begin=time)
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'begin', 'reason': "'begin' must not be of 'int' type",
                                           'value': time}}, r

    def test_19(self):
        """ End filter test. End is invalidate value. """
        r = user1.merchant1.inpay_history(ord_by='ctime', ord_dir=True, end='now')
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'end', 'reason': 'Should be an Integer'}}, r

    def test_20(self):
        """ Success curr filter test. """
        curr = 'USD'
        ibill = user1.merchant1.inpay_history(curr=curr)['data'][0]
        assert ibill['in_curr'] == curr, ibill

    def test_21(self):
        """ Unknown curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.inpay_history(curr=curr)
        assert ibill['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                  'data': {'field': 'in_curr', 'reason': 'Invalid currency name'}}

    def test_22(self):
        """ First filter test. """
        ibill = user1.merchant1.inpay_history()['data'][1]
        test_ibill = user1.merchant1.inpay_history(first='1')['data'][0]
        assert ibill == test_ibill

    def test_23(self):
        """ First filter test. """
        ibill = user1.merchant1.inpay_history(first=1)
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                           'value': 1}}

    def test_24(self):
        """ First filter test. """
        ibill = user1.merchant1.inpay_history(first='one')
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': 'Should be an Integer'}}

    def test_25(self):
        """ First filter test. """
        ibill = user1.merchant1.inpay_history(first='9999999')['data']
        assert not ibill

    def test_26(self):
        """ Count filter test. """
        count = 10
        ibill = user1.merchant1.inpay_history(count=str(count))
        len = ibill['data'].__len__()
        assert len == count or len == ibill['total']

    def test_27(self):
        """ Count filter test. """
        ibill = user1.merchant1.inpay_history(count='0')
        assert ibill['error'] == {'code': -32002, 'message': 'EParamInvalid',
                                  'data': {'field': 'count', 'reason': 'Should be more than zero'}}

    def test_28(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = None
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_29(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = False
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_30(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = True
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] <= r[1]['ctime'], r

    def test_31(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'in_amount'
        ord_dir = None
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['in_amount']) >= float(r[1]['in_amount']), r

    def test_32(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'in_amount'
        ord_dir = False
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['in_amount']) >= float(r[1]['in_amount']), r

    def test_33(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'in_amount'
        ord_dir = True
        r = user1.merchant1.inpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['in_amount']) <= float(r[1]['in_amount']), r

    def test_34(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'time'
        r = user1.merchant1.inpay_history(ord_by=ord_by)
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'ord_by', 'reason': 'Invalid ord_by value', 'value': 'time'}}, r

    def test_35(self):
        """ ord_by and ord_dir filter test. """
        r = user1.merchant1.inpay_history(ord_dir=123)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'ord_dir', 'reason': "'ord_dir' must not be of 'int' type",
                                       'value': 123}}, r

    @pytest.mark.usefixtures('create_payin_with_uaccount')
    def test_36(self):
        r = user1.merchant1.inpay_history(uaccount='5168********7159')['data']
        assert '5168********7159' == r[0]['userdata']['payer'], r

    def test_37(self):
        r = user1.merchant1.inpay_history(uaccount='5168')['data']
        assert '5168' in r[0]['userdata']['payer'], r

    def test_38(self):
        r = user1.merchant1.inpay_history(uaccount='68**')['data']
        assert '68**' in r[0]['userdata']['payer'], r

    def test_39(self):
        r = user1.merchant1.inpay_history(uaccount='7159')['data']
        assert '7159' in r[0]['userdata']['payer'], r

    def test_40(self):
        r = user1.merchant1.inpay_history(uaccount='test88')['data']
        assert r == [], r

    def test_41(self):
        r = user1.merchant1.inpay_history(uaccount=5168)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'uaccount', 'reason': "'uaccount' must not be of 'int' type",
                                       'value': 5168}}, r

class TestOutpayHistory:
    """ outpay_history """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success request with no filter. """
        r = user1.merchant1.outpay_history()['data'][0]
        assert r['tp'] == 'payout'

    def test_2(self):
        """ Success payway filter. """
        r = user1.merchant1.outpay_history(payway='anycash')['data'][0]
        assert r['tp'] == 'payout'
        assert r['payway_name'] == 'anycash'

    def test_3(self):
        """ Unknown payway filter. """
        r = user1.merchant1.outpay_history(payway='Termynal')
        assert r['error'] == {'code': -32081, 'message': 'EParamPaywayInvalid',
                              'data': {'field': 'payway', 'reason': 'Invalid payway name'}}

    def test_4(self):
        """ Unknown payway filter. """
        r = user1.merchant1.outpay_history(payway=101)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'payway', 'reason': "'payway' must not be of 'int' type", 'value': 101}}

    def test_5(self):
        """ Success "unfinished" status filter. """
        r = user1.merchant1.outpay_history(status='unfinished')['data'][0]
        assert r['tp'] == 'payout'
        assert r['status'] in ['new', 'prereq', 'pending', 'started', 'accepted', 'wait', 'retry', 'confirmed',
                               'wtf', 'final']

    def test_6(self):
        """ Success "done" status filter. """
        r = user1.merchant1.outpay_history(status='done')['data'][0]
        assert r['tp'] == 'payout'
        assert r['status'] == 'done'

    def test_7(self):
        """ Success "fail" status filter. """
        r = user1.merchant1.outpay_history(status='fail')['data'][0]
        assert r['tp'] == 'payout'
        assert r['status'] in ['fail', 'reject']

    def test_8(self):
        """ Inpay count comparison. """
        admin_count = int(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': 10})[0]['count'])
        assert admin_count == user1.merchant1.outpay_history()['total']

    def test_9(self):
        """ Ibill [0] comparison. """
        ibill = user1.merchant1.outpay_history()['data'][0]
        assert admin.get_order(selector={'merchant_id': user1.merchant1.id, 'lid':ibill['lid'], 'tp': 10}) \
               != 'No ibills for this query.'

    def test_10(self):
        """ Begin filter test. Begin = ibill ctime. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_11(self):
        """ Begin filter test. Begin = ibill ctime -1. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_12(self):
        """ Begin filter test. Begin = ibill ctime +1. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_13(self):
        """ End filter test. End = ibill ctime. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_14(self):
        """ End filter test. End = ibill ctime -1. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_15(self):
        """ End filter test. End = ibill ctime +1. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_16(self):
        """ Begin + End filter test. Begin = ibill ctime, end = ibill ctime +1. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time+1))['data'][0]
        test_ibill2 = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=False, begin=str(time), end=str(time+1))['data'][0]
        assert test_ibill['ctime'] <= test_ibill2['ctime'] >= time

    def test_17(self):
        """ Begin + End filter test. Begin = ibill ctime = end. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time))['data']
        assert not test_ibill

    def test_18(self):
        """ Begin filter test. Begin is int value. """
        time = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        r = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, begin=time)
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'begin', 'reason': "'begin' must not be of 'int' type",
                                           'value': time}}, r

    def test_19(self):
        """ End filter test. End is invalidate value. """
        r = user1.merchant1.outpay_history(ord_by='ctime', ord_dir=True, end='now')
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'end', 'reason': 'Should be an Integer'}}, r

    def test_20(self):
        """ Success curr filter test. """
        curr = 'UAH'
        ibill = user1.merchant1.outpay_history(curr=curr)['data'][0]
        assert ibill['out_curr'] == curr, ibill

    def test_21(self):
        """ Unknown curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.outpay_history(curr=curr)
        assert ibill['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                  'data': {'field': 'out_curr', 'reason': 'Invalid currency name'}}

    def test_22(self):
        """ First filter test. """
        ibill = user1.merchant1.outpay_history()['data'][1]
        test_ibill = user1.merchant1.outpay_history(first='1')['data'][0]
        assert ibill == test_ibill

    def test_23(self):
        """ First filter test. """
        ibill = user1.merchant1.outpay_history(first=1)
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                           'value': 1}}

    def test_24(self):
        """ First filter test. """
        ibill = user1.merchant1.outpay_history(first='one')
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': 'Should be an Integer'}}

    def test_25(self):
        """ First filter test. """
        ibill = user1.merchant1.outpay_history(first='9999999')['data']
        assert not ibill

    def test_26(self):
        """ Count filter test. """
        count = 10
        ibill = user1.merchant1.outpay_history(count=str(count))
        len = ibill['data'].__len__()
        assert len == count or len == ibill['total']

    def test_27(self):
        """ Count filter test. """
        ibill = user1.merchant1.outpay_history(count='0')
        assert ibill['error'] == {'code': -32002, 'message': 'EParamInvalid',
                                  'data': {'field': 'count', 'reason': 'Should be more than zero'}}

    def test_28(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = None
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_29(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = False
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_30(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = True
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] <= r[1]['ctime'], r

    def test_31(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = None
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) >= float(r[1]['out_amount']), r

    def test_32(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = False
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) >= float(r[1]['out_amount']), r

    def test_33(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = True
        r = user1.merchant1.outpay_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) <= float(r[1]['out_amount']), r

    def test_34(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'time'
        r = user1.merchant1.outpay_history(ord_by=ord_by)
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'ord_by', 'reason': 'Invalid ord_by value', 'value': 'time'}}, r

    def test_35(self):
        """ ord_by and ord_dir filter test. """
        ord_dir = 123
        r = user1.merchant1.outpay_history(ord_dir=ord_dir)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'ord_dir', 'reason': "'ord_dir' must not be of 'int' type",
                                       'value': 123}}, r

    @pytest.mark.usefixtures('create_payout_with_uaccount')
    def test_36(self):
        r = user1.merchant1.outpay_history(uaccount='+380666789567')['data']
        assert '+380666789567' == r[0]['userdata']['contact'], r

    def test_37(self):
        r = user1.merchant1.outpay_history(uaccount='066')['data']
        assert '066' in r[0]['userdata']['contact'], r

    def test_38(self):
        r = user1.merchant1.outpay_history(uaccount='6789')['data']
        assert '6789' in r[0]['userdata']['contact'], r

    def test_39(self):
        r = user1.merchant1.outpay_history(uaccount='567')['data']
        assert '567' in r[0]['userdata']['contact'], r

    def test_40(self):
        r = user1.merchant1.outpay_history(uaccount='test123409')['data']
        assert r == [], r

    def test_41(self):
        r = user1.merchant1.outpay_history(uaccount=380666789567)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'uaccount', 'reason': "'uaccount' must not be of 'int' type",
                                       'value': 380666789567}}, r

class TestConvertHistory:
    """ outpay_history """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success request with no filter. """
        r = user1.merchant1.convert_history()['data'][0]
        assert r['tp'] == 'convert'

    def test_2(self):
        """ Success "unfinished" status filter. """
        r = user1.merchant1.convert_history(status='unfinished')['data'][0]
        assert r['tp'] == 'convert'
        assert r['status'] in ['new', 'prereq', 'pending', 'started', 'accepted', 'wait', 'retry', 'confirmed',
                               'wtf', 'final']

    def test_3(self):
        """ Success "done" status filter. """
        r = user1.merchant1.convert_history(status='done')['data'][0]
        assert r['tp'] == 'convert'
        assert r['status'] == 'done'

    def test_4(self):
        """ Success "fail" status filter. """
        r = user1.merchant1.convert_history(status='fail')['data'][0]
        assert r['tp'] == 'convert'
        assert r['status'] in ['fail', 'reject']

    def test_5(self):
        """ Inpay count comparison. """
        admin_count = int(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': 20})[0]['count'])
        assert admin_count == user1.merchant1.convert_history()['total']

    def test_6(self):
        """ Ibill [0] comparison. """
        ibill = user1.merchant1.convert_history()['data'][0]
        assert admin.get_order(selector={'merchant_id': user1.merchant1.id, 'lid':ibill['lid'], 'tp': 20}) \
               != 'No ibills for this query.'

    def test_7(self):
        """ Begin filter test. Begin = ibill ctime. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_8(self):
        """ Begin filter test. Begin = ibill ctime -1. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_9(self):
        """ Begin filter test. Begin = ibill ctime +1. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=str(time))['data'][0]
        assert test_ibill['ctime'] >= time

    def test_10(self):
        """ End filter test. End = ibill ctime. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_11(self):
        """ End filter test. End = ibill ctime -1. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']-1
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_12(self):
        """ End filter test. End = ibill ctime +1. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']+1
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=False, end=str(time))['data'][0]
        assert test_ibill['ctime'] < time

    def test_13(self):
        """ Begin + End filter test. Begin = ibill ctime, end = ibill ctime +1. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time+1))['data'][0]
        test_ibill2 = user1.merchant1.convert_history(ord_by='ctime', ord_dir=False, begin=str(time), end=str(time+1))['data'][0]
        assert test_ibill['ctime'] <= test_ibill2['ctime'] >= time

    def test_14(self):
        """ Begin + End filter test. Begin = ibill ctime = end. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        test_ibill = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=str(time), end=str(time))['data']
        assert not test_ibill

    def test_15(self):
        """ Begin filter test. Begin is int value. """
        time = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True)['data'][1]['ctime']
        r = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, begin=time)
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'begin', 'reason': "'begin' must not be of 'int' type",
                                           'value': time}}, r

    def test_16(self):
        """ End filter test. End is invalidate value. """
        r = user1.merchant1.convert_history(ord_by='ctime', ord_dir=True, end='now')
        assert r.get('error') == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'end', 'reason': 'Should be an Integer'}}, r

    def test_17(self):
        """ Success in_curr filter test. """
        curr = 'UAH'
        ibill = user1.merchant1.convert_history(in_curr=curr)['data'][0]
        assert ibill['in_curr'] == curr, ibill

    def test_18(self):
        """ Unknown curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.convert_history(in_curr=curr)
        assert ibill['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                  'data': {'field': 'in_curr', 'reason': 'Invalid currency name'}}

    def test_19(self):
        """ Success out_curr filter test. """
        curr = 'UAH'
        ibill = user1.merchant1.convert_history(out_curr=curr)['data'][0]
        assert ibill['out_curr'] == curr, ibill

    def test_20(self):
        """ Unknown out_curr filter test. """
        curr = 'ГРН'
        ibill = user1.merchant1.convert_history(out_curr=curr)
        assert ibill['error'] == {'code': -32014, 'message': 'EParamCurrencyInvalid',
                                  'data': {'field': 'out_curr', 'reason': 'Invalid currency name'}}

    def test_21(self):
        """ First filter test. """
        ibill = user1.merchant1.convert_history()['data'][1]
        test_ibill = user1.merchant1.convert_history(first='1')['data'][0]
        assert ibill == test_ibill

    def test_22(self):
        """ First filter test. """
        ibill = user1.merchant1.convert_history(first=1)
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                           'value': 1}}

    def test_23(self):
        """ First filter test. """
        ibill = user1.merchant1.convert_history(first='one')
        assert ibill['error'] == {'code': -32003, 'message': 'EParamType',
                                  'data': {'field': 'first', 'reason': 'Should be an Integer'}}

    def test_24(self):
        """ First filter test. """
        ibill = user1.merchant1.convert_history(first='9999999')['data']
        assert not ibill

    def test_25(self):
        """ Count filter test. """
        count = 10
        ibill = user1.merchant1.convert_history(count=str(count))
        len = ibill['data'].__len__()
        assert len == count or len == ibill['total']

    def test_26(self):
        """ Count filter test. """
        ibill = user1.merchant1.convert_history(count='0')
        assert ibill['error'] == {'code': -32002, 'message': 'EParamInvalid',
                                  'data': {'field': 'count', 'reason': 'Should be more than zero'}}

    def test_27(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = None
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_28(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = False
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] >= r[1]['ctime'], r

    def test_29(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'ctime'
        ord_dir = True
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert r[0]['ctime'] <= r[1]['ctime'], r

    def test_30(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = None
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) >= float(r[1]['out_amount']), r

    def test_31(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = False
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) >= float(r[1]['out_amount']), r

    def test_32(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'out_amount'
        ord_dir = True
        r = user1.merchant1.convert_history(ord_by=ord_by, ord_dir=ord_dir)['data']
        assert float(r[0]['out_amount']) <= float(r[1]['out_amount']), r

    def test_33(self):
        """ ord_by and ord_dir filter test. """
        ord_by = 'time'
        r = user1.merchant1.convert_history(ord_by=ord_by)
        assert r['error'] == {'code': -32002, 'message': 'EParamInvalid',
                              'data': {'field': 'ord_by', 'reason': 'Invalid ord_by value', 'value': 'time'}}, r

    def test_34(self):
        """ ord_by and ord_dir filter test. """
        r = user1.merchant1.convert_history(ord_dir=123)
        assert r['error'] == {'code': -32003, 'message': 'EParamType',
                              'data': {'field': 'ord_dir', 'reason': "'ord_dir' must not be of 'int' type",
                                       'value': 123}}, r

class TestCurrencyList:
    """ CurrencyList """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_CurrencyList_1(self):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='BTC', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='BCHABC', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='ETH', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='USDT', is_disabled=False, is_active=True)
        admin.set_currency_activity(name='LTC', is_disabled=False, is_active=True)
        assert user1.merchant1.currency_list()['result'] == \
               {'BCHABC': {'admin_max': '3',
                           'admin_min': '0.000001',
                           'is_crypto': True,
                           'precision': 8},
                'BTC': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'ETH': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'LTC': {'admin_max': '3',
                        'admin_min': '0.000001',
                        'is_crypto': True,
                        'precision': 8},
                'RUB': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'UAH': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'USD': {'admin_max': '3000',
                        'admin_min': '0.01',
                        'is_crypto': False,
                        'precision': 2},
                'USDT': {'admin_max': '3',
                         'admin_min': '0.000001',
                         'is_crypto': True,
                         'precision': 8}}

    def test_CurrencyList_2(self, _enable_currency):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='USD', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='BTC', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='RUB', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='BCHABC', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='ETH', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='USDT', is_disabled=False, is_active=False)
        admin.set_currency_activity(name='LTC', is_disabled=False, is_active=False)
        user1.merchant1.currency_list()
        # pprint.pprint(user1.merchant1.resp_currency_list)
        assert user1.merchant1.resp_currency_list['error']['code'] == -32090
        assert user1.merchant1.resp_currency_list['error']['message'] == 'EParamNotFound'
        assert user1.merchant1.resp_currency_list['error']['data']['field'] == 'currency'
        assert user1.merchant1.resp_currency_list['error']['data']['reason'] == 'Not found'

    def test_CurrencyList_3(self, _enable_currency):
        """ Currency List. """
        admin.set_currency_activity(name='UAH', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='USD', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='BTC', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='RUB', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='BCHABC', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='ETH', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='USDT', is_disabled=True, is_active=True)
        admin.set_currency_activity(name='LTC', is_disabled=True, is_active=True)
        user1.merchant1.currency_list()
        # pprint.pprint(user1.merchant1.resp_currency_list)
        assert user1.merchant1.resp_currency_list['error']['code'] == -32090
        assert user1.merchant1.resp_currency_list['error']['message'] == 'EParamNotFound'
        assert user1.merchant1.resp_currency_list['error']['data']['field'] == 'currency'
        assert user1.merchant1.resp_currency_list['error']['data']['reason'] == 'Not found'

class TestPaywayList:
    """ PaywayLis """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000))
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3))

    def test_PaywayList_1(self):
        """ Payway List. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdterc20']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['bchabc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_moscow']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc_p2p']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdt']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['nixmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['tinkoff_cs']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['anycash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['alfa_bank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['vtb24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['advcash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['monobank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['sberbank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC',
                                     is_active=True, tech_min=bl(0.000001), tech_max=bl(3))
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_fee(tp=10, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'],
                      merchant_id=user1.merchant1.id)
        admin.set_fee(tp=10, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(tp=10, currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'],
                      merchant_id=user1.merchant1.id)
        admin.set_fee(tp=10, currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(tp=0, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(mult=bl(0.05), add=bl(2), _min=0, _max=0, tp=0, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'])
        # adm_list = {dct['name'] for dct in admin.get_model(model='payway', _filter='is_active', value=True)}
        # pprint.pprint(adm_list)
        user1.merchant1.payway_list()
        pprint.pprint(user1.merchant1.resp_payway_list)
        assert user1.merchant1.resp_payway_list['result'] == {'btc': {'currencies': [{'fee': {},
                                    'is_crypto': True,
                                    'is_out': True,
                                    'name': 'BTC',
                                    'precision': 8,
                                    'tech_max': '3',
                                    'tech_min': '0.000001'},
                                   {'fee': {'add': '0',
                                            'max': '0',
                                            'method': 'ceil',
                                            'min': '0',
                                            'mult': '0'},
                                    'is_crypto': True,
                                    'is_out': False,
                                    'name': 'BTC',
                                    'precision': 8,
                                    'tech_max': '1',
                                    'tech_min': '0.0008'}],
                    'is_active': True,
                    'is_public': True,
                    'type': 'crypto'},
            'cash_kiev': {'currencies': [{'fee': {'add': '2',
                                                  'max': '0',
                                                  'method': 'ceil',
                                                  'min': '0',
                                                  'mult': '0.1'},
                                          'is_crypto': False,
                                          'is_out': True,
                                          'name': 'USD',
                                          'precision': 2,
                                          'tech_max': '15',
                                          'tech_min': '1'},
                                         {'fee': {'add': '2',
                                                  'max': '0',
                                                  'method': 'ceil',
                                                  'min': '0',
                                                  'mult': '0.1'},
                                          'is_crypto': False,
                                          'is_out': False,
                                          'name': 'USD',
                                          'precision': 2,
                                          'tech_max': '100',
                                          'tech_min': '1'}],
                          'is_active': True,
                          'is_public': True,
                          'type': 'cash'},
            'eth': {'currencies': [{'fee': {'add': '0',
                                            'max': '0',
                                            'method': 'ceil',
                                            'min': '0',
                                            'mult': '0'},
                                    'is_crypto': True,
                                    'is_out': True,
                                    'name': 'ETH',
                                    'precision': 8,
                                    'tech_max': '0.895',
                                    'tech_min': '0.000001'},
                                   {'fee': {'add': '0',
                                            'max': '0',
                                            'method': 'ceil',
                                            'min': '0',
                                            'mult': '0'},
                                    'is_crypto': True,
                                    'is_out': False,
                                    'name': 'ETH',
                                    'precision': 8,
                                    'tech_max': '3',
                                    'tech_min': '0.000001'}],
                    'is_active': True,
                    'is_public': True,
                    'type': 'crypto'},
            'exmo': {'currencies': [{'fee': {'add': '0',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0'},
                                     'is_crypto': False,
                                     'is_out': True,
                                     'name': 'USD',
                                     'precision': 2,
                                     'tech_max': '3000',
                                     'tech_min': '0.01'},
                                    {'fee': {'add': '10',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0'},
                                     'is_crypto': False,
                                     'is_out': False,
                                     'name': 'USD',
                                     'precision': 2,
                                     'tech_max': '2',
                                     'tech_min': '0.01'},
                                    {'fee': {'add': '0',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0'},
                                     'is_crypto': False,
                                     'is_out': True,
                                     'name': 'UAH',
                                     'precision': 2,
                                     'tech_max': '15.48',
                                     'tech_min': '0.01'},
                                    {'fee': {'add': '0',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0.00011111'},
                                     'is_crypto': False,
                                     'is_out': False,
                                     'name': 'UAH',
                                     'precision': 2,
                                     'tech_max': '3000',
                                     'tech_min': '0.01'}],
                     'is_active': True,
                     'is_public': True,
                     'type': 'cheque'},
            'kuna': {'currencies': [{'fee': {'add': '0',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0.15'},
                                     'is_crypto': False,
                                     'is_out': True,
                                     'name': 'UAH',
                                     'precision': 2,
                                     'tech_max': '100',
                                     'tech_min': '1'},
                                    {'fee': {'add': '1.9',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0.1'},
                                     'is_crypto': False,
                                     'is_out': False,
                                     'name': 'UAH',
                                     'precision': 2,
                                     'tech_max': '3000',
                                     'tech_min': '100'}],
                     'is_active': True,
                     'is_public': True,
                     'type': 'cheque'},
            'ltc': {'currencies': [{'fee': {'add': '0.001',
                                            'max': '0',
                                            'method': 'ceil',
                                            'min': '0',
                                            'mult': '0'},
                                    'is_crypto': True,
                                    'is_out': True,
                                    'name': 'LTC',
                                    'precision': 8,
                                    'tech_max': '0.6',
                                    'tech_min': '0.002'},
                                   {'fee': {'add': '0.001',
                                            'max': '0',
                                            'method': 'ceil',
                                            'min': '0',
                                            'mult': '0'},
                                    'is_crypto': True,
                                    'is_out': False,
                                    'name': 'LTC',
                                    'precision': 8,
                                    'tech_max': '200',
                                    'tech_min': '0.4'}],
                    'is_active': True,
                    'is_public': True,
                    'type': 'crypto'},
            'payeer': {'currencies': [{'fee': {'add': '0.5',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'USD',
                                       'precision': 2,
                                       'tech_max': '100',
                                       'tech_min': '0.01'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': True,
                                       'name': 'USD',
                                       'precision': 2,
                                       'tech_max': '3000',
                                       'tech_min': '0.01'},
                                      {'fee': {'add': '1',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': True,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '100',
                                       'tech_min': '1'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '200',
                                       'tech_min': '1'}],
                       'is_active': True,
                       'is_public': True,
                       'type': 'sci'},
            'paymer': {'currencies': [{'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '3000',
                                       'tech_min': '0.01'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'USD',
                                       'precision': 2,
                                       'tech_max': '3000',
                                       'tech_min': '0.01'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': True,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '3000',
                                       'tech_min': '0.01'}],
                       'is_active': True,
                       'is_public': True,
                       'type': 'cheque'},
            'perfect': {'currencies': [{'fee': {'add': '2',
                                                'max': '0',
                                                'method': 'ceil',
                                                'min': '0',
                                                'mult': '0.1'},
                                        'is_crypto': False,
                                        'is_out': True,
                                        'name': 'USD',
                                        'precision': 2,
                                        'tech_max': '15',
                                        'tech_min': '1'},
                                       {'fee': {'add': '1',
                                                'max': '100',
                                                'method': 'ceil',
                                                'min': '3',
                                                'mult': '0.02'},
                                        'is_crypto': False,
                                        'is_out': False,
                                        'name': 'USD',
                                        'precision': 2,
                                        'tech_max': '100',
                                        'tech_min': '1'}],
                        'is_active': True,
                        'is_public': True,
                        'type': 'sci'},
            'privat24': {'currencies': [{'fee': {'add': '0',
                                                 'max': '0',
                                                 'method': 'ceil',
                                                 'min': '0',
                                                 'mult': '0.15'},
                                         'is_crypto': False,
                                         'is_out': False,
                                         'name': 'UAH',
                                         'precision': 2,
                                         'tech_max': '200',
                                         'tech_min': '10'},
                                        {'fee': {'add': '0',
                                                 'max': '0',
                                                 'method': 'ceil',
                                                 'min': '0',
                                                 'mult': '0.15'},
                                         'is_crypto': False,
                                         'is_out': True,
                                         'name': 'UAH',
                                         'precision': 2,
                                         'tech_max': '100',
                                         'tech_min': '1'}],
                         'is_active': True,
                         'is_public': True,
                         'type': 'sci'},
            'qiwi': {'currencies': [{'fee': {'add': '1',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0.055'},
                                     'is_crypto': False,
                                     'is_out': True,
                                     'name': 'RUB',
                                     'precision': 2,
                                     'tech_max': '100',
                                     'tech_min': '1'},
                                    {'fee': {'add': '0',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0'},
                                     'is_crypto': False,
                                     'is_out': False,
                                     'name': 'UAH',
                                     'precision': 2,
                                     'tech_max': '1000',
                                     'tech_min': '0.05'},
                                    {'fee': {'add': '1',
                                             'max': '0',
                                             'method': 'ceil',
                                             'min': '0',
                                             'mult': '0.055'},
                                     'is_crypto': False,
                                     'is_out': False,
                                     'name': 'RUB',
                                     'precision': 2,
                                     'tech_max': '1000',
                                     'tech_min': '8.449999999'}],
                     'is_active': True,
                     'is_public': True,
                     'type': 'sci'},
            'visamc': {'currencies': [{'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '3000',
                                       'tech_min': '0.01'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': True,
                                       'name': 'RUB',
                                       'precision': 2,
                                       'tech_max': '100',
                                       'tech_min': '1'},
                                      {'fee': {'add': '0',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0'},
                                       'is_crypto': False,
                                       'is_out': True,
                                       'name': 'UAH',
                                       'precision': 2,
                                       'tech_max': '100',
                                       'tech_min': '1'},
                                      {'fee': {'add': '2',
                                               'max': '0',
                                               'method': 'ceil',
                                               'min': '0',
                                               'mult': '0.05'},
                                       'is_crypto': False,
                                       'is_out': False,
                                       'name': 'UAH',
                                       'precision': 2,
                                       'tech_max': '100',
                                       'tech_min': '0.01'}],
                       'is_active': True,
                       'is_public': True,
                       'type': 'sci'},
            'webmoney': {'currencies': [],
                         'is_active': True,
                         'is_public': True,
                         'type': 'sci'}}

    def test_PaywayList_2(self, _activate_merchant_payways_after):
        """ Payway List. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdterc20']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['bchabc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_moscow']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc_p2p']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdt']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['nixmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['tinkoff_cs']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['anycash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['alfa_bank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['vtb24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['advcash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['monobank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['sberbank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=False)
        user1.merchant1.payway_list()
        # pprint.pprint(user1.merchant1.resp_payway_list)
        assert user1.merchant1.resp_payway_list['error']['code'] == -32090
        assert user1.merchant1.resp_payway_list['error']['message'] == 'EParamNotFound'
        assert user1.merchant1.resp_payway_list['error']['data']['field'] == 'payway'
        assert user1.merchant1.resp_payway_list['error']['data']['reason'] == 'Not found'

class TestExchangeList:
    """ ExchangeList """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max='3000000000000')
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max='3000000000')

    def test_ExchangeList_1(self):
        """ Exchange List. """
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
        # pprint.pprint(user1.merchant1.exchange_list()['result'])
        assert user1.merchant1.exchange_list()['result'] == \
               {'RUB-UAH': {'fee': '0',
                            'i_rate': ['2.48757', '1'],
                            'in_curr': 'RUB',
                            'in_max': '100000',
                            'in_min': '0.03',
                            'out_curr': 'UAH',
                            'out_max': '40199.87',
                            'out_min': '0.01',
                            'rate': ['2.48757', '1'],
                            'ratesource': 'minfin'},
                'UAH-RUB': {'fee': '0',
                            'i_rate': ['1', '2.46305'],
                            'in_curr': 'UAH',
                            'in_max': '40700.04',
                            'in_min': '0.01',
                            'out_curr': 'RUB',
                            'out_max': '100246.23',
                            'out_min': '0.02',
                            'rate': ['1', '2.46305'],
                            'ratesource': 'minfin'},
                'UAH-USD': {'fee': '0.04',
                            'i_rate': ['25.91463', '1'],
                            'in_curr': 'UAH',
                            'in_max': '100000',
                            'in_min': '0.26',
                            'out_curr': 'USD',
                            'out_max': '3858.82',
                            'out_min': '0.01',
                            'rate': ['26.95122', '1'],
                            'ratesource': 'minfin'},
                'USD-UAH': {'fee': '0.03',
                            'i_rate': ['1', '25.7355'],
                            'in_curr': 'USD',
                            'in_max': '3886.43',
                            'in_min': '0.01',
                            'out_curr': 'UAH',
                            'out_max': '100019.21',
                            'out_min': '0.25',
                            'rate': ['1', '24.96343'],
                            'ratesource': 'minfin'}}

    def test_ExchangeList_2(self, _enable_exchange_operation_UAH_RUB, _enable_exchange_operation_UAH_USD,
                            _enable_exchange_operation_RUB_UAH, _enable_exchange_operation_USD_UAH):
        """ Exchange List. """
        admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH',
                                tech_min=bl(0.01), tech_max=bl(3886.43), is_active=False)
        admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH',
                                tech_min=bl(0.03), tech_max=bl(100000), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD',
                                tech_min=bl(0.26), tech_max=bl(100000), is_active=False)
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB',
                                tech_min=bl(0.01), tech_max=bl(40700.04), is_active=False)
        admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='BTC', out_currency='ETH',
                                tech_min=bl(0.26), tech_max=bl(100000), is_active=False)
        admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='BTC', out_currency='USDT',
                                tech_min=bl(0.01), tech_max=bl(40700.04), is_active=False)
        user1.merchant1.exchange_list()
        # pprint.pprint(user1.merchant1.resp_exchange_list)
        assert user1.merchant1.resp_exchange_list['error']['code'] == -32090
        assert user1.merchant1.resp_exchange_list['error']['message'] == 'EParamNotFound'
        assert user1.merchant1.resp_exchange_list['error']['data']['field'] == 'exchange'
        assert user1.merchant1.resp_exchange_list['error']['data']['reason'] == 'Not found'
