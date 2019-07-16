import pytest
from users.user import User


class TestRegistration:
    """ Registration by email. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_registration_1(self, _delete_user):
        """ Success registration by email with min length password. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(key=User.confirm_key, code=admin.get_onetime_code('anymoneyuser100@mailinator.com'))
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 20
        assert admin.get_session(email='anymoneyuser100@mailinator.com') == User.headers['x-token']
        user1.authorization_by_email(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        assert user1.resp_authorization['session']['token'] == admin.get_session(email='anymoneyuser100@mailinator.com')


    def test_registration_2(self, _delete_user):
        """ Registration to busy not activated email. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*456')
        User.confirm_registration(code=admin.get_onetime_code(email='anymoneyuser100@mailinator.com'),
                                  key=User.confirm_key)
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 20
        assert admin.get_session(email='anymoneyuser100@mailinator.com') == User.headers['x-token']
        user1.authorization_by_email(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        assert user1.resp_authorization['error'] == {"code": -32090, "message": "NotFound", "data": "pwd"}
        user1.authorization_by_email(email='anymoneyuser100@mailinator.com', pwd='Ac*456')
        assert user1.resp_authorization['session']['token'] == admin.get_session(email='anymoneyuser100@mailinator.com')


    def test_registration_3(self, _delete_user):
        """ Registration on busy and activated email. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(code=admin.get_onetime_code(email='anymoneyuser100@mailinator.com'),
                                  key=User.confirm_key)
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        assert User.resp_registration['error'] == {"code": -32033, "message": "Unique", "data": "email"}

    def test_registration_4(self, _delete_user):
        """ Registration with double activation. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        code = admin.get_onetime_code(email='anymoneyuser100@mailinator.com')
        User.confirm_registration(code=code, key=User.confirm_key)
        User.confirm_registration(code=code, key=User.confirm_key)
        # print('\n',  User.resp_confirm)
        assert User.resp_confirm['error'] == {"code": -32033, "message": "Auth2Drop", "data": "key"}

    def test_registration_5(self, _delete_user):
        """ Registration without confirmation code. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(code=None, key=User.confirm_key)
        assert User.resp_confirm['error'] == {"code": -32033, "message": "Auth2Wrong"}

    def test_registration_6(self, _delete_user):
        """ Registration with wrong one time code. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(code='000000', key=User.confirm_key)
        assert User.resp_confirm['error'] == {"code": -32033, "message": "Auth2Wrong"}
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 10

    def test_registration_7(self, _delete_user):
        """ Registration without confirm token. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(code=admin.get_onetime_code(email='anymoneyuser100@mailinator.com'), key=None)
        assert User.resp_confirm['error'] == {'code': -32040, 'message': 'Req400', 'data': 'Bad Request'}
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 10

    def test_registration_8(self, _delete_user):
        """ Registration with wrong confirm token. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        User.confirm_registration(code=admin.get_onetime_code(email='anymoneyuser100@mailinator.com'), key='1')
        assert User.resp_confirm['error'] == {"code": -32033, "message": "Auth2Drop", "data": "key"}
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 10

    def test_registration_9(self, _delete_user):
        """ Registration with deactivated confirm token. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        code = admin.get_onetime_code(email='anymoneyuser100@mailinator.com')
        User.cancel_2auth(key=User.confirm_key)
        User.confirm_registration(code=code, key=User.confirm_key)
        assert User.resp_confirm['error'] == {"code": -32033, "message": "Auth2Drop", "data": "key"}
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 10

    def test_registration_10(self):
        """ Registration without password. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd=None)
        assert User.resp_registration['error'] == {"code": -32070, "message": "InvalidParam", "data": "pwd"}

    def test_registration_11(self):
        """ Registration with password less than 6 symbols. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*12')
        assert User.resp_registration['error'] == {"code": -32070, "message": "InvalidPassLength", "data": "pwd"}

    def test_registration_12(self):
        """ Registration without email. """
        User.registration(email=None, pwd='Ac*123')
        assert User.resp_registration['error'] == {"code": -32080, "message": "InvalidLoginType", "data": "logintype"}

    def test_registration_13(self):
        """ Registration with wrong format email: without @. """
        User.registration(email='anymoneyuser100mailinator.com', pwd='Ac*123')
        assert User.resp_registration['error'] == {'code': -32000, 'message': 'InvalidField'}
        assert admin.get_user(email='anymoneyuser100mailinator.com')['exception'] == "User wasn't found"

    def test_registration_14(self):
        """ Registration with wrong format email: double @. """
        User.registration(email='anymoneyuser100@@mailinator.com', pwd='Ac*123')
        assert User.resp_registration['error'] == {'code': -32000, 'message': 'InvalidField'}

    def test_registration_15(self):
        """ Registration with wrong format email: without string before @. """
        User.registration(email='@zzz.com', pwd='Ac*123')
        assert User.resp_registration['error'] == {'code': -32000, 'message': 'InvalidField'}
        assert admin.get_user(email='@zzz.com')['exception'] == "User wasn't found"

    def test_registration_16(self):
        """ Registration with wrong format email: without domain part. """
        User.registration(email='anymoneyuser100@mailinator', pwd='Ac*123')
        assert User.resp_registration['error'] == {'code': -32000, 'message': 'InvalidField'}

    def test_registration_17(self):
        """ Registration with wrong format email: without host part. """
        User.registration(email='anymoneyuser100@.com', pwd='Ac*123')
        assert User.resp_registration['error'] == {'code': -32000, 'message': 'InvalidField'}
        assert admin.get_user(email='anymoneyuser100.com')['exception'] == "User wasn't found"


class TestAuthorization:
    """ Autorization by email including two step autentification. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    @pytest.mark.skip(reason='Avoiding wrong captcha')
    def test_autorization_1(self):
        """ Autorization in to not real account. """
        user1.authorization_by_email(email='161616@mailinator.com', pwd='Ac*123')
        assert 'error' in user1.resp_authorization
        assert admin.get_session(email='161616@mailinator.com')['exception'] == "Session wasn't found"

    def test_autorization_2(self):
        """ Success autorization. """
        user1.authorization_by_email(email=user1.email, pwd='123456')
        assert user1.resp_authorization['session']['token'] == admin.get_session(email=user1.email)

    def test_autorization_3(self):
        """ Autorization with wrong password. """
        user1.authorization_by_email(email=user1.email, pwd='111111')
        assert user1.resp_authorization['error'] == {'code': -32000, 'message': 'NotFound', 'data': 'pwd'}

    def test_autorization_4(self, _delete_auth2type_token, _delete_user,):
        """ Authorization in to not activated account. """
        User.registration(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        user1.authorization_by_email(email='anymoneyuser100@mailinator.com', pwd='Ac*123')
        assert 'key' in user1.resp_authorization['error']['data']
        assert admin.get_user(email='anymoneyuser100@mailinator.com')['lvl'] == 10

    def test_autorization_5(self, _disable_2type):
        """ Autorization with 2 step autorization. """
        user1.set_2type(tp='0')
        user1.authorization_by_email(email=user1.email, pwd='123456')
        assert 'key' in user1.resp_authorization['error']['data']
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        assert user1.resp_confirm['session']['token'] == admin.get_session(user1.email)

    @pytest.mark.skip(reason=' Avoiding wrong captcha ')
    def test_autorization_6(self, _delete_auth2type_token, _disable_2type):
        """ Authorization with 2 step with wrong code. """
        user1.set_2type(tp=0)
        user1.authorization_by_email(email=user1.email, pwd='123456')
        user1.confirm_registration(code='000000', key=user1.confirm_key, user=user1)
        assert 'error' in user1.resp_confirm

    @pytest.mark.skip(reason=' Avoiding wrong captcha ')
    def test_autorization_7(self, _delete_auth2type_token, _disable_2type):
        """ Authorization after deactivated 2 step auth token. """
        user1.set_2type(tp=0)
        user1.authorization_by_email(email=user1.email, pwd='123456')
        code = admin.get_onetime_code(email=user1.email)
        user1.cancel_2auth(key=user1.confirm_key)
        user1.confirm_registration(code=code, key=user1.confirm_key, user=user1)
        assert 'error' in user1.resp_confirm

    def test_autorization_8(self, _authorization):
        """ Logout user. """
        user1.logout()
        assert user1.headers['x-token'] != admin.get_session(email=user1.email)

    def test_autorization_9(self):
        """ Renew session. """
        user1.renew_session()
        assert 'token' in user1.resp_renew
        assert user1.headers['x-token'] == admin.get_session(email=user1.email)

    def test_autorization_10(self, _authorization):
        """ Renew session with wrong session token. """
        user1.headers['x-token'] = '1'
        user1.renew_session()
        assert user1.resp_renew['error'] == {'code': -32041, 'message': 'InvalidToken', 'data': 'Unauthorized'}

    def test_autorization_11(self):
        """ Authorization without password. """
        user1.authorization_by_email(email=user1.email, pwd=None)
        assert user1.resp_authorization['error'] == {'code': -32000, 'message': 'NotFound', 'data': 'pwd'}

    def test_autorization_12(self):
        """ Getting session by forgot password. """
        user1.forgot(email=user1.email)
        assert 'key' in user1.resp_forgot['error']['data']
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.forgot_key, user=user1)
        assert user1.resp_confirm['session']['token'] == admin.get_session(email=user1.email)

    def test_autorization_13(self, _disable_2type):
        """ Banned on getting session by forgot password with added two step auth. """
        user1.set_2type(tp=0)
        user1.forgot(email=user1.email)
        assert user1.resp_forgot['error'] == {'code': -32000, 'message': 'Unavailable', 'data': 'not enough factors for authorization'}

    def test_autorization_14(self):
        """ Getting session for not real email. """
        user1.forgot(email='anycashuser100@mailinator.com')
        assert user1.resp_forgot['error'] == {'code': -32000, 'message': 'NotFound', 'data': 'email'}

    def test_autorization_15(self):
        """ Getting session without email. """
        user1.forgot(email=None)
        assert user1.resp_forgot['error'] == {'code': -32000, 'message': 'InvalidLoginType', 'data': 'logintype'}


class TestUpdate:
    """ Updating email.  """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_update_email_1(self, _drop_email):
        """ Update email and authorization by him. """
        user1.update_email(email='anymoneyuser1000@mailinator.com')
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        assert user1.resp_confirm['session']['token'] == admin.get_session(email='anymoneyuser1000@mailinator.com')
        assert admin.get_user(email='anymoneyuser1000@mailinator.com')['email'] == 'anymoneyuser1000@mailinator.com'
        assert admin.get_session(email=user1.email)['exception'] == "Session wasn't found"
        user1.authorization_by_email(email='anymoneyuser1000@mailinator.com', pwd='123456')
        assert user1.resp_authorization['session']['token'] == admin.get_session(email='anymoneyuser1000@mailinator.com')

    def test_update_email_2(self, _disable_2type, _drop_email):
        """ Update email with activated two step auth. """
        user1.set_2type(tp=0)
        user1.update_email(email='anymoneyuser1000@mailinator.com')
        user1.confirm_registration(code=admin.get_onetime_code(user1.email), key=user1.confirm_key, user=user1)
        assert admin.get_user(email='anymoneyuser1000@mailinator.com')['exception'] == "User wasn't found"
        user1.second_confirm(code=admin.get_onetime_code(user1.email), key=user1.confirm_key)
        assert admin.get_session(email=user1.email)['exception'] == "Session wasn't found"
        assert user1.resp_second_confirm['session']['token'] == admin.get_session(email='anymoneyuser1000@mailinator.com')
        assert admin.get_user(email='anymoneyuser1000@mailinator.com')['email'] == 'anymoneyuser1000@mailinator.com'

    def test_update_email_3(self):
        """ Update email on booked email. """
        user1.update_email(email=user2.email)
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'Forbidden', 'data': user2.email}
        assert admin.get_user(email='anymoneyuser1@mailinator.com')['email'] == 'anymoneyuser1@mailinator.com'

    def test_update_email_4(self):
        """ Update email with wrong format: without string before @. """
        user1.update_email(email='@mailinator.com')
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}

    def test_update_email_5(self):
        """ Update email with wrong format: with @@. """
        user1.update_email(email='anymoneyuser10@@mailinator.com')
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}
        assert admin.get_user(email='anymoneyuser10@@mailinator.com')['exception'] == "User wasn't found"

    def test_update_email_6(self):
        """ Update email with wrong format: without domain part after @. """
        user1.update_email(email='anymoneyuser10@')
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}

    def test_update_email_7(self):
        """ Update email with wrong format: without @. """
        user1.update_email(email='anymoneyuser10mailinator.com')
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}
        assert admin.get_user(email='anymoneyuser10mailinator.com')['exception'] == "User wasn't found"

    def test_update_email_8(self):
        """ Update email with wrong format: without empty string. """
        user1.update_email(email='')
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}

    def test_update_email_9(self):
        """ Update email without email string. """
        user1.update_email(email=None)
        assert user1.resp_update_email['error'] == {'code': -32000, 'message': 'InvalidField'}


@pytest.mark.skip(reason='Save password 123456 on real account. ')
class TestUpdatePassword:
    """ Updating password. """

    def test_update_password_1(self, _drop_pwd):
        """ Update password. """
        user1.update_pwd(pwd='000000')
        assert user1.resp_update_pwd['result']['session']['token'] == admin.get_session(email=user1.email)
        user1.authorization_by_email(email=user1.email, pwd='000000')
        assert user1.resp_authorization['result']['session']['token'] == admin.get_session(email=user1.email)

    def test_update_password_2(self, _disable_2type, _drop_pwd):
        """ Update password with 2 step auth. """
        user1.set_2type(tp=0)
        user1.update_pwd(pwd='000000')
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        assert user1.resp_confirm['result']['session']['token'] == admin.get_session(email=user1.email)
        user1.authorization_by_email(email=user1.email, pwd='000000')
        user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
        assert user1.resp_confirm['result']['session']['token'] == admin.get_session(email=user1.email)

    def test_update_password_3(self):
        """ Update password with empty password. """
        user1.update_pwd(pwd=None)
        assert 'error' in user1.resp_update_pwd

    def test_update_password_4(self):
        """ Update password with string shorter than 6 symbols. """
        user1.update_pwd(pwd='12345')
        assert 'error' in user1.resp_update_pwd
        assert admin.get_session(email=user1.email) == user1.headers['x-token']


class TestUpdateLanguage:
    """ Updating language. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_update_language_1(self):
        """ Update language. """
        user1.update_lang(lang='en')
        assert user1.headers['x-token'] == admin.get_session(email=user1.email)
        assert admin.get_user(email=user1.email)['lang_id'] == admin.lang_id['en']
        user1.update_lang(lang='ru')

    def test_update_language_2(self):
        """ Update language with wrong lang id. """
        user1.update_lang(lang='bb')
        assert user1.resp_update_lang['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'lang'}

    def test_update_language_3(self):
        """ Update language without lang id. """
        user1.update_lang(lang=None)
        assert user1.resp_update_lang['error'] == {'code': -32000, 'message': 'InvalidField', 'data': 'lang'}


class TestUpdateTimezone:
    """ Updating timezone. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_update_timezone_1(self):
        """ Update timezone. """
        user1.update_tz(tz='Australia/Sydney')
        assert admin.get_user(email=user1.email)['timezone'] == 'Australia/Sydney'
        user1.update_tz(tz='Europe/Amsterdam')

    def test_update_timezone_2(self):
        """ Update timezone with wrong format. """
        user1.update_tz(tz='Australia')
        assert user1.resp_update_tz['error'] == {'code': -32000, 'message': 'InvalidParam'}
        assert admin.get_user(email=user1.email)['timezone'] == 'Europe/Amsterdam'

    def test_update_timezone_3(self):
        """ Update timezone with None value. """
        user1.update_tz(tz=None)
        assert user1.resp_update_tz['error'] == {'code': -32000, 'message': 'InvalidParam'}


class TestUpdateSafemode:
    """ Updating safemode. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_update_safemode_1(self):
        """ Update safemode. """
        user1.update_safemode(safemode=True)
        assert user1.resp_update_safemode['user']['safemode'] is True
        assert admin.get_user(email=user1.email)['safemode'] is True
        user1.update_safemode(safemode=False)
        assert user1.resp_update_safemode['user']['safemode'] is False
        assert admin.get_user(email=user1.email)['safemode'] is False

    def test_update_safemode_2(self):
        """ Update safemode with None in parameter. """
        user1.update_safemode(safemode=None)
        assert admin.get_user(email=user1.email)['safemode'] is False

    @pytest.mark.skip
    def test_update_safemode_3(self):
        """ Update safemode with non boolean parameter: string. """
        user1.update_safemode(safemode='Test')
        assert admin.get_user(email=user1.email)['safemode'] is False


class TestCurrencyList:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_currency_1(self):
        """ Getting full list by all currency.  """
        user1.currency_list(first=None, count=100)
        ls_currency = [ls['name'] for ls in user1.resp_currency_list['data']]
        ls_currency.sort()
        ls_admin = [ls for ls in admin.currency]
        ls_admin.sort()
        assert ls_currency == ls_admin

    def test_list_currency_2(self):
        """ Getting list of two elements. """
        user1.currency_list(first=None, count=2)
        assert len(user1.resp_currency_list['data']) == 2

    def test_list_currency_3(self):
        """ Getting list without first element. """
        user1.currency_list(first=None, count=None)
        second_element = user1.resp_currency_list['data'][1]
        user1.currency_list(first=1, count=None)
        first_element = user1.resp_currency_list['data'][0]
        assert first_element == second_element

    def test_list_currency_4(self):
        """ Getting data from currency. """
        user1.currency_list(first=None, count=None)
        ls = [ls for ls in user1.resp_currency_list['data'][0]]
        assert 'is_active' in ls
        assert 'is_crypto' in ls
        assert 'name' in ls
        assert 'precision' in ls


class TestPaywayList:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_list_payway_1(self):
        """ Getting full list of payway. """
        user1.payway_list(tp=None)
        assert 'currency' in user1.resp_payway_list[0]
        assert 'direction' in user1.resp_payway_list[0]
        assert 'params' in user1.resp_payway_list[0]
        assert 'payway' in user1.resp_payway_list[0]

    def test_list_payway_2(self):
        """ Getting list of payway for sci type. """
        user1.payway_list(tp='sci')
        ls_payway = [pw['payway'] for pw in user1.resp_payway_list]
        assert 'btc' not in ls_payway
        assert 'kuna' not in ls_payway
        assert 'payeer' in ls_payway

    def test_list_payway_3(self):
        """ Getting list of payway for crypto type. """
        user1.payway_list(tp='crypto')
        ls_payway = [pw['payway'] for pw in user1.resp_payway_list]
        assert 'btc' in ls_payway
        assert 'kuna' not in ls_payway
        assert 'payeer' not in ls_payway

    def test_list_payway_4(self):
        """ Getting list of payway for crypto type. """
        user1.payway_list(tp='cheque')
        ls_payway = [pw['payway'] for pw in user1.resp_payway_list]
        assert 'btc' not in ls_payway
        assert 'kuna' in ls_payway
        assert 'payeer' not in ls_payway

    def test_list_payway_5(self):
        """ Getting list with wrong tp. """
        user1.payway_list(tp='ch')
        assert user1.resp_payway_list['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'tp'}


class TestBookmark:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_create_bookmark_1(self):
        """ Creating bookmark with ASCII symbols. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='ASCII !@#$%^&*()_=+',
                              params={'params1': 1, 'params2': {'params3': 3}}, order=True)
        assert user1.resp_bookmark_create['order'] == 1
        assert user1.resp_bookmark_create['params'] == {'params1': 1, 'params2': {'params3': 3}}
        assert user1.resp_bookmark_create['title'] == 'ASCII !@#$%^&*()_=+'
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert user1.resp_bookmark_list['data'][0]['id'] == user1.bookmark_oid
        assert user1.resp_bookmark_list['data'][0]['title'] == 'ASCII !@#$%^&*()_=+'
        assert len(user1.resp_bookmark_list['data']) == 1
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)
        assert user1.resp_bookmark_delete['id'] == user1.bookmark_oid
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert len(user1.resp_bookmark_list['data']) == 0


    def test_create_bookmark_2(self):
        """ Creating bookmark with kirills symbols. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='New bk', params={}, order='0')
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='Закладка Тестовая ', params={}, order='0')
        assert user1.resp_bookmark_create['title'] == 'Закладка Тестовая '
        assert user1.resp_bookmark_create['params'] == {}
        assert user1.resp_bookmark_create['order'] == 0
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        ls_oid = [oid['id'] for oid in user1.resp_bookmark_list['data']]
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=1, count=1)
        assert len(user1.resp_bookmark_list['data']) == 1
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=ls_oid[0])
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=ls_oid[1])

    def test_create_bookmark_3(self):
        """ Create bookmark without m_lid. """
        user1.bookmark_create(m_lid=None, title='New', params={}, order=1)
        assert user1.resp_bookmark_create['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'm_lid'}
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert len(user1.resp_bookmark_list['data']) == 0


    def test_create_bookmark_4(self):
        """ Create bookmark for wrong m_lid. """
        user1.bookmark_create(m_lid=1, title='New', params={}, order=0)
        assert user1.resp_bookmark_create['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': 'Server Error'}


    def test_create_bookmark_5(self):
        """ Create bookmark without title. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title=None, params={}, order=False)
        assert user1.resp_bookmark_create['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'title'}


    def test_create_bookmark_6(self):
        """ Create bookmark with string in params. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='Test', params='String', order=False)
        assert user1.resp_bookmark_create['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'params'}


    def test_create_bookmark_7(self):
        """ Create bookmark without params. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='Test', params=None, order=False)
        assert user1.resp_bookmark_create['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'params'}


    def test_create_bookmark_8(self):
        """ Create bookmark without order. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='Test', params=None, order=None)
        assert user1.resp_bookmark_create['error'] == {'code': -32000, 'message': 'InvalidParam', 'data': 'params'}


    def test_create_bookmark_9(self):
        """ Create bookmark without session. """
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='Test', params=None, order=1)
        assert user1.resp_bookmark_create['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Server Error'}
        user1.headers['x-token'] = session

    def test_update_bookmark_1(self):
        """ Updating bookmark after creating. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='New', params={'param1': 1}, order=1)
        user1.bookmark_update(m_lid=user1.merchant1.lid, title='New1', oid=user1.bookmark_oid, order=0)
        assert user1.resp_bookmark_update['title'] == 'New1'
        assert user1.resp_bookmark_update['order'] == 0
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert user1.resp_bookmark_list['data'][0]['title'] == 'New1'
        assert user1.resp_bookmark_list['data'][0]['order'] == 0
        user1.bookmark_update(m_lid=user1.merchant1.lid, title=None, oid=user1.bookmark_oid, order=False)
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert user1.resp_bookmark_list['data'][0]['title'] == 'New1'
        assert user1.resp_bookmark_list['data'][0]['order'] == 0
        user1.bookmark_update(m_lid=user1.merchant1.lid, title='NewNew', oid=user1.bookmark_oid, order=None)
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert user1.resp_bookmark_list['data'][0]['title'] == 'NewNew'
        assert user1.resp_bookmark_list['data'][0]['order'] == 0
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)

    def test_update_bookmark_2(self):
        """ Updating bookmark with wrong title and order. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='New', params={'param1': 1}, order=True)
        user1.bookmark_update(m_lid=user1.merchant1.lid, title='1', oid=333, order=True)
        assert 'error' in user1.resp_bookmark_update
        user1.bookmark_update(m_lid=None, title='1', oid=user1.bookmark_oid, order=True)
        assert 'error' in user1.resp_bookmark_update
        user1.bookmark_update(m_lid=20000, title='1', oid=user1.bookmark_oid, order=True)
        assert 'error' in user1.resp_bookmark_update
        user1.bookmark_list(m_lid=user1.merchant1.lid, first=None, count=None)
        assert user1.resp_bookmark_list['data'][0]['title'] == 'New'
        assert user1.resp_bookmark_list['data'][0]['order'] == 1
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)

    def test_delete_bookmark_1(self):
        """ Delete not own bookmark. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='New', params={'param1': 1}, order=True)
        user2.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)
        assert 'error' in user2.resp_bookmark_delete
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)

    def test_delete_bookmark_2(self):
        """ Delete bookmark without session. """
        user1.bookmark_create(m_lid=user1.merchant1.lid, title='New', params={'param1': 1}, order=True)
        session, user1.headers['x-token'] = user1.headers['x-token'], None
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)
        assert user1.resp_bookmark_delete['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': 'Server Error'}
        user1.headers['x-token'] = session
        user1.bookmark_delete(m_lid=user1.merchant1.lid, oid=user1.bookmark_oid)
