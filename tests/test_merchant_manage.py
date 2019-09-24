import pytest
from users.tools import *
from users.user import User


@pytest.mark.positive
class TestCreateMerchant:
    """ Creating merchant. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_create_1(self, _delete_merchant):
        """ Creating merchant by owner with ASCII symbols. """
        user1.merchant(method='create', params={'title': 'Test merchant !@#$%^&*()_+ .', 'payway': None})
        admin.params['lid'] = user1.resp_merchant['lid']
        assert user1.resp_merchant['title'] == 'Test merchant !@#$%^&*()_+ .'
        assert admin.get_model(model='merchant', _filter='lid', value=user1.resp_merchant['lid'])[0]['title'] == 'Test merchant !@#$%^&*()_+ .'

    def test_merchant_create_2(self, _delete_merchant):
        """ Creating merchant with kirrils symbols in title. """
        user1.merchant(method='create', params={'title': 'Тестовый мерчант', 'payway': None})
        admin.params['lid'] = user1.resp_merchant['lid']
        assert user1.resp_merchant['title'] == 'Тестовый мерчант'

    def test_merchant_create_3(self, _delete_merchant):
        """ Creating merchant with empty string. """
        adm_ls = [dct['name'] for dct in admin.get_model(model='payway', _filter=None, value=None)]
        adm_ls.sort()
        user1.merchant(method='create', params={'title': '', 'payway': None})
        admin.params['lid'] = user1.resp_merchant['lid']
        us_ls = user1.resp_merchant['pw']
        us_ls.sort()
        assert user1.resp_merchant['title'] == ''
        assert adm_ls == us_ls
        assert admin.get_model(model='merchant', _filter='lid', value=user1.resp_merchant['lid'])[0]['title'] == ''

    def test_merchant_create_4(self, _delete_merchant):
        """ Creating merchant with space in title. """
        user1.merchant(method='create', params={'title': ' '})
        admin.params['lid'] = user1.resp_merchant['lid']
        assert user1.resp_merchant['title'] == ' '
        assert admin.get_model(model='merchant', _filter='lid', value=user1.resp_merchant['lid'])[0]['title'] == ' '

    def test_merchant_create_5(self, _delete_merchant):
        """ Creating 2 merchant with equal title in two different merchant. """
        user1.merchant(method='create', params={'title': 'Title'})
        user2.merchant(method='create', params={'title': 'Title'})
        admin.params['lid'] = user2.resp_merchant['lid']
        assert user2.resp_merchant['title'] == 'Title'
        assert admin.get_model(model='merchant', _filter='lid', value=user2.resp_merchant['lid'])[0]['title'] == 'Title'
        admin.delete_merchant(lid=user1.resp_merchant['lid'])

    def test_merchant_create_6(self, _delete_merchant):
        """ Creating merchant for payway. """
        adm_ls = [dct['name'] for dct in admin.get_model(model='payway', _filter=None, value=None)]
        adm_ls.sort()
        admin.set_model(model='payway', selector={'name': ['eq', 'visamc']}, data={'is_active': True, 'is_public': True, 'is_linkable': True})
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        us_ls = user1.resp_merchant['pw']
        us_ls.sort()
        admin.params['lid'] = user1.resp_merchant['lid']
        assert user1.resp_merchant['title'] == 'Title'
        assert adm_ls == us_ls
        assert user1.resp_merchant['linked_pw'] == 'visamc'

    def test_merchant_create_7(self, _delete_merchant):
        """ Creating two merchant for two equal payway. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        user1.merchant(method='create', params={'title': 'Title1', 'payway': 'visamc'})
        assert user1.resp_merchant['title'] == 'Title1'
        admin.delete_merchant(user1.resp_merchant['lid'])


