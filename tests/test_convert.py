import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint


class TestConvertGet:
    """ Get convert. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success get convert"""
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': '20'})[1]['lid'])
        r = user1.merchant1.convert_get(o_lid=lid)
        assert  str(r.get('result').get('lid')) == lid, r

    def test_2(self):
        """ Request with invalidate o_lid filter"""
        r = user1.merchant1.convert_get(o_lid=10)
        assert r.get('error') == {'code': -32070, 'message': 'InvalidParam',
                                  'data': {'reason': "Key 'o_lid' must not be of 'int' type"}}, r

    def test_3(self):
        """ Request with empty o_lid filter"""
        r = user1.merchant1.convert_get(o_lid=None)
        assert r.get('error') == {'code': -32070, 'message': 'InvalidParam', 'data': {'reason': None}}, r

    def test_4(self):
        """ Request with unknown o_lid filter"""
        lid = str(admin.get_order(selector={'merchant_id': user1.merchant2.id, 'tp': '20'})[1]['lid'])
        r = user1.merchant1.convert_get(o_lid=lid)
        assert r.get('error') == {'code': -32090, 'message': 'NotFound',
                                  'data': {'reason': 'Not found order with params'}}, r

    def test_5(self):
        """ Request with unknown o_lid filter"""
        r = user1.merchant1.convert_get(o_lid='999999')
        assert r.get('error') == {'code': -32090, 'message': 'NotFound',
                                  'data': {'reason': 'Not found order with params'}}, r


class TestConvertParams:
    """ Convert Params. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Success request convert params. """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        out_curr = admin.get_currency(exchange[0].get('out_currency_id'))
        r = user1.merchant1.convert_params(in_curr=in_curr, out_curr=out_curr).get('result')
        assert r.get('in_curr') == in_curr, r
        assert r.get('out_curr') == out_curr, r
        assert r.get('is_convert') == True, r

    def test_2(self):
        """ Request convert params with in_curr = out_curr. """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        curr = admin.get_currency(exchange[0].get('in_currency_id'))
        error = user1.merchant1.convert_params(in_curr=curr, out_curr=curr).get('error')
        assert error['code'] == -32065
        assert error['message'] =='UnavailExchange'

    def test_3(self):
        """ Request convert params with inactive in_curr and out_curr. """
        exchange = admin.get_exchange(_filter='is_active', value=False)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        out_curr = admin.get_currency(exchange[0].get('out_currency_id'))
        error = user1.merchant1.convert_params(in_curr=in_curr, out_curr=out_curr).get('error')
        assert error['code'] == -32065
        assert error['message'] =='UnavailExchange'

    def test_4(self):
        """ Request convert params with invalidate out_curr """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        error = user1.merchant1.convert_params(in_curr=in_curr, out_curr='blah').get('error')
        assert error['code'] == -32076, error
        assert error['message'] =='InvalidCurrency'

    def test_5(self):
        """ Request convert params with invalidate out_curr """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        error = user1.merchant1.convert_params(in_curr=in_curr, out_curr=999).get('error')
        assert error['code'] == -32070, error
        assert error['message'] =='InvalidParam'

    def test_6(self):
        """ Request convert params with out_curr = None """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        error = user1.merchant1.convert_params(in_curr=in_curr, out_curr=None).get('error')
        assert error['code'] == -32076, error
        assert error['message'] =='InvalidCurrency'

    def test_7(self):
        """ Request convert params with out_curr and in_curr = None """
        exchange = admin.get_exchange(_filter='is_active', value=True)
        in_curr = admin.get_currency(exchange[0].get('in_currency_id'))
        error = user1.merchant1.convert_params(in_curr=None, out_curr=None).get('error')
        assert error['code'] == -32076, error
        assert error['message'] =='InvalidCurrency'


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

    # def test_3(self):
    #     """ Unknown in_curr filter test. """
    #     curr = 'ГРН'
    #     r = user1.merchant1.convert_list(in_curr=curr)
    #     assert r == {'code': -32076, 'message': 'InvalidCurrency', 'data': curr}, r

    def test_4(self):
        """ Success out_curr filter test. """
        curr = 'USD'
        r = user1.merchant1.convert_list(out_curr=curr)['data'][0]
        assert r['out_curr'] == curr, r

    # def test_5(self):
    #     """ Unknown out_curr filter test. """
    #     curr = 'ГРН'
    #     r = user1.merchant1.convert_list(out_curr=curr)
    #     assert r == {'code': -32076, 'message': 'InvalidCurrency', 'data': curr}

    def test_6(self):
        """ First filter test. """
        r = user1.merchant1.convert_list()['data'][1]
        test = user1.merchant1.convert_list(first='1')['data'][0]
        assert r == test

    def test_7(self):
        """ First filter test. """
        r = user1.merchant1.convert_list(first=1)
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': "Key 'first' must not be of 'int' type"}}

    def test_8(self):
        """ First filter test. """
        r = user1.merchant1.convert_list(first='one')
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'first - has to be an Integer'}}

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
        """ Count filter test. """
        count = 0
        r = user1.merchant1.convert_list(count=str(count))
        len = r['data'].__len__()
        assert len == 20 or len == r['total']
