import pytest
from users.tools import *
from users.user import User


class TestPwmerchactivePublicList:
    """ Getting list of public and active payways. """

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_pwmerchactive_public_list_1(self):
        """ Getting full list public payway. """
        admin_payway = [pw['name'] for pw in admin.get_model(model='payway', _filter='is_active', value=True) if pw['is_public'] is True]
        admin_payway.sort()
        user1.pwmerchactive(method='public_list', params={})
        user1.resp_pwmerchactive.sort()
        assert admin_payway == user1.resp_pwmerchactive


class TestWrongPwmerchactivePublicList:
    """ Test wrong requests  to public_list method. """

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_pwmerchactive_public_list_1(self):
        """ Request with excess parameter 'm_lid'. """
        user1.pwmerchactive(method='public_list', params={'m_lid': user1.merchant1.lid})
        assert user1.resp_pwmerchactive == {'code': -32602,
                                            'data': {'reason': "method 'pwmerchactive.public_list' received a redundant argument 'm_lid'"},
                                            'message': 'InvalidInputParams'}

    def test_wrong_pwmerchactive_public_list_2(self, _authorization):
        """ Request with wrong x-token . """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.pwmerchactive(method='public_list', params={})
        assert user1.resp_pwmerchactive == {'code': -32091, 'message': 'Unauth',
                                            'data': {'reason': 'Invalid or expired session token', 'token': user1.headers['x-token']}}

    def test_wrong_pwmerchactive_public_list_3(self, _authorization):
        """ Request with NONE x-token . """
        user1.headers['x-token'] = None
        user1.pwmerchactive(method='public_list', params={})
        assert user1.resp_pwmerchactive == {'code': -32003, 'data': {'reason': 'Add x-token to headers'}, 'message': 'InvalidHeaders'}


class TestPwmerchactiveUpdate:
    """ Updating payways for merchant. """

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_pwmerchactive_update_1(self):
        """ Enabling payway for merchant. """
        admin_payway = [pw['name'] for pw in admin.get_model(model='payway', _filter='is_active', value=True) if pw['is_public'] is True][0]
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id[admin_payway], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant2.id, payway_id=admin.payway_id[admin_payway], is_active=False)
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': admin_payway, 'is_active': True})
        assert user1.resp_pwmerchactive == {'is_active': True, 'merchant_id': user1.merchant1.id, 'payway_name': admin_payway}
        assert admin.payway_id[admin_payway] in [pw['payway_id'] for pw in
                                                 admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                                                 if pw['is_active'] is True]
        assert admin.payway_id[admin_payway] in [pw['payway_id'] for pw in
                                                 admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant2.id)
                                                 if pw['is_active'] is False]
        admin.set_pwmerchactive(merch_id=user1.merchant2.id, payway_id=admin.payway_id[admin_payway], is_active=True)

    def test_pwmerchactive_update_2(self):
        """ Disabling payway for merchant. """
        admin_payway = [pw['name'] for pw in admin.get_model(model='payway', _filter='is_active', value=True) if pw['is_public'] is True][0]
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id[admin_payway], is_active=True)
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': admin_payway, 'is_active': False})
        assert user1.resp_pwmerchactive == {'is_active': False, 'merchant_id': user1.merchant1.id, 'payway_name': admin_payway}
        assert admin.payway_id[admin_payway] in [pw['payway_id'] for pw in
                                                 admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                                                 if pw['is_active'] is False]
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway_id[admin_payway], is_active=True)