@pytest.mark.negative
class TestWrongCreateMerchant:
    """ Wrong request to merchant.create method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_merchant_create_1(self):
        """ Creating merchant without title. """
        user1.merchant(method='create', params={'title': None, 'payway': 'visamc'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'title', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_merchant_create_2(self, _delete_merchant):
        """ Creating 2 merchant with equal title. """
        user1.merchant(method='create', params={'title': 'Double title'})
        admin.params['lid'] = user1.resp_merchant['lid']
        user1.merchant(method='create', params={'title': 'Double title'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'reason': 'Unable to complete: Unique title', 'value': 'Double title'},
                                       'message': 'EParamInvalid'}

    def test_wrong_merchant_create_3(self):
        """ Creating merchant with not real payway. """
        admin.set_model(model='payway', selector={'name': ['eq', 'tinkoff_cs']}, data={'is_active': False, 'is_public': True, 'is_linkable': True})
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'tinkoff_cs'})
        assert user1.resp_merchant == {'code': -32082, 'data': {'field': 'payway', 'reason': 'Inactive'},
                                       'message': 'EStatePaywayInactive'}

    def test_wrong_merchant_create_4(self):
        """ Creating merchant with not public payway. """
        admin.set_model(model='payway', selector={'name': ['eq', 'tinkoff_cs']}, data={'is_active': True, 'is_public': False, 'is_linkable': True})
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'tinkoff_cs'})
        assert user1.resp_merchant == {'code': -32082, 'data': {'field': 'payway', 'reason': 'Inactive'}, 'message': 'EStatePaywayInactive'}

    def test_wrong_merchant_create_5(self):
        """ Creating merchant with not active payway. """
        admin.set_model(model='payway', selector={'name': ['eq', 'tinkoff_cs']}, data={'is_active': True, 'is_public': True, 'is_linkable': False})
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'tinkoff_cs'})
        assert user1.resp_merchant == {'code': -32082, 'data': {'field': 'payway', 'reason': 'Inactive'}, 'message': 'EStatePaywayInactive'}

    def test_wrong_merchant_create_6(self):
        """ Request with excess parameter. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc', 'par': '123'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'par', 'reason': 'Should not be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_merchant_create_7(self, _authorization):
        """ Request with wrong session. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid',
                                       'value': user1.headers['x-token']}, 'message': 'EStateUnauth'}


@pytest.mark.positive
class TestSwitchMerchant:
    """ Switching merchant setting. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_switching_merchant_1(self):
        """ Disabling/enabling common payway's merchant. """
        print(user1.merchant1.lid)
        user1.merchant(method='switch', params={'m_lid': user1.merchant1.lid, 'is_active': False})
        assert user1.resp_merchant['is_active'] is False
        assert admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['is_active'] is False
        user1.merchant(method='switch', params={'m_lid': user1.merchant1.lid, 'is_active': True})
        assert user1.resp_merchant['is_active'] is True
        assert admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['is_active'] is True

    def test_switching_merchant_2(self):
        """ Disabling/enabling common payway's merchant. """
        user1.merchant(method='switch', params={'m_lid': user1.merchant1.lid, 'is_active': None})
        assert user1.resp_merchant['is_active'] is False
        assert admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['is_active'] is False
        user1.merchant(method='switch', params={'m_lid': user1.merchant1.lid, 'is_active': True})

    def test_switching_merchant_3(self, _delete_merchant):
        """ Disabling/enabling special payway's merchant. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        user1.merchant(method='switch', params={'m_lid': str(user1.resp_merchant['lid']), 'is_active': True})
        assert user1.resp_merchant['is_active'] is True
        assert admin.get_model(model='merchant', _filter='lid', value=user1.resp_merchant['lid'])[0]['is_active'] is True
        user1.merchant(method='switch', params={'m_lid': str(user1.resp_merchant['lid']), 'is_active': False})
        assert user1.resp_merchant['is_active'] is False
        assert admin.get_model(model='merchant', _filter='lid', value=user1.resp_merchant['lid'])[0]['is_active'] is False


@pytest.mark.negative
class TestWrongSwitchMerchant:
    """ Wrong request to switch.merchant method"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_switch_merchant_1(self):
        """ Switching merchant by not owner. """
        user1.merchant(method='switch', params={'m_lid': user2.merchant1.lid, 'is_active': False})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'm_lid', 'reason': 'Not found'}, 'message': 'EParamNotFound'}
        assert admin.get_model(model='merchant', _filter='lid', value=int(user2.merchant1.lid))[0]['is_active'] is True

    def test_wrong_switch_merchant_2(self):
        """ Switching merchant without m_lid parameter. """
        user1.merchant(method='switch', params={'is_active': False})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'm_lid', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_switch_merchant_3(self):
        """ Switching merchant with excess parameter. """
        user1.merchant(method='switch', params={'m_lid': user1.merchant1.lid, 'is_active': False, 'par': '123'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'par', 'reason': 'Should not be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_switch_merchant_4(self, _authorization):
        """ Switching merchant without session token. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='switch', params={'is_active': False})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid',  'value': user1.headers['x-token']},
                                       'message': 'EStateUnauth'}


@pytest.mark.positive
class TestListMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_merchant_1(self):
        """ Getting list of all merchants. """
        adm_ls = [dct['lid'] for dct in admin.get_model(model='merchant', _filter='owner_id', value=user1.id)]
        adm_ls.sort()
        user1.merchant(method='list', params={'first': None, 'count': None})
        us_ls = [dct['lid'] for dct in user1.resp_merchant['data']]
        us_ls.sort()
        assert us_ls == adm_ls

    def test_list_merchant_2(self):
        """ Getting list merchant from one element. """
        adm_ls = [dct['lid'] for dct in admin.get_model(model='merchant', _filter='owner_id', value=user1.id)][:1]
        user1.merchant(method='list', params={'first': None, 'count': '1'})
        us_ls = [dct['lid'] for dct in user1.resp_merchant['data']]
        assert adm_ls == us_ls

    def test_list_merchant_3(self):
        """ Getting list merchant from one element from first. """
        adm_ls = [dct['lid'] for dct in admin.get_model(model='merchant', _filter='owner_id', value=user1.id)][1:2]
        user1.merchant(method='list', params={'first': '1', 'count': '1'})
        us_ls = [dct['lid'] for dct in user1.resp_merchant['data']]
        assert adm_ls == us_ls

    def test_list_merchant_4(self):
        """ Getting balances. """
        admin.set_wallet_amount(balance=bl(0.000012), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(5.55), currency='USD', merch_lid=user1.merchant1.lid)
        user1.merchant(method='list', params={'first': None, 'count': None})
        us_ls = [dct['balances'] for dct in user1.resp_merchant['data'] if dct['lid'] == int(user1.merchant1.lid)]
        print(us_ls)
        assert us_ls[0]['BTC'] == '0.000012'
        assert us_ls[0]['USD'] == '5.55'


@pytest.mark.negative
class TestWrongListMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_list_merchant_1(self):
        """ Request with int in FIRST parameter. """
        user1.merchant(method='list', params={'first': 1, 'count': None})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'first', 'reason': "'first' must not be of 'int' type",
                                       'value': 1}, 'message': 'EParamType'}

    def test_wrong_list_merchant_2(self):
        """ Request with negative number in FIRST parameter. """
        user1.merchant(method='list', params={'first': '-1', 'count': None})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'first', 'reason': 'Should be a positive Number'}, 'message': 'EParamInvalid'}

    def test_wrong_list_merchant_3(self):
        """ Request with float number in FIRST parameter. """
        user1.merchant(method='list', params={'first': '0.3', 'count': None})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'first', 'reason': 'Should be an Integer'}, 'message': 'EParamType'}

    def test_wrong_list_merchant_4(self):
        """ Request with float number in COUNT parameter. """
        user1.merchant(method='list', params={'first': None, 'count': 1})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'count', 'reason': "'count' must not be of 'int' type",
                                       'value': 1}, 'message': 'EParamType'}

    def test_wrong_list_merchant_5(self):
        """ Request with negative number in COUNT parameter. """
        user1.merchant(method='list', params={'first': None, 'count': '-1'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'count', 'reason': 'Should be more than zero'},
                                       'message': 'EParamInvalid'}

    def test_wrong_list_merchant_6(self):
        """ Request with float number in COUNT parameter. """
        user1.merchant(method='list', params={'first': None, 'count': '0.5'})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'count', 'reason': 'Should be an Integer'}, 'message': 'EParamType'}

    def test_wrong_list_merchant_7(self):
        """ Request with excess parameter. """
        user1.merchant(method='list', params={'first': None, 'count': None, 'par': '123'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'par', 'reason': 'Should not be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_list_merchant_8(self, _authorization):
        """ Request with wrong session token. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='list', params={'first': None, 'count': None})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid', 'value': user1.headers['x-token']},
                                       'message': 'EStateUnauth'}


