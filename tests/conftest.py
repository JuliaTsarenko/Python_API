import pytest
from users.user import User
from users.admin import Admin


def pytest_addoption(parser):
    parser.addoption(
        '--ADMIN', action='store', default='', help=' Getting admin token '
    )
    parser.addoption(
        '--USER1', action='store', default='', help=' Getting user1 email and password '
    )
    parser.addoption(
        '--USER2', action='store', default='', help=' Getting user2 email and password '
    )


@pytest.fixture(scope='session', autouse=False)
def comline(request):
    print('In comline')
    return {'admin': request.config.getoption('--ADMIN'),
            'user1': request.config.getoption('--USER1'),
            'user2': request.config.getoption('--USER2'),
            }


@pytest.yield_fixture(scope='session', autouse=True)
def start_session(comline):
    print('\n Start session')
    global admin, user1, user2
    if comline['admin'] == '':
        admin = Admin(email='viktor.yahoda@gmail.com', pwd='*Anycash15')
    else:
        print(' Admin token...')
        admin = Admin(token=comline['admin'])
    user1 = User(user=admin.get_user(email=comline['user1'].split(':')[0]), admin=admin)
    user2 = User(user=admin.get_user(email=comline['user2'].split(':')[0]), admin=admin)
    user1.authorization_by_email(user1.email, pwd=comline['user1'].split(':')[1])
    user2.authorization_by_email(user2.email, pwd=comline['user2'].split(':')[1])
    yield admin, user1, user2
    admin.delete_sessions(email=user1.email)
    admin.delete_sessions(email=user2.email)
    print('\n Finish session')


@pytest.yield_fixture(scope='function')
def _delete_user(email='anymoneyuser100@mailinator.com'):
    yield
    admin.delete_user(email=email)
    print('\n User Deleted')


@pytest.yield_fixture(scope='function')
def _delete_auth2type_token(email='@mailinator.com'):
    yield
    admin.delete_auth2type_token(email=email)
    print('\n auth2type token deleted')


@pytest.yield_fixture(scope='function')
def _disable_2type():
    yield
    user1.authorization_by_email(email=user1.email, pwd='Avtotest1!')
    user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
    user1.set_2type(tp=None)
    user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
    print('\n disable 2type')


@pytest.yield_fixture(scope='function')
def _authorization():
    yield
    user1.authorization_by_email(email=user1.email, pwd='123456')


@pytest.yield_fixture(scope='function')
def _drop_email(email='anymoneyuser1000@mailinator.com'):
    yield
    print('\n\t Start drop email')
    user1.authorization_by_email(email=email, pwd='123456')
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=email), user=user1)
    except IndexError:
        pass
    user1.update_email(email=user1.email)
    user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=email), user=user1)
    try:
        user1.second_confirm(key=user1.confirm_key, code=admin.get_onetime_code(email=email))
    except IndexError:
        pass
    user1.authorization_by_email(email=user1.email, pwd='123456')
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=user1.email), user=user1)
    except IndexError:
        pass
    print('\n\t Finish drop email')


@pytest.yield_fixture(scope='function')
def _drop_pwd(email='anymoneyuser1@mailinator.com'):
    yield
    user1.update_pwd(pwd='123456')
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=email), user=user1)
    except IndexError:
        pass
    user1.authorization_by_email(email=email, pwd='123456')
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=email), user=user1)
    except IndexError:
        pass