class TestWrongPwmerchactiveUpdate:
    """ Wrong updating pwmerchactive. """

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_pwmerchactive_update_1(self):
        """ Banned on disabling payway with deactivated is_public option by payway's table. """
        admin.set_payways(name='bchabc', is_active=True, is_public=False, is_disabled=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, is_active=True, payway_id=admin.payway_id['bchabc'])
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'bchabc', 'is_active': False})
        assert user1.resp_pwmerchactive == {'code': -32062, 'data': {'reason': "Payway name bchabc - can't be updated manually"},
                                            'message': 'UnavailPayway'}
        assert admin.payway_id['bchabc'] in [pw['payway_id'] for pw in
                                             admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                                             if pw['is_active'] is True]
        admin.set_payways(name='bchabc', is_active=True, is_public=True, is_disabled=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, is_active=True, payway_id=admin.payway_id['bchabc'])

    def test_wrong_pwmerchactive_update_2(self):
        """ Banned on enabling payway with deactivated is_public option by payway's table. """
        admin.set_payways(name='bchabc', is_active=True, is_public=False, is_disabled=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, is_active=False, payway_id=admin.payway_id['bchabc'])
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'bchabc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32062, 'data': {'reason': "Payway name bchabc - can't be updated manually"},
                                            'message': 'UnavailPayway'}
        assert admin.payway_id['bchabc'] in [pw['payway_id'] for pw in
                                             admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                                             if pw['is_active'] is False]
        admin.set_payways(name='bchabc', is_active=True, is_public=True, is_disabled=False)

    @pytest.mark.skip(reason='Need fix in admin')
    def test_wrong_pwmerchactive_update_3(self):
        """ Requests with not active payway. """
        payway = [pw['name'] for pw in admin.get_model(model='payway', _filter='is_active', value=False)][0]
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': payway, 'is_active': True})
        assert user1.resp_pwmerchactive == ""

    def test_wrong_pwmerchactive_update_4(self):
        """ Requests with not real payway. """
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'visam', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32060, 'data': {'reason': 'payway_name'}, 'message': 'InvalidPayway'}

    def test_wrong_pwmerchactive_update_5(self):
        """ Requests with NONE payway. """
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': None, 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32602, 'data': {'reason': "method 'pwmerchactive.update' missing 1 argument: 'payway_name'"},
                                            'message': 'InvalidInputParams'}

    def test_wrong_pwmerchactive_update_6(self):
        """ Requests with wrong m_lid. """
        user1.pwmerchactive(method='update', params={'m_lid': '01', 'payway_name': 'visamc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32090, 'data': {'field': 'm_lid', 'reason': 'Merchant with lid 1 was not found'},
                                            'message': 'NotFound'}

    def test_wrong_pwmerchactive_update_7(self):
        """ Requests with NONE m_lid. """
        user1.pwmerchactive(method='update', params={'m_lid': None, 'payway_name': 'visamc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32602, 'data': {'reason': "method 'pwmerchactive.update' missing 1 argument: 'm_lid'"},
                                            'message': 'InvalidInputParams'}

    def test_wrong_pwmerchactive_update_8(self):
        """ Requests with not str m_lid. """
        user1.pwmerchactive(method='update', params={'m_lid': int(user1.merchant1.lid), 'payway_name': 'visamc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32070, 'data': {'reason': "Key 'm_lid' must not be of 'int' type"}, 'message': 'InvalidParam'}

    def test_wrong_pwmerchactive_update_9(self):
        """ Requests with NONE is_active parameter. """
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'visamc', 'is_active': None})
        assert user1.resp_pwmerchactive == {'code': -32602, 'data': {'reason': "method 'pwmerchactive.update' missing 1 argument: 'is_active'"},
                                            'message': 'InvalidInputParams'}

    def test_wrong_pwmerchactive_update_10(self, _authorization):
        """ Requests with wrong x-token parameter. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'visamc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32091, 'data': {'reason': 'Invalid or expired session token', 'token': user1.headers['x-token']},
                                            'message': 'Unauth'}

    def test_wrong_pwmerchactive_update_11(self, _authorization):
        """ Requests with NONE x-token parameter. """
        user1.headers['x-token'] = None
        user1.pwmerchactive(method='update', params={'m_lid': user1.merchant1.lid, 'payway_name': 'visamc', 'is_active': True})
        assert user1.resp_pwmerchactive == {'code': -32003, 'data': {'reason': 'Add x-token to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_personal_operation_payout_fee', )
class TestPwmerchactiveList:

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_pwmerchactive_list_1(self):
        """ Getting full list of payway for merchant default parameter. Checking all payways. """
        merch_payway = {dct['payway_id'] for dct in admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                        if dct['is_active'] is True}
        print('Merch payway', merch_payway)
        adm_payways_in = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=False)
                          if dct['is_active'] is True}
        print(adm_payways_in)
        payways_in = list(merch_payway & adm_payways_in)
        payways_in.sort()
        print('Payways_in', payways_in)
        adm_payways_out = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=True)
                           if dct['is_active'] is True}
        payways_out = list(merch_payway & adm_payways_out)
        payways_out.sort()
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': None})
        us_list_in = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['in']]
        us_list_in.sort()
        us_list_out = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['out']]
        us_list_out.sort()
        print(us_list_in, payways_in)
        print(us_list_out, payways_out)
        assert us_list_in == payways_in
        assert us_list_out == payways_out

    def test_pwmerchactive_list_2(self):
        """ Getting full list payways for currency UAH. Checking all payways. """
        merch_payway = {dct['payway_id'] for dct in admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                        if dct['is_active'] is True}
        adm_payway_in = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=False)
                        if dct[admin.currency('UAH')]}
        payways_in = list(merch_payway & adm_payway_in)
        payways_in.sort()
        adm_payway_out = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=True)
                          if dct[admin.currency('UAH')]}
        payways_out = list(merch_payway & adm_payway_out)
        payways_out.sort()
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': 'UAH', 'is_out': None})
        us_list_in = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['in']]
        us_list_in.sort()
        us_list_out = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['out']]
        us_list_out.sort()
        print(payways_in, us_list_in)
        assert us_list_in == payways_in
        assert us_list_out == payways_out
        assert equal_list(_list=[dct for dct in user1.resp_pwmerchactive['in'].values() for dct in dct], elem='UAH')
        assert equal_list(_list=[dct for dct in user1.resp_pwmerchactive['out'].values() for dct in dct], elem='UAH')

    def test_pwmerchactive_list_3(self):
        """ Getting full IN list. Checking all payways. """
        merch_payway = {dct['payway_id'] for dct in admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                        if dct['is_active'] is True}
        adm_payways = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=False)}
        payways_in = list(merch_payway & adm_payways)
        payways_in.sort()
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': False})
        us_list = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['in']]
        us_list.sort()
        print(us_list, payways_in)
        assert us_list == payways_in
        assert 'out' not in user1.resp_pwmerchactive

    def test_pwmerchactive_list_4(self):
        """ Getting OUT list for USD. Checking all payways. """
        merch_payway = {dct['payway_id'] for dct in admin.get_model(model='pwmerchactive', _filter='merchant_id', value=user1.merchant1.id)
                        if dct['is_active'] is True}
        adm_payways = {dct['payway_id'] for dct in admin.get_model(model='pwcurrency', _filter='is_out', value=True)
                       if dct['currency_id'] == admin.currency['USD']}
        payways_out = list(merch_payway & adm_payways)
        payways_out.sort()
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': 'USD', 'is_out': True})
        us_list = [admin.payway_id[pw] for pw in user1.resp_pwmerchactive['out']]
        us_list.sort()
        print(us_list, payways_out)
        assert us_list == payways_out
        assert 'in' not in user1.resp_pwmerchactive

    def test_pwmerchactive_list_5(self):
        """ Getting common fee for operation payin for currency RUB. """
        admin.set_fee(mult=bl(2), add=bl(1), _min=bl(3), _max=bl(100), payway_id=admin.payway_id('perfect'), tp=0, currency_id=admin.currency('USD'))
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': 'USD', 'is_out': False})
        assert user1.resp_pwmerchactive['perfect']['USD'] == {'add': '1', 'max': '100', 'min': '3', 'mult': '0.02'}

    def test_pwmerchactive_list_6(self, _custom_fee, _set_fee):
        """ Getting common fee for payin: payeer USD and common + personal fee for payout: visamc UAH. """
        admin.set_fee(mult=bl(1), add=bl(1), _min=bl(3), _max=bl(50), payway_id=admin.payway_id('payeer'), tp=0, currency_id=admin.currency('USD'))
        admin.set_fee(mult=bl(1), add=bl(1), _min=bl(3), _max=bl(50), payway_id=admin.payway_id('visamc'), tp=10, currency_id=admin.currency('UAH'))
        admin.set_fee(mult=pers(0.5), add=bl(0.5), _min=bl(1), _max=bl(100), payway_id=admin.payway_id('visamc'), tp=10, currency_id=admin.currency('UAH'),
                      merchant_id=user1.merchant1.id)
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive['in']['payeer']['USD'] == {'add': '1', 'max': '50', 'min': '3', 'mult': '1'}
        assert user1.resp_pwmerchactive['out']['visamc']['UAH'] == {'add': '0.5', 'max': '100', 'min': '1', 'mult': '0.005'}


class TestWrongPwmerchactiveList:
    """ Wrong requests to pwmerchactive list method. """

    def test_0(self, start_session):
        """ Warming up. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_pwmerchactive_list_1(self):
        """ Requests with not real currency. """
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': 'UDS', 'is_out': False})
        assert user1.resp_pwmerchactive == {'code': -32076, 'message': 'InvalidCurrency',
                                            'data': {'field': 'curr', 'reason': 'Invalid currency name'}}

    def test_wrong_pwmerchactive_list_2(self):
        """ Requests with non bool parameter IS_OUT. """
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': {}})
        assert user1.resp_pwmerchactive == {'code': -32070, 'message': 'InvalidParam', 'data': {'reason': "Field 'is_out' must be bool"}}

    def test_wrong_pwmerchactive_list_3(self):
        """ Requests with not real merchant. """
        user1.pwmerchactive(method='list', params={'m_lid': '01', 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32010, 'message': 'InvalidMerchant',
                                            'data': {'field': 'm_lid', 'reason': 'Merchant with lid 1 was not found'}}

    @pytest.mark.skip(reason='Fail')
    def test_wrong_pwmerchactive_list_4(self, _merchant_activate):
        """ Requests with not active merchant. """
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}

    def test_wrong_pwmerchactive_list_5(self):
        """ Requests with excess parameter. """
        user1.pwmerchactive(method='list', params={'m_lid': '01', 'curr': None, 'is_out': None, 'par': '123'})
        assert user1.resp_pwmerchactive == {'code': -32602, 'message': 'InvalidInputParams',
                                            'data': {'reason': "method 'pwmerchactive.list' received a redundant argument 'par'"}}

    def test_wrong_pwmerchactive_list_6(self):
        """ Requests with NONE m_lid parameter. """
        user1.pwmerchactive(method='list', params={'m_lid': None, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32602, 'message': 'InvalidInputParams',
                                            'data': {'reason': "method 'pwmerchactive.list' missing 1 argument: 'm_lid'"}}

    def test_wrong_pwmerchactive_list_7(self):
        """ Requests with NONE m_lid parameter. """
        user1.pwmerchactive(method='list', params={'m_lid': None, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32602, 'message': 'InvalidInputParams',
                                            'data': {'reason': "method 'pwmerchactive.list' missing 1 argument: 'm_lid'"}}

    def test_wrong_pwmerchactive_list_8(self, _authorization):
        """ Requests with wrong session token. """
        user1.headers['x-token'] = user1.headers['x-token'] + '1'
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32091, 'message': 'Unauth',
                                            'data': {'reason': 'Invalid or expired session token', 'token': user1.headers}}

    def test_wrong_pwmerchactive_list_9(self, _authorization):
        """ Requests with NONE session token. """
        user1.headers['x-token'] = None
        user1.pwmerchactive(method='list', params={'m_lid': user1.merchant1.lid, 'curr': None, 'is_out': None})
        assert user1.resp_pwmerchactive == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-token to headers'}}