@pytest.mark.positive
class TestGetMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_get_1(self):
        """ Getting information for common merchant with balance. """
        admin.set_wallet_amount(balance=bl(0.000012), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(5.55), currency='UAH', merch_lid=user1.merchant1.lid)
        merch = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]
        user1.merchant(method='get', params={'m_lid': user1.merchant1.lid, 'balance': True})
        assert user1.resp_merchant['is_active'] == merch['is_active']
        assert user1.resp_merchant['title'] == merch['title']
        assert user1.resp_merchant['linked_pw'] is None
        assert user1.resp_merchant['balances']['BTC'] == '0.000012'
        assert user1.resp_merchant['balances']['UAH'] == '5.55'

    def test_merchant_get_2(self, _merchant_activate):
        """ Getting information for inactive common merchant without balances. """
        adm_ls = [dct['name'] for dct in admin.get_model(model='payway', _filter=None, value=None)]
        adm_ls.sort()
        user1.merchant(method='get', params={'m_lid': user1.merchant1.lid, 'balance': False})
        us_ls = user1.resp_merchant['pw']
        us_ls.sort()
        assert user1.resp_merchant['is_active'] is False
        assert us_ls == adm_ls
        assert 'balances' not in user1.resp_merchant

    def test_merchant_get_3(self, _delete_merchant):
        """ Getting information special visamc merchant without balances. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        user1.merchant(method='get', params={'m_lid': str(user1.resp_merchant['lid']), 'balance': None})
        assert user1.resp_merchant['lid'] == admin.params['lid']
        assert user1.resp_merchant['linked_pw'] == 'visamc'
        assert 'balances' not in user1.resp_merchant

    def test_merchant_get_4(self, _delete_merchant):
        """ Getting information special visamc merchant without balances. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        admin.set_wallet_amount(balance=bl(33.88), currency='UAH', merch_lid=user1.resp_merchant['lid'])
        user1.merchant(method='get', params={'m_lid': str(user1.resp_merchant['lid']), 'balance': True})
        assert user1.resp_merchant['balances']['UAH'] == '33.88'


