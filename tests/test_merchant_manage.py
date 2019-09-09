import pytest
from users.tools import *
from users.user import User


class TestCreateMerchant:
    """ Creating merchant. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_create_1(self):
        """ Creating merchant by owner with ASCII symbols. """
        user1.merchant_create(title='Test merchant !@#$%^&*()_+ .')
        assert user1.resp_merch_create['title'] == 'Test merchant !@#$%^&*()_+ .'
        ls_param = ['apiip', 'is_active', 'lid', 'out_pay', 'pw', 'title']
        ls_param.sort()
        assert user1.merch_create_param_list == ls_param
        assert admin.get_merchant(lid=user1.merch_lid)['title'] == 'Test merchant !@#$%^&*()_+ .'
        admin.delete_merchant(lid=user1.merch_lid)

    def test_merchant_create_2(self):
        """ Creating merchant with kirrils symbols in title. """
        user1.merchant_create(title='Тестовый мерчант')
        assert user1.resp_merch_create['title'] == 'Тестовый мерчант'
        admin.delete_merchant(lid=user1.merch_lid)

    def test_merchant_create_3(self):
        """ Creating merchant with empty string. """
        user1.merchant_create(title='')
        assert user1.resp_merch_create['title'] == ''
        assert admin.get_merchant(lid=user1.merch_lid)['title'] == ''
        admin.delete_merchant(lid=user1.merch_lid)

    def test_merchant_create_4(self):
        """ Creating merchant with space in title. """
        user1.merchant_create(title=' ')
        assert user1.resp_merch_create['title'] == ' '
        assert admin.get_merchant(lid=user1.merch_lid)['title'] == ' '
        admin.delete_merchant(lid=user1.merch_lid)

    def test_merchant_create_5(self):
        """ Creating merchant without title. """
        user1.merchant_create(title=None)
        assert user1.resp_merch_create['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                                    'data': {'reason': "method 'merchant.create' missing 1 argument: 'title'"}}

    def test_merchant_create_6(self):
        """ Creating 2 merchant with equal title. """
        user1.merchant_create(title='Double title')
        user1.merchant_create(title='Double title')
        assert user1.resp_merch_create['error'] == {'code': -32033, 'message': 'ReqExcept', 'data': 'Unique'}
        admin.delete_merchant(lid=user1.merch_lid)

    def test_merchant_create_7(self):
        """ Creating 2 merchant with equal title in two different merchant. """
        user1.merchant_create(title='Title')
        user2.merchant_create(title='Title')
        assert user2.resp_merch_create['title'] == 'Title'
        admin.delete_merchant(lid=user1.merch_lid)
        admin.delete_merchant(lid=user2.merch_lid)


class TestSwitchingMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_switching_merchant_1(self):
        """ Disabling/enabling merchant. """
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=False)
        assert user1.resp_merch_switch['is_active'] is False
        assert admin.get_merchant(lid=user1.merchant2.lid)['is_active'] is True
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=True)
        assert user1.resp_merch_switch['is_active'] is True
        assert admin.get_merchant(lid=user1.merchant2.lid)['is_active'] is True
        ls_param = ['apiip', 'balances', 'is_active', 'lid', 'out_pay', 'pw', 'title']
        ls_param.sort()
        assert user1.resp_merch_switch_params == ls_param

    def test_switching_merchant_2(self):
        """ Switching merchant by not owner. """
        user1.merchant_switch(m_lid=user2.merchant1.lid, is_active=False)
        assert user1.resp_merch_switch['error'] == {'code': -32070, 'message': 'InvalidParam'}
        assert admin.get_merchant(lid=user2.merchant1.lid)['is_active'] is True

    def test_switching_merchant_3(self):
        """ Switching merchant without session token. """
        session = user1.headers['x-token']
        user1.headers['x-token'] = None
        user1.merchant_switch(m_lid=user1.merchant2.lid, is_active=False)
        assert user1.resp_merch_switch['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-token to headers'}}
        user1.headers['x-token'] = session


class TestListMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_merchant_1(self, _merchant_activate):
        """ Getting list of all merchants. """
        user1.merchant_list(first=None, count=None)
        merch_dct = {str(mr['lid']): {'is_active': mr['is_active']} for mr in user1.resp_merch_list['data']}
        print(merch_dct)
        assert merch_dct[str(user1.merchant2.lid)]['is_active'] is True
        assert merch_dct[user1.merchant1.lid]['is_active'] is False
        assert len(user1.resp_merch_list['data']) == 2

    def test_list_merchant_2(self):
        """ Getting list merchant from one element. """
        user1.merchant_list(first=None, count=None)
        full_ls = user1.resp_merch_list['data']
        user1.merchant_list(first='1', count='1')
        assert len(user1.resp_merch_list['data']) == 1
        assert full_ls[1] == user1.resp_merch_list['data'][0]
        assert 'title' in user1.resp_merch_list['data'][0]
        assert 'apiip' in user1.resp_merch_list['data'][0]
        assert 'lid' in user1.resp_merch_list['data'][0]
        assert 'pw' in user1.resp_merch_list['data'][0]
        assert 'out_pay' in user1.resp_merch_list['data'][0]
        assert 'balances' in user1.resp_merch_list['data'][0]


class TestGetMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_get_1(self, _merchant_activate):
        """ Getting information for inactive merchant without balance. """
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=False)
        list_params = ['apiip', 'is_active', 'lid', 'out_pay', 'pw', 'title']
        list_params.sort()
        resp_list_params = list(user1.resp_merch_get)
        resp_list_params.sort()
        assert user1.resp_merch_get['is_active'] is False
        assert user1.resp_merch_get['out_pay'] is True
        assert resp_list_params == list_params
        list_payway = [dct['payway_id'] for dct in admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                       if dct['is_active'] is True]
        list_payway.sort()
        resp_list_payway = [admin.payway[dct]['id'] for dct in user1.resp_merch_get['pw']]
        resp_list_payway.sort()
        assert list_payway == resp_list_payway

    def test_merchant_get_2(self, _merchant_activate):
        """ Getting information for active merchant with balance. """
        admin.set_wallet_amount(balance=30000, currency='BTC', merch_lid=user1.merchant2.lid)
        user1.merchant_get(m_lid=user1.merchant2.lid, balance=True)
        assert user1.resp_merch_get['is_active'] is True
        assert user1.resp_merch_get['out_pay'] is True
        assert user1.resp_merch_get['lid'] == int(user1.merchant2.lid)
        assert user1.resp_merch_get['balances']['BTC'] == '0.00003'

    def test_merchant_get_3(self):
        """ Getting information with NONE balance. """
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=None)
        assert 'balances' not in user1.resp_merch_get
        assert 'lid' in user1.resp_merch_get

    def test_merchant_get_4(self):
        """ Getting information with not own m_lid. """
        user1.merchant_get(m_lid=user2.merchant1.lid, balance=False)
        assert user1.resp_merch_get['error'] == {'code': -32090, 'message': 'NotFound',
                                                 'data': {'field': None, 'reason': 'Merchant with lid ' + user2.merchant1.lid + ' was not found'}}

    def test_merchant_get_5(self):
        """ Getting information with wrong merchant lid. """
        user1.merchant_get(m_lid='1', balance=False)
        assert user1.resp_merch_get['error'] == {'code': -32090, 'data': {'field': None, 'reason': 'Merchant with lid 1 was not found'},
                                                 'message': 'NotFound'}

    def test_merchant_get_6(self):
        """ Getting information without m_lid. """
        user1.merchant_get(m_lid=None, balance=False)
        assert user1.resp_merch_get['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                                 'data': {'reason': "method 'merchant.get' missing 1 argument: 'm_lid'"}}

    def test_merchant_get_7(self):
        """ Getting information with wrong session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=True)
        assert user1.resp_merch_get['error'] == {'code': -32091, 'message': 'Unauth',
                                                 'data': {'reason': 'Invalid or expired session token', 'token': '1'}}
        user1.headers['x-token'] = session

    def test_merchant_get_8(self):
        """ Getting information without session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=True)
        assert user1.resp_merch_get['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-token to headers'}}
        user1.headers['x-token'] = session


class TestMerchantGetKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_get_key_1(self):
        """ Getting key for merchant without 2 step auth. """
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['merch_token'] == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_get_key_2(self, _disable_2type):
        """ Getting key for merchant with 2 step auth. """
        user1.set_2type(tp='0')
        user1.merchant_get_key(m_lid=user1.merchant2.lid)
        assert user1.resp_merch_get_key['error']['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.get_key_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == admin.get_merchant(lid=user1.merchant2.lid)['apikey']

    def test_merchant_get_key_3(self, _merchant_activate):
        """ Getting key for inactive merchant. """
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32010, 'message': 'InvalidMerchant',
                                                     'data': {'field': None, 'reason': 'Active merchant with lid ' + user1.merchant1.lid + ' was not found'}}

    def test_merchant_get_key_4(self):
        """ Getting key for other owner. """
        user1.merchant_get_key(m_lid=user2.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32090, 'message': 'NotFound',
                                                     'data': {'field': None, 'reason': 'Merchant with lid ' + user2.merchant1.lid + ' was not found'}}

    def test_merchant_get_key_5(self):
        """ Getting key without lid. """
        user1.merchant_get_key(m_lid=None)
        assert user1.resp_merch_get_key['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                                     'data': {'reason': "method 'merchant.get_key' missing 1 argument: 'm_lid'"}}

    def test_merchant_get_key_6(self):
        """ Getting key with wrong session. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32091, 'message': 'Unauth',
                                                     'data': {'reason': 'Invalid or expired session token', 'token': '1'}}
        user1.headers['x-token'] = session

    def test_merchant_get_key_7(self):
        """ Getting key without session. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                                                     'data': {'reason': 'Add x-token to headers'}}
        user1.headers['x-token'] = session


class TestMerchantRenewKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_renew_key_1(self, _renew_key):
        """ Renew api key for owner without 2 step auth. """
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['merch_token'] == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_renew_key_2(self, _disable_2type, _renew_key):
        """ Renew api key for owner with 2 step auth. """
        user1.set_2type(tp='0')
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['error']['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.renew_key_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_renew_key_3(self, _merchant_activate):
        """ Renew key for inactive merchant. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert 'error' in user1.resp_merch_renew_key
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_renew_key_4(self):
        """ Renew key for other owner. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.merchant_renew_key(m_lid=user2.merchant1.lid)
        assert user1.resp_merch_renew_key['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 39}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_renew_key_5(self):
        """ Renew key without lid. """
        apikey1 = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        apikey2 = admin.get_merchant(lid=user1.merchant2.lid)['apikey']
        user1.merchant_renew_key(m_lid=None)
        assert user1.resp_merch_renew_key['error'] == {'code': -32070, 'message': 'InvalidParam'}
        assert apikey1 == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        assert apikey2 == admin.get_merchant(lid=user1.merchant2.lid)['apikey']

    def test_merchant_renew_key_6(self):
        """ Renew key with wrong session token. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['error'] == {'code': -32091, 'message': 'Unauth',
                                                       'data': {'reason': 'Invalid or expired session token', 'token': '1'}}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.headers['token'] = session

    def test_merchant_renew_key_7(self):
        """ Renew key with wrong session token. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        session, user1.headers['token'] = user1.headers['token'], None
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['error'] == {'code': -32091, 'message': 'Unauth',
                                                       'data': {'reason': 'Invalid or expired session token', 'token': '1'}}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.headers['token'] = session


class TestMerchantUpdate:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_update_1(self):
        """ Updating all parameter by valid data and drop to first state. """
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Новый тайтл', params={'param1': {'sub_param': 1}, 'param2': 2},
                              payment_expiry='3600000', rotate_addr=True, apiip='192.168.5.10, 192.168.100.5')
        assert user1.resp_merch_update['apiip'] == '192.168.5.10, 192.168.100.5'
        assert user1.resp_merch_update['title'] == 'Новый тайтл'
        user1.merchant_update(m_lid=user1.merchant1.lid, title=merchant_data['title'], params={},
                              payment_expiry='0', rotate_addr=False, apiip='')
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['params'] == {}
        assert merchant_data['payment_expiry'] == 0
        assert merchant_data['rotate_addr'] is False
        assert merchant_data['apiip'] is None

    def test_merchant_update_2(self):
        """ Updating one parameter of all. """
        merch_title = admin.get_merchant(lid=user1.merchant1.lid)['title']
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Новый тайтл', params={'param1': {'sub_param': 1}, 'param2': 2},
                              payment_expiry='3600000', rotate_addr=True, apiip='192.168.5.10, 192.168.100.5')
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['title'] == 'New'
        assert merchant_data['params']['param1'] == {'sub_param': 1}
        assert merchant_data['params']['param2'] == 2
        assert merchant_data['payment_expiry'] == 3600000
        assert merchant_data['rotate_addr'] is True
        assert merchant_data['apiip'] == '192.168.5.10, 192.168.100.5'
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params={}, payment_expiry=None, rotate_addr=None, apiip=None)
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'New'
        user1.merchant_update(m_lid=user1.merchant1.lid, title=merch_title, params={}, payment_expiry='0', rotate_addr=False, apiip='')


    def test_merchant_update_3(self):
        """ Banned on updating merchant without any parameter. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32070, 'message': 'InvalidParam'}

    def test_merchant_update_4(self):
        """ Banned on updating merchant with wrong ip parameter: space string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=None, apiip=' ')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_5(self):
        """ Banned on updating merchant with wrong ip parameter: without point between letter. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=None, apiip='1921681005')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_6(self):
        """ Banned on updating merchant with wrong ip parameter: with three part number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=None, apiip='192.168.10')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_7(self):
        """ Banned on updating merchant with wrong ip parameter: with five part number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=None, apiip='192.168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_8(self):
        """ Banned on updating merchant with wrong ip parameter: with two points before numbers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='192..168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_9(self):
        """ Banned on updating merchant with wrong ip parameter: with four numbers in part. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='1927.168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_10(self):
        """ Banned on updating merchant with wrong ip parameter: with defis between numbers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='927-168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_11(self):
        """ Banned on updating merchant with wrong ip parameter: with space between nambers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='927 168 10 1 1')
        assert user1.resp_merch_update['error'] == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_merchant_update_12(self):
        """ Banned on updating merchant with wrong params parameter: string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params='String',
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32070, 'message': 'InvalidParam', 'data': 'params'}

    def test_merchant_update_13(self):
        """ Banned on updating merchant with wrong params parameter: dict in string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params="{'Param': 9}",
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32070, 'message': 'InvalidParam', 'data': 'params'}

    def test_merchant_update_14(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr='String', apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32070, 'message': 'InvalidParam', 'data': 'rotate_addr'}

    def test_merchant_update_15(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=1, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32070, 'message': 'InvalidParam',
                                                    'data': {'reason': "Key 'rotate_addr' must not be of 'int' type"}}

    def test_merchant_update_16(self):
        """ Updating merchant parameter without m_lid. """
        user1.merchant_update(m_lid=None, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                                    'data': {'reason': "method 'merchant.update' missing 1 argument: 'm_lid'"}}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        assert admin.get_merchant(lid=user1.merchant2.lid)['title'] == 'Merchant2'

    def test_merchant_update_17(self):
        """ Updating merchant parameter with not own m_lid. """
        merch_title = admin.get_merchant(lid=user2.merchant1.lid)['title']
        user1.merchant_update(m_lid=user2.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert 'error' in user1.resp_merch_update
        assert admin.get_merchant(lid=user2.merchant1.lid)['title'] == merch_title

    def test_merchant_update_18(self):
        """ Updating merchant parameter with not real merchant lid. """
        merch1_title = admin.get_merchant(lid=user1.merchant1.lid)['title']
        merch2_title = admin.get_merchant(lid=user1.merchant2.lid)['title']
        user1.merchant_update(m_lid='01', title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert 'error' in user1.resp_merch_update
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == merch1_title
        assert admin.get_merchant(lid=user1.merchant2.lid)['title'] == merch2_title

    def test_merchant_update_19(self):
        """ Updating merchant parameter with wrong session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32091, 'message': 'Unauth',
                                                    'data': {'reason': 'Invalid or expired session token', 'token': '1'}}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        user1.headers['x-token'] = session

    def test_merchant_update_20(self):
        """ Updating merchant parameter without session token. """
        merch_title = admin.get_merchant(lid=user1.merchant1.lid)['title']
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-token to headers'}}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == merch_title
        user1.headers['x-token'] = session

    def test_merchant_update_21(self, _merchant_activate):
        """ Updating inactive merchant parameter. """
        merch_title = admin.get_merchant(lid=user1.merchant1.lid)['title']
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'New'
        user1.merchant_update(m_lid=user1.merchant1.lid, title=merch_title, params=None, payment_expiry=None, rotate_addr=None, apiip=None)

