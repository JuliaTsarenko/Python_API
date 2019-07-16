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
        assert user1.resp_merch_create['error'] == {'code': -32000, 'message': 'ReqExcept', 'data': 'NotNull'}

    def test_merchant_create_6(self):
        """ Creating 2 merchant with equal title. """
        user1.merchant_create(title='Double title')
        user1.merchant_create(title='Double title')
        assert user1.resp_merch_create['error'] == {'code': -32000, 'message': 'ReqExcept', 'data': 'Unique'}
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
        assert user1.resp_merch_switch['error'] == {'code': -32000, 'message': 'InvalidParam'}
        assert admin.get_merchant(lid=user2.merchant1.lid)['is_active'] is True

    def test_switching_merchant_3(self):
        """ Switching merchant without session token. """
        session = user1.headers['x-token']
        user1.headers['x-token'] = None
        user1.merchant_switch(m_lid=user1.merchant2.lid, is_active=False)
        assert user1.resp_merch_switch['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Server Error'}
        user1.headers['x-token'] = session


class TestListMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_merchant_1(self):
        """ Getting list of all merchants. """
        user1.merchant_switch(m_lid=user1.merchant2.lid, is_active=False)
        user1.merchant_list(first=None, count=None)
        merch_dct = {mr['lid']: {'balances': mr['balances'], 'pw': mr['pw'], 'is_active': mr['is_active']} for mr in user1.resp_merch_list['data']}
        assert merch_dct[user1.merchant2.lid]['is_active'] is False
        assert merch_dct[user1.merchant1.lid]['is_active'] is True
        assert len(user1.resp_merch_list['data']) == 2
        user1.merchant_switch(m_lid=user1.merchant2.lid, is_active=True)

    def test_list_merchant_2(self):
        """ Getting list merchant from one element. """
        user1.merchant_list(first=None, count=None)
        full_ls = user1.resp_merch_list['data']
        user1.merchant_list(first=1, count=1)
        assert len(user1.resp_merch_list['data']) == 1
        assert full_ls[1] == user1.resp_merch_list['data'][0]


class TestGetMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_get_1(self):
        """ Getting information for inactive merchant without balance. """
        admin.set_merchant(lid=user1.merchant1.lid, is_active=False, is_customfee=False, payout_allowed=False)
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=False)
        list_params = ['apiip', 'is_active', 'lid', 'out_pay', 'pw', 'title']
        list_params.sort()
        resp_list_params = list(user1.resp_merch_get)
        resp_list_params.sort()
        assert user1.resp_merch_get['is_active'] is False
        assert user1.resp_merch_get['out_pay'] is False
        assert resp_list_params == list_params
        list_payway = list(admin.payway)
        list_payway.sort()
        resp_list_payway = user1.resp_merch_get['pw']
        resp_list_payway.sort()
        assert list_payway == resp_list_payway
        admin.set_merchant(lid=user1.merchant1.lid, is_active=True, is_customfee=False, payout_allowed=True)

    def test_merchant_get_2(self):
        """ Getting information for active merchant with balance. """
        admin.set_merchant(lid=user1.merchant2.lid, is_active=True, is_customfee=True, payout_allowed=True)
        admin.set_wallet_amount(balance=30000, currency='BTC', merch_lid=user1.merchant2.lid)
        user1.merchant_get(m_lid=user1.merchant2.lid, balance=True)
        assert user1.resp_merch_get['is_active'] is True
        assert user1.resp_merch_get['out_pay'] is True
        assert user1.resp_merch_get['lid'] == user1.merchant2.lid
        assert user1.resp_merch_get['balances']['BTC'] == '0.00003'
        admin.set_merchant(lid=user1.merchant2.lid, is_active=True, is_customfee=False, payout_allowed=True)

    def test_merchant_get_3(self):
        """ Getting information with NONE balance. """
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=None)
        assert 'balances' not in user1.resp_merch_get
        assert 'lid' in user1.resp_merch_get

    def test_merchant_get_4(self):
        """ Getting information with not own m_lid. """
        user1.merchant_get(m_lid=user2.merchant1.lid, balance=False)
        assert user1.resp_merch_get['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}

    def test_merchant_get_5(self):
        """ Getting information without m_lid. """
        user1.merchant_get(m_lid=None, balance=False)
        assert user1.resp_merch_get['error'] == {'code': -32000, 'message': 'InvalidParam'}

    def test_merchant_get_6(self):
        """ Getting information with wrong session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=True)
        assert user1.resp_merch_get['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        user1.headers['x-token'] = session

    def test_merchant_get_7(self):
        """ Getting key without session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_get(m_lid=user1.merchant1.lid, balance=True)
        assert user1.resp_merch_get['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Server Error'}
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

    def test_merchant_get_key_3(self):
        """ Getting key for inactive merchant. """
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=False)
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=True)

    def test_merchant_get_key_4(self):
        """ Getting key for other owner. """
        user1.merchant_get_key(m_lid=user2.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}

    def test_merchant_get_key_5(self):
        """ Getting key without lid. """
        user1.merchant_get_key(m_lid=None)
        assert user1.resp_merch_get_key['error'] == {'code': -32000, 'message': 'InvalidParam'}

    def test_merchant_get_key_6(self):
        """ Getting key with wrong session. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        user1.headers['x-token'] = session

    def test_merchant_get_key_7(self):
        """ Getting key without session. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_get_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_get_key['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Server Error'}
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

    def test_merchant_renew_key_3(self):
        """ Renew key for inactive merchant. """
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=False)
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert 'error' in user1.resp_merch_renew_key
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=True)

    def test_merchant_renew_key_4(self):
        """ Renew key for other owner. """
        user1.merchant_renew_key(m_lid=user2.merchant1.lid)
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        assert user1.resp_merch_renew_key['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 39}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']

    def test_merchant_renew_key_5(self):
        """ Renew key without lid. """
        apikey1 = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        apikey2 = admin.get_merchant(lid=user1.merchant2.lid)['apikey']
        user1.merchant_renew_key(m_lid=None)
        assert user1.resp_merch_renew_key['error'] == {'code': -32000, 'message': 'InvalidParam'}
        assert apikey1 == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        assert apikey2 == admin.get_merchant(lid=user1.merchant2.lid)['apikey']

    def test_merchant_renew_key_6(self):
        """ Renew key with wrong session token. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.headers['token'] = session

    def test_merchant_renew_key_7(self):
        """ Renew key with wrong session token. """
        apikey = admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        session, user1.headers['token'] = user1.headers['token'], None
        user1.merchant_renew_key(m_lid=user1.merchant1.lid)
        assert user1.resp_merch_renew_key['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        assert apikey == admin.get_merchant(lid=user1.merchant1.lid)['apikey']
        user1.headers['token'] = session


class TestMerchantUpdate:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_update_1(self):
        """ Updating all parameter by valid data and drop to first state. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Новый тайтл', params={'param1': {'sub_param': 1}, 'param2': 2},
                              payment_expiry='3600000', rotate_addr=True, apiip='192.168.5.10, 192.168.100.5')
        assert user1.resp_merch_update['apiip'] == '192.168.5.10, 192.168.100.5'
        assert user1.resp_merch_update['title'] == 'Новый тайтл'
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['params']['param1'] == {'sub_param': 1}
        assert merchant_data['params']['param2'] == 2
        assert merchant_data['payment_expiry'] == 3600000
        assert merchant_data['rotate_addr'] is True
        assert merchant_data['apiip'] == '192.168.5.10, 192.168.100.5'
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Merchant1', params={},
                              payment_expiry='0', rotate_addr=False, apiip='')
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['params'] == {}
        assert merchant_data['payment_expiry'] == 0
        assert merchant_data['rotate_addr'] is False
        assert merchant_data['apiip'] is None

    def test_merchant_update_2(self):
        """ Updating one parameter of all. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Новый тайтл', params={'param1': {'sub_param': 1}, 'param2': 2},
                              payment_expiry='3600000', rotate_addr=True, apiip='192.168.5.10, 192.168.100.5')
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None,
                              payment_expiry=None, rotate_addr=None, apiip=None)
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['title'] == 'New'
        assert merchant_data['params']['param1'] == {'sub_param': 1}
        assert merchant_data['params']['param2'] == 2
        assert merchant_data['payment_expiry'] == 3600000
        assert merchant_data['rotate_addr'] is True
        assert merchant_data['apiip'] == '192.168.5.10, 192.168.100.5'
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params={},
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'New'
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Merchant1', params={}, payment_expiry=0, rotate_addr=False, apiip='')

    def test_merchant_update_3(self):
        """ Banned on updating merchant without any parameter. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam'}
        merchant_data = admin.get_merchant(lid=user1.merchant1.lid)
        assert merchant_data['params'] == {}
        assert merchant_data['payment_expiry'] == 0
        assert merchant_data['rotate_addr'] is False
        assert merchant_data['apiip'] is None

    def test_merchant_update_4(self):
        """ Banned on updating merchant with wrong ip parameter: space string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip=' ')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_5(self):
        """ Banned on updating merchant with wrong ip parameter: without point between letter. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='1921681005')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_6(self):
        """ Banned on updating merchant with wrong ip parameter: with three part number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='192.168.10')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_7(self):
        """ Banned on updating merchant with wrong ip parameter: with five part number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='192.168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_8(self):
        """ Banned on updating merchant with wrong ip parameter: with two points before numbers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='192..168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_9(self):
        """ Banned on updating merchant with wrong ip parameter: with four numbers in part. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='1927.168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_10(self):
        """ Banned on updating merchant with wrong ip parameter: with defis between numbers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='927-168.10.1.1')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_11(self):
        """ Banned on updating merchant with wrong ip parameter: with space between nambers. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None,
                              payment_expiry=None, rotate_addr=None, apiip='927 168 10 1 1')
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'apiip'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['apiip'] is None

    def test_merchant_update_12(self):
        """ Banned on updating merchant with wrong params parameter: string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params='String',
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'params'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['params'] == {}

    def test_merchant_update_13(self):
        """ Banned on updating merchant with wrong params parameter: dict in string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params="{'Param': 9}",
                              payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'params'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['params'] == {}

    def test_merchant_update_14(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: string. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr='String', apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'rotate_addr'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['rotate_addr'] is False

    def test_merchant_update_15(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: number. """
        user1.merchant_update(m_lid=user1.merchant1.lid, title=None, params=None, payment_expiry=None, rotate_addr=1, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'rotate_addr'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['rotate_addr'] is False

    def test_merchant_update_16(self):
        """ Updating merchant parameter without m_lid. """
        user1.merchant_update(m_lid=None, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'm_lid'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        assert admin.get_merchant(lid=user1.merchant2.lid)['title'] == 'Merchant2'

    def test_merchant_update_17(self):
        """ Updating merchant parameter with not own m_lid. """
        user1.merchant_update(m_lid=user2.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}
        assert admin.get_merchant(lid=user2.merchant1.lid)['title'] == 'Мерчант 1 второго юзера'

    def test_merchant_update_18(self):
        """ Updating merchant parameter with not real merchant lid. """
        user1.merchant_update(m_lid=100056, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        assert admin.get_merchant(lid=user1.merchant2.lid)['title'] == 'Merchant2'

    def test_merchant_update_19(self):
        """ Updating merchant parameter with wrong session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        user1.headers['x-token'] = session

    def test_merchant_update_20(self):
        """ Updating merchant parameter without session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        assert user1.resp_merch_update['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Add x-token to headers'}
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'Merchant1'
        user1.headers['x-token'] = session

    def test_merchant_update_21(self):
        """ Updating inactive merchant parameter. """
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=False)
        user1.merchant_update(m_lid=user1.merchant1.lid, title='New', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        # assert user1.resp_merch_update['exception'] == 'InvalidMerchant'  ()
        assert admin.get_merchant(lid=user1.merchant1.lid)['title'] == 'New'
        user1.merchant_update(m_lid=user1.merchant1.lid, title='Merchant1', params=None, payment_expiry=None, rotate_addr=None, apiip=None)
        user1.merchant_switch(m_lid=user1.merchant1.lid, is_active=True)


class TestPwmerchactive:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


    def test_pwmerchactive_public_list_1(self):
        """ Getting list public payway. """
        ls_payway_admin = [pw for pw in admin.payway if admin.payway[pw]['is_public'] is True]
        ls_payway_admin.sort()
        user1.pwmerchactive_public_list()
        user1.resp_merch_public_list.sort()
        assert ls_payway_admin == user1.resp_merch_public_list


    def test_pwmerchactive_public_list_2(self):
        """ Getting list public without disabled public payway. """
        admin.set_payways(name='visamc', is_active=True, is_public=False)
        user1.pwmerchactive_public_list()
        assert 'visamc' not in user1.resp_merch_public_list
        admin.set_payways(name='visamc', is_active=True, is_public=True)
        user1.pwmerchactive_public_list()
        assert 'visamc' in user1.resp_merch_public_list


    def test_pwmerchactive_update_2(self):
        """ Banned on pwmerchactive update with inactive payway by payways table. """
        admin.set_payways(name='visamc', is_active=True, is_public=False)
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32000, 'message': 'InvalidPayway', 'data': "payway name visamc - can't be updated manually"}
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert 'visamc' in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list
        assert admin.payway['visamc']['id'] in admin.get_pwmerchactive(is_active=True, merch_id=user1.merchant1.id)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, is_active=False, payway_id=admin.payway['visamc']['id'])
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=True, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32000, 'message': 'InvalidPayway', 'data': "payway name visamc - can't be updated manually"}
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert 'visamc' not in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' not in user1.resp_pwmerchactive_list
        admin.set_payways(name='visamc', is_active=True, is_public=True)


    def test_pwmerchactive_update_3(self):
        """ Updating pwmerchactive. """
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update == {'is_active': False, 'merchant_id': user1.merchant1.id, 'payway_name': 'visamc'}
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert 'visamc' not in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' not in user1.resp_pwmerchactive_list
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=True, payway_name='visamc')
        assert user1.resp_pwmerchactive_update == {'is_active': True, 'merchant_id': user1.merchant1.id, 'payway_name': 'visamc'}
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert 'visamc' in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list


    def test_pwmerchactive_update_4(self):
        """ Updating payway without lid. """
        user1.pwmerchactive_update(m_lid=None, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'm_lid'}
        user1.pwmerchactive_list(m_lid=user1.merchant2.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list


    def test_pwmerchactive_update_5(self):
        """ Updating payway with wrong payway. """
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name='VISSA')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32000, 'message': 'InvalidPayway', 'data': 'payway_name'}


    def test_pwmerchactive_update_6(self):
        """ Updating payway without payway. """
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name=None)
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32000, 'message': 'InvalidPayway', 'data': 'payway_name'}


    def test_pwmerchactive_update_7(self):
        """ Updating payway for not own merchant. """
        user1.pwmerchactive_update(m_lid=user2.merchant1.lid, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'm_lid'}
        user2.pwmerchactive_list(m_lid=user2.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list


    def test_pwmerchactive_update_8(self):
        """ Updating payway with wrong session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        user1.headers['x-token'] = session
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list


    def test_pwmerchactive_update_9(self):
        """ Updating payway without session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.pwmerchactive_update(m_lid=user1.merchant1.lid, is_active=False, payway_name='visamc')
        assert user1.resp_pwmerchactive_update['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Add x-token to headers'}
        user1.headers['x-token'] = session
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert 'visamc' in user1.resp_pwmerchactive_list


    def test_pwmerchactive_list_1(self):
        """ Getting common fee for operation payout. """
        admin.set_fee(add=bl(2), mult=pers(1), tp=0, payway=admin.payway['visamc']['id'], currency='UAH')
        admin.set_fee(tp=0, payway=admin.payway['visamc']['id'], currency='RUB')
        admin.set_fee(tp=0, payway=admin.payway['privat24']['id'], currency='UAH')
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=True)
        assert user1.resp_pwmerchactive_list['visamc']['UAH'] == {'add': '2', 'max': '0', 'min': '0', 'mult': '0.01'}
        assert user1.resp_pwmerchactive_list['visamc']['RUB'] == {'add': '0', 'max': '0', 'min': '0', 'mult': '0'}
        assert user1.resp_pwmerchactive_list['privat24']['UAH'] == {'add': '0', 'max': '0', 'min': '0', 'mult': '0'}

    def test_pwmerchactive_list_2(self):
        """ Getting personal fee for operation payout and UAH currency only . """
        admin.set_merchant(lid=user1.merchant1.lid, is_active=True, is_customfee=True, payout_allowed=True)
        admin.set_fee(add=bl(2), mult=pers(1), tp=10, payway=admin.payway['visamc']['id'], currency='UAH')
        admin.set_fee(add=bl(1), mult=pers(0.5), tp=10, payway=admin.payway['visamc']['id'],
                      currency='UAH', merchant_id=user1.merchant1.id)
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr='UAH', is_out=True)
        assert user1.resp_pwmerchactive_list['visamc']['UAH'] == {'add': '1', 'max': '0', 'min': '0', 'mult': '0.005'}
        assert 'RUB' not in user1.resp_pwmerchactive_list['visamc']
        assert 'btc' not in user1.resp_pwmerchactive_list
        user1.pwmerchactive_list(m_lid=user1.merchant2.lid, curr='UAH', is_out=True)
        assert user1.resp_pwmerchactive_list['visamc']['UAH'] == {'add': '2', 'max': '0', 'min': '0', 'mult': '0.01'}
        admin.set_fee(tp=10, payway=admin.payway['visamc']['id'],
                      currency='UAH', merchant_id=user1.merchant1.id, is_active=False)
        admin.set_merchant(lid=user1.merchant1.lid, is_active=True, is_customfee=False, payout_allowed=True)

    @pytest.mark.skip(reason='Canceled tp parameter')
    def test_pwmerchactive_list_3(self):
        """ Getting payway for operation payin only + UAH currency only. """
        admin.set_fee(add=2000000000, mult=30000000, tp=0, payway=admin.payway['visamc']['id'],
                      currency='UAH')
        admin.set_fee(add=5000000000, mult=10000000, tp=10, payway=admin.payway['visamc']['id'],
                      currency='UAH')
        admin.set_fee(add=5000000000, mult=10000000, tp=0, payway=admin.payway['visamc']['id'],
                      currency='RUB')
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr='UAH', is_out=False)
        assert user1.resp_pwmerchactive_list['visamc']['UAH'] == {'add': '2', 'max': '0', 'min': '0', 'mult': '0.03'}
        assert len(user1.resp_pwmerchactive_list['visamc']) == 1
        assert 'btc' not in user1.resp_pwmerchactive_list

    def test_pwmerchactive_list_4(self):
        """ Getting payway without lid param. """
        user1.pwmerchactive_list(m_lid=None, curr=None, is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'm_lid'}

    def test_pwmerchactive_list_5(self):
        """ Getting payway by not own lid. """
        user1.pwmerchactive_list(m_lid=user2.merchant1.lid, curr=None, is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}

    def test_pwmerchactive_list_6(self):
        """ Getting payway by not real merchant. """
        user1.pwmerchactive_list(m_lid=2, curr=None, is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}

    def test_pwmerchactive_list_7(self):
        """ Getting payway with not real currency. """
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr='UHA', is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32075, 'message': 'InvalidCurrency'}


    def test_pwmerchactive_list_9(self):
        """ Getting payway without is out param. """
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=None)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'is_out'}

    def test_pwmerchactive_list_10(self):
        """ Getting payway with session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], '1'
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}
        user1.headers['x-token'] = session

    def test_pwmerchactive_list_11(self):
        """ Getting payway without session token. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.pwmerchactive_list(m_lid=user1.merchant1.lid, curr=None, is_out=False)
        assert user1.resp_pwmerchactive_list['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Add x-token to headers'}
        user1.headers['x-token'] = session