@pytest.mark.negative
class TestWrongGetMerchant:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_get_merchant_1(self):
        """ Getting information with not own m_lid. """
        user1.merchant(method='get', params={'m_lid': user2.merchant1.lid, 'balance': None})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'merchant', 'reason': 'Not found'}, 'message': 'EParamNotFound'}

    def test_wrong_get_merchant_2(self):
        """ Getting information with wrong merchant lid. """
        user1.merchant(method='get', params={'m_lid': '01', 'balance': None})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'merchant', 'reason': 'Not found'}, 'message': 'EParamNotFound'}

    def test_wrong_get_merchant_3(self):
        """ Getting information with int merchant lid. """
        user1.merchant(method='get', params={'m_lid': int(user1.merchant1.lid), 'balance': None})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'm_lid', 'reason': "'m_lid' must not be of 'int' type",
                                                                'value': int(user1.merchant1.lid)}, 'message': 'EParamType'}

    def test_wrong_get_merchant_4(self):
        """ Getting information without m_lid. """
        user1.merchant(method='get', params={'m_lid': None, 'balance': None})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'm_lid', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_get_merchant_5(self):
        """ Getting merchant with excess parameter. """
        user1.merchant(method='get', params={'m_lid': user1.merchant1.lid, 'balance': None, 'par': '123'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'par', 'reason': 'Should not be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_merchant_get_6(self, _authorization):
        """ Getting merchant with wrong session token. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='get', params={'m_lid': user1.merchant1.lid, 'balance': None})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid', 'value': user1.headers['x-token']},
                                       'message': 'EStateUnauth'}


@pytest.mark.positive
class TestMerchantGetKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_get_key_1(self):
        """ Getting key for common merchant without 2 step auth. """
        user1.merchant(method='get_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant['merch_token'] == user1.merchant1.akey

    def test_merchant_get_key_2(self, _disable_2type):
        """ Getting key for merchant with 2 step auth. """
        user1.set_2type(tp='0')
        user1.merchant(method='get_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.merch_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == user1.merchant1.akey

    def test_merchant_get_key_3(self, _delete_merchant):
        """ Getting key for special merchant without 2 step auth. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        admin.set_model(model='merchant', selector={'lid': ['=', str(user1.resp_merchant['lid'])]}, data={'is_active': True})
        user1.merchant(method='get_key', params={'m_lid': str(user1.resp_merchant['lid'])})
        assert user1.resp_merchant['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=admin.params['lid'])[0]['apikey']

    def test_merchant_get_key_4(self, _disable_2type, _delete_merchant):
        """ Getting key for special merchant with 2 step auth. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        admin.set_model(model='merchant', selector={'lid': ['=', str(user1.resp_merchant['lid'])]}, data={'is_active': True})
        user1.set_2type(tp='0')
        user1.merchant(method='get_key', params={'m_lid': str(user1.resp_merchant['lid'])})
        assert user1.resp_merchant['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.merch_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=admin.params['lid'])[0]['apikey']


@pytest.mark.negative
class TestWrongMerchantGetKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_merchant_get_key_1(self):
        """ Getting key for other owner. """
        user1.merchant(method='get_key', params={'m_lid': user2.merchant1.lid})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'merchant', 'reason': 'Not found'}, 'message': 'EParamNotFound'}

    def test_wrong_merchant_get_key_2(self):
        """ Getting key with int m_lid parameter. """
        user1.merchant(method='get_key', params={'m_lid': int(user1.merchant1.lid)})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'm_lid', 'reason': "'m_lid' must not be of 'int' type",
                                       'value': int(user1.merchant1.lid)}, 'message': 'EParamType'}

    def test_wrong_merchant_get_key_3(self):
        """ Getting key without m_lid parameter. """
        user1.merchant(method='get_key', params={})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'm_lid', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_merchant_get_key_4(self):
        """ Getting key with excess parameter. """
        user1.merchant(method='get_key', params={'m_lid': user2.merchant1.lid, 'par': '123'})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'par', 'reason': 'Should not be provided'}, 'message': 'EParamInvalid'}

    def test_wrong_merchant_get_key_5(self, _authorization):
        """ Getting key with wrong session. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='get_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid',
                                       'value': user1.headers['x-token']}, 'message': 'EStateUnauth'}

    def test_wrong_merchant_get_key_6(self, _authorization):
        """ Getting key without session. """
        user1.headers['x-token'] = None
        user1.merchant(method='get_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant == {'code': -32012, 'data': {'field': 'x-token', 'reason': 'Not present'}, 'message': 'EParamHeadersInvalid'}


@pytest.mark.positive
class TestMerchantRenewKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_renew_key_1(self, _renew_key):
        """ Renew api key for owner without 2 step auth. """
        user1.merchant(method='renew_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']

    def test_merchant_renew_key_2(self, _disable_2type, _renew_key):
        """ Renew api key for owner with 2 step auth. """
        user1.set_2type(tp='0')
        user1.merchant(method='renew_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.merch_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']

    def test_merchant_renew_key_3(self,  _delete_merchant):
        """ Renew key for special merchant. """
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        admin.set_model(model='merchant', selector={'lid': ['=', str(user1.resp_merchant['lid'])]}, data={'is_active': True})
        user1.merchant(method='renew_key', params={'m_lid': str(user1.resp_merchant['lid'])})
        assert user1.resp_merchant['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=admin.params['lid'])[0]['apikey']

    def test_merchant_renew_key_4(self, _disable_2type, _delete_merchant):
        """ Renew api key for owner with 2 step auth. """
        user1.set_2type(tp='0')
        user1.merchant(method='create', params={'title': 'Title', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        admin.set_model(model='merchant', selector={'lid': ['=', str(user1.resp_merchant['lid'])]}, data={'is_active': True})
        user1.merchant(method='renew_key', params={'m_lid': str(user1.resp_merchant['lid'])})
        assert user1.resp_merchant['message'] == 'Auth2Required'
        user1.confirm_registration(key=user1.merch_2step, code=admin.get_onetime_code(user1.email), user=user1)
        assert user1.resp_confirm['merch_token'] == admin.get_model(model='merchant', _filter='lid', value=admin.params['lid'])[0]['apikey']


@pytest.mark.negative
class TestWrongMerchantRenewKey:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_merchant_renew_key_1(self, _merchant_activate):
        """ Renew key for inactive merchant. """
        apikey = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']
        user1.merchant(method='renew_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant == {'code': -32015, 'data': {'field': 'm_lid', 'reason': 'Improper merchant'}, 'message': 'EParamMerchantInvalid'}
        assert apikey == admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']

    def test_wrong_merchant_renew_key_2(self):
        """ Renew key for other owner. """
        apikey = admin.get_model(model='merchant', _filter='lid', value=int(user2.merchant1.lid))[0]['apikey']
        user1.merchant(method='renew_key', params={'m_lid': user2.merchant1.lid})
        assert user1.resp_merchant == {'code': -32015, 'data': {'field': 'm_lid', 'reason': 'Improper merchant'}, 'message': 'EParamMerchantInvalid'}
        assert apikey == admin.get_model(model='merchant', _filter='lid', value=int(user2.merchant1.lid))[0]['apikey']

    def test_wrong_merchant_renew_key_3(self):
        """ Renew key for with wrong m_lid. """
        user1.merchant(method='renew_key', params={'m_lid': '01'})
        assert user1.resp_merchant == {'code': -32015, 'data': {'field': 'm_lid', 'reason': 'Improper merchant'}, 'message': 'EParamMerchantInvalid'}

    def test_merchant_renew_key_5(self):
        """ Renew key without lid. """
        apikey1 = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']
        apikey2 = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant2.lid))[0]['apikey']
        user1.merchant(method='renew_key', params={})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'm_lid', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}
        assert apikey1 == admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['apikey']
        assert apikey2 == admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant2.lid))[0]['apikey']

    def test_merchant_renew_key_6(self, _authorization):
        """ Renew key with wrong session token. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.merchant(method='renew_key', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid', 'value': user1.headers['x-token']},
                                       'message': 'EStateUnauth'}


@pytest.mark.positive
class TestMerchantUpdate:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_merchant_update_1(self):
        """ Updating all parameter by valid data and drop to first state. """
        merchant_data = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': 'Новый тайтл', 'params': {'param1': {'sub_param': 1}, 'param2': 2},
                                                'payment_expiry': '3600000', 'rotate_addr': True, 'apiip': '192.168.5.10, 192.168.100.5'})
        assert user1.resp_merchant['apiip'] == '192.168.5.10, 192.168.100.5'
        assert user1.resp_merchant['title'] == 'Новый тайтл'
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': merchant_data['title'], 'params': merchant_data['params'],
                                                'payment_expiry': '0', 'rotate_addr': False,
                                                'apiip': ''})
        merchant_data_default = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]
        assert merchant_data_default['params'] == merchant_data['params']
        assert merchant_data_default['payment_expiry'] == 0
        assert merchant_data_default['rotate_addr'] is False
        assert merchant_data_default['apiip'] is None

    def test_merchant_update_2(self):
        """ Updating one parameter of all. """
        merchant_data_default = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': 'Новый тайтл', 'params': {'param1': {'sub_param': 1}, 'param2': 2},
                                                'payment_expiry': '3600000', 'rotate_addr': True, 'apiip': '192.168.5.10, 192.168.100.5'})
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': 'New', 'params': None, 'payment_expiry': None,
                                                'rotate_addr': None, 'apiip': None})
        assert user1.resp_merchant['title'] == 'New'
        merchant_data = admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]
        assert merchant_data['title'] == 'New'
        assert merchant_data['params']['param1'] == {'sub_param': 1}
        assert merchant_data['params']['param2'] == 2
        assert merchant_data['payment_expiry'] == 3600000
        assert merchant_data['rotate_addr'] is True
        assert merchant_data['apiip'] == '192.168.5.10, 192.168.100.5'
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': merchant_data_default['title'],
                                                'params': merchant_data_default['params'], 'payment_expiry': '0', 'rotate_addr': False, 'apiip': ''})

    def test_merchant_update_3(self, _delete_merchant):
        """ Updating special merchant. """
        user1.merchant(method='create', params={'title': 'New', 'payway': 'visamc'})
        admin.params['lid'] = user1.resp_merchant['lid']
        user1.merchant(method='update', params={'m_lid': str(user1.resp_merchant['lid']),  'title': 'Новый тайтл',
                                                'params': {'param1': {'sub_param': 1}, 'param2': 2}, 'payment_expiry': '3600000', 'rotate_addr': True,
                                                'apiip': '192.168.5.10'})
        assert user1.resp_merchant['title'] == 'Новый тайтл'
        merchant_data = admin.get_model(model='merchant', _filter='lid', value=admin.params['lid'])[0]
        assert merchant_data['title'] == 'Новый тайтл'
        assert merchant_data['params'] == {'param1': {'sub_param': 1}, 'param2': 2}
        assert merchant_data['apiip'] == '192.168.5.10'
        assert merchant_data['rotate_addr'] is True


@pytest.mark.negative
class TestWrongMerchantUpdate:
    """ Wrong request to merchant.update method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_merchant_update_1(self):
        """ Banned on updating merchant without any parameter. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': None})
        assert user1.resp_merchant == {'code': -32002, 'data': {'reason': 'Unable to complete: improper data', 'value': {}},
                                       'message': 'EParamInvalid'}

    def test_wrong_merchant_update_2(self):
        """ Banned on updating merchant with string in apiip any parameter. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': 'String'})
        assert user1.resp_merchant == {'code': -32035, 'data': 'apiip', 'message': 'InvalidField'}

    def test_wrong_merchant_update_3(self):
        """ Banned on updating merchant with wrong ip parameter: space string. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': 'String'})
        assert user1.resp_merchant == {'code': -32035, 'data': 'apiip', 'message': 'InvalidField'}

    def test_wrong_merchant_update_4(self):
        """ Banned on updating merchant with wrong ip parameter: without point between letter. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '1921681005'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_5(self):
        """ Banned on updating merchant with wrong ip parameter: with three part number. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '192.168.10'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_6(self):
        """ Banned on updating merchant with wrong ip parameter: with five part number. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '192.168.10.1.1'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_7(self):
        """ Banned on updating merchant with wrong ip parameter: with two points before numbers. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '192..168.10.1'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_8(self):
        """ Banned on updating merchant with wrong ip parameter: with four numbers in part. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '1927.168.10.1'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_9(self):
        """ Banned on updating merchant with wrong ip parameter: with defis between numbers. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '192-168.10.1'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_10(self):
        """ Banned on updating merchant with wrong ip parameter: with space between nambers. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'apiip': '192 168 10 1'})
        assert user1.resp_merchant == {'code': -32035, 'message': 'InvalidField', 'data': 'apiip'}

    def test_wrong_merchant_update_11(self):
        """ Banned on updating merchant with wrong params parameter: string. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'params': 'String'})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'params', 'reason': 'Should be a Mapping object'}, 'message': 'EParamType'}

    def test_wrong_merchant_update_12(self):
        """ Banned on updating merchant with wrong params parameter: dict in string. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'params': "{'Param': 9}"})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'params', 'reason': 'Should be a Mapping object'}, 'message': 'EParamType'}

    def test_wrong_merchant_update_13(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: string. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'rotate_addr': 'String', 'apiip': None})
        assert user1.resp_merchant == {'code': -32003, 'data': {'field': 'rotate_addr', 'reason': 'Should be a Boolean'}, 'message': 'EParamType'}

    def test_wrong_merchant_update_14(self):
        """ Banned on updating merchant with wrong rotate_addr parameter: number. """
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'rotate_addr': 1, 'apiip': None})
        assert user1.resp_merchant == {'code': -32003, 'message': 'EParamType',
                                       'data': {'field': 'rotate_addr', 'reason': "'rotate_addr' must not be of 'int' type", 'value': 1}}

    def test_wrong_merchant_update_15(self):
        """ Updating merchant parameter without m_lid. """
        user1.merchant(method='update', params={'m_lid': None, 'title': 'New89', 'apiip': None})
        assert user1.resp_merchant == {'code': -32002, 'data': {'field': 'm_lid', 'reason': 'Should be provided'}, 'message': 'EParamInvalid'}
        assert admin.get_model(model='merchant', _filter='lid', value=int(user1.merchant1.lid))[0]['title'] != 'New89'

    def test_wrong_merchant_update_16(self):
        """ Updating merchant parameter with not own m_lid. """
        merch_title = admin.get_model(model='merchant', _filter='lid', value=int(user2.merchant1.lid))[0]['title']
        user1.merchant(method='update', params={'m_lid': user2.merchant1.lid, 'title': 'New89', 'apiip': None})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'merchant', 'reason': 'Not found'}, 'message': 'EParamNotFound'}
        assert merch_title == admin.get_model(model='merchant', _filter='lid', value=int(user2.merchant1.lid))[0]['title']

    def test_wrong_merchant_update_17(self):
        """ Updating merchant parameter with not real merchant lid. """
        user1.merchant(method='update', params={'m_lid': '01', 'title': 'New', 'apiip': None})
        assert user1.resp_merchant == {'code': -32090, 'data': {'field': 'merchant', 'reason': 'Not found'}, 'message': 'EParamNotFound'}

    def test_wrong_merchant_update_18(self, _authorization):
        """ Updating merchant parameter with wrong session token. """
        user1.headers['x-token'] += '1'
        user1.merchant(method='update', params={'m_lid': user1.merchant1.lid, 'title': 'New89', 'apiip': None})
        assert user1.resp_merchant == {'code': -32034, 'data': {'field': 'token', 'reason': 'Expired or invalid', 'value': user1.headers['x-token']},
                                       'message': 'EStateUnauth'}