@pytest.yield_fixture(scope='class')
def _personal_exchange_fee():
    print(' \n Creating personal exchange fee')
    admin.create_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['UAH'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    admin.create_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    admin.create_personal_exchange_fee(in_curr=admin.currency['RUB'], out_curr=admin.currency['UAH'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    admin.create_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    admin.create_personal_exchange_fee(in_curr=admin.currency['USD'], out_curr=admin.currency['BTC'],
                                       merchant_id=user1.merchant1.id, fee=0, is_active=False)
    yield
    print(' \n Deleted personal exchange fee')
    admin.delete_personal_exchange_fee(merchant_id=user1.merchant1.id)


@pytest.mark.skip(scope='class')
def _personal_fee():
    admin.create_personal_fee(currency=admin.currency['USD'], is_active=False, payway_id=admin.payway['perfect']['id'],
                              merchant_id=user1.merchant1.lid)
    admin.create_personal_fee(currency=admin.currency['USD'], is_active=False, payway_id=admin.payway['cash_kiev']['id'],
                              merchant_id=user1.merchant1.lid)
    print(' \n Creating personal payin fee')
    yield
    print(' \n Deleted personal payin fee')


@pytest.yield_fixture(scope='class')
def delete_personal_exchange_fee():
    yield
    admin.delete_personal_exchange_fee(merchant_id=user1.merchant1.id)

@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_USD():
    yield
    admin.set_fee(tp=30, currency='USD', is_active=False, merchant_id=user1.merchant1.id)

@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_BTC():
    yield
    admin.set_fee(tp=30, currency='BTC', is_active=False, merchant_id=user1.merchant1.id)

@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_UAH():
    yield
    admin.set_fee(tp=30, currency='UAH', is_active=False, merchant_id=user1.merchant1.id)

@pytest.yield_fixture(scope='function')
def _enable_merchant_is_active():
    yield
    # print('Disabling operations fee')
    admin.set_merchant(is_active=True, lid=user1.merchant1.lid)
    admin.set_merchant(is_active=True, lid=user1.merchant2.lid)
    admin.set_merchant(is_active=True, lid=user2.merchant1.lid)
    admin.set_merchant(is_active=True, lid=user2.merchant2.lid)

@pytest.yield_fixture(scope='function')
def _enable_merchant_payout_allowed():
    yield
    # print('Disabling operations fee')
    admin.set_merchant(payout_allowed=True, lid=user1.merchant1.lid)
    admin.set_merchant(payout_allowed=True, lid=user1.merchant2.lid)
    admin.set_merchant(payout_allowed=True, lid=user2.merchant1.lid)
    admin.set_merchant(payout_allowed=True, lid=user2.merchant2.lid)

@pytest.yield_fixture(scope='function')
def _disable_st_value():
    yield
    # print('Disabling operations fee')
    admin.set_st_value(name='out_is_blocked', value=False)


@pytest.yield_fixture(scope='function')
def _enable_currency():
    yield
    # print('Disabling operations fee')
    admin.set_currency_activity(name='UAH', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='USD', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='BTC', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='RUB', is_disabled=False, is_active=True)


def _disable_personal_exchange_fee():
    yield
    admin.set_personal_exchange_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _custom_fee():
    # print('\n Enable custom fee')
    admin.set_merchant(lid=user1.merchant1.lid, is_customfee=True)
    yield
    # print('\n Disable custom fee')
    admin.set_merchant(lid=user1.merchant1.lid)


@pytest.yield_fixture(scope='function')
def _set_fee():
    yield
    admin.set_fee(is_active=False, merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _renew_key():
    print('In renew')
    yield
    user1.merchant1.akey = admin.get_merchant(lid=user1.merchant1.lid)


@pytest.yield_fixture(scope='function')
def _merchant_activate():
    admin.set_merchant(lid=user1.merchant1.lid, is_active=False)
    yield
    admin.set_merchant(lid=user1.merchant1.lid, is_active=True)

@pytest.yield_fixture(scope='function')
def _enable_exchange_operation_UAH_RUB():
    yield
    admin.set_rate_exchange(rate=2666600000, fee=0, in_currency='UAH', out_currency='RUB')

@pytest.yield_fixture(scope='function')
def _enable_exchange_operation_UAH_USD():
    yield
    admin.set_rate_exchange(rate=28199900000, fee=0, in_currency='UAH', out_currency='USD')

@pytest.yield_fixture(scope='function')
def _activate_kuna():
    yield
    admin.set_payways(name='kuna')

@pytest.yield_fixture(scope='function')
def _activate_payeer():
    yield
    admin.set_payways(name='payeer')
