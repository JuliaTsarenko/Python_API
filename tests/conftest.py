import pytest
from users.user import User
from users.admin import Admin
from users.tools import *


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
    user1 = User(user=admin.get_user(email=comline['user1'].split(':')[0]), pwd=comline['user1'].split(':')[1], admin=admin)
    user2 = User(user=admin.get_user(email=comline['user2'].split(':')[0]), pwd=comline['user2'].split(':')[1], admin=admin)
    user1.authorization_by_email(user1.email, pwd=user1.pwd)
    user2.authorization_by_email(user2.email, pwd=user2.pwd)
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
    user1.authorization_by_email(email=user1.email, pwd=user1.pwd)
    user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)
    user1.set_2type(tp=None)
    user1.confirm_registration(code=admin.get_onetime_code(email=user1.email), key=user1.confirm_key, user=user1)


@pytest.yield_fixture(scope='function')
def _authorization():
    yield
    user1.authorization_by_email(email=user1.email, pwd=user1.pwd)


@pytest.yield_fixture(scope='function')
def _drop_email(email='anymoneyuser1000@mailinator.com'):
    yield
    print('\n\t Start drop email')
    user1.authorization_by_email(email=email, pwd=user1.pwd)
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
    user1.authorization_by_email(email=user1.email, pwd=user1.pwd)
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=user1.email), user=user1)
    except IndexError:
        pass
    print('\n\t Finish drop email')


@pytest.yield_fixture(scope='function')
def _drop_pwd():
    """ Drop pwd for user1"""
    yield
    user1.update_pwd(pwd=user1.pwd)
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=user1.email), user=user1)
    except IndexError:
        pass
    user1.authorization_by_email(email=user1.email, pwd=user1.pwd)
    try:
        user1.confirm_registration(key=user1.confirm_key, code=admin.get_onetime_code(email=user1.email), user=user1)
    except IndexError:
        pass


@pytest.yield_fixture(scope='class')
def _personal_exchange_fee():
    print('\n Creating personal exchange fee')
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
    print(' \n Deleting personal exchange fee')
    admin.delete_personal_exchange_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='class')
def _transfer_fee():
    print('\n Creating transfer fee')
    admin.create_personal_fee(currency='USD', merchant_id=user1.merchant1.id, is_active=False, tp=30)
    admin.create_personal_fee(currency='UAH', merchant_id=user1.merchant1.id, is_active=False, tp=30)
    admin.create_personal_fee(currency='RUB', merchant_id=user1.merchant1.id, is_active=False, tp=30)
    admin.create_personal_fee(currency='BTC', merchant_id=user1.merchant1.id, is_active=False, tp=30)
    yield
    print(' \n Deleting transfer fee')
    admin.delete_personal_fee(merchant_id=user1.merchant1.id, tp=30)


@pytest.yield_fixture(scope='class')
def _payout_fee():
    print('\n Creating payout fee')
    admin.create_personal_fee(currency='USD', merchant_id=user1.merchant1.id, is_active=False, tp=10,
                              payway_id=admin.payway['perfect']['id'])
    admin.create_personal_fee(currency='USD', merchant_id=user1.merchant1.id, is_active=False, tp=10,
                              payway_id=admin.payway['cash_kiev']['id'])
    admin.create_personal_fee(currency='UAH', merchant_id=user1.merchant1.id, is_active=False, tp=10)
    admin.create_personal_fee(currency='RUB', merchant_id=user1.merchant1.id, is_active=False, tp=10)
    admin.create_personal_fee(currency='BTC', merchant_id=user1.merchant1.id, is_active=False, tp=10)
    yield
    print(' \n Deleting payout fee')
    admin.delete_personal_fee(merchant_id=user1.merchant1.id, tp=10)


@pytest.yield_fixture(scope='class')
def _sci_fee():
    print('\n Creating sci fee')
    admin.create_personal_fee(currency='UAH', merchant_id=user1.merchant1.id, is_active=False, tp=40)
    admin.create_personal_fee(currency='RUB', merchant_id=user1.merchant1.id, is_active=False, tp=40)
    admin.create_personal_fee(currency='BTC', merchant_id=user1.merchant1.id, is_active=False, tp=40)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['perfect'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['cash_kiev'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='BTC', is_active=False, payway_id=admin.payway_id['btc'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['privat24'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='USD', is_active=False, merchant_id=user1.merchant1.id, tp=46,
                              payway_id=admin.payway_id['anycash'])
    admin.create_personal_fee(currency='BTC', is_active=False, merchant_id=user1.merchant1.id, tp=46,
                              payway_id=admin.payway_id['anycash'])
    admin.create_personal_fee(currency='UAH', is_active=False, merchant_id=user1.merchant1.id, tp=46,
                              payway_id=admin.payway_id['anycash'])
    admin.create_personal_fee(currency='RUB', is_active=False, merchant_id=user1.merchant1.id, tp=46,
                              payway_id=admin.payway_id['anycash'])
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['perfect'],
                              merchant_id=user1.merchant1.id, tp=45)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['cash_kiev'],
                              merchant_id=user1.merchant1.id, tp=45)
    admin.create_personal_fee(currency='BTC', is_active=False, payway_id=admin.payway_id['btc'],
                              merchant_id=user1.merchant1.id, tp=45)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['privat24'],
                              merchant_id=user1.merchant1.id, tp=45)
    yield
    print(' \n Deleting sci fee')
    admin.set_fee(currency_id=admin.currency['USD'], is_active=False, payway_id=admin.payway_id['anycash'], tp=46)
    admin.set_fee(currency_id=admin.currency['BTC'], is_active=False, payway_id=admin.payway_id['anycash'], tp=46)
    admin.set_fee(currency_id=admin.currency['UAH'], is_active=False, payway_id=admin.payway_id['anycash'], tp=46)
    admin.set_fee(currency_id=admin.currency['RUB'], is_active=False, payway_id=admin.payway_id['anycash'], tp=46)
    admin.delete_personal_fee(merchant_id=user1.merchant1.id, tp=40)
    admin.delete_personal_fee(merchant_id=user1.merchant1.id, tp=45)
    admin.delete_personal_fee(merchant_id=user1.merchant1.id, tp=46)


@pytest.yield_fixture(scope='class')
def _personal_operation_fee():
    print('\n Creating personal PAYIN fee')
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['perfect'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['cash_kiev'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='BTC', is_active=False, payway_id=admin.payway_id['btc'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['privat24'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['exmo'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['kuna'],
                              merchant_id=user1.merchant1.id)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['visamc'],
                              merchant_id=user1.merchant1.id, tp=10)
    yield
    print('\n Deleting personal PAYIN fee')
    admin.delete_personal_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='class')
def _personal_sci_fee():
    print('\n Creating personal SCI fee')
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['perfect'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='USD', is_active=False, payway_id=admin.payway_id['cash_kiev'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='BTC', is_active=False, payway_id=admin.payway_id['btc'],
                              merchant_id=user1.merchant1.id, tp=40)
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['privat24'],
                              merchant_id=user1.merchant1.id, tp=40)
    yield
    print('\n Deleting personal fee')
    admin.delete_personal_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='class')
def _personal_operation_payout_fee():
    print('\n Creating personal PAYOUT fee')
    admin.create_personal_fee(currency='UAH', is_active=False, payway_id=admin.payway_id['visamc'], tp=10,
                              merchant_id=user1.merchant1.id)
    yield
    print('\n Deleting personal PAYOUT fee')
    admin.delete_personal_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='class')
def delete_personal_exchange_fee():
    yield
    admin.delete_personal_exchange_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_USD():
    yield
    admin.set_fee(tp=30, currency_id=admin.currency['USD'], is_active=False, merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_BTC():
    yield
    admin.set_fee(tp=30, currency_id=admin.currency['BTC'], is_active=False, merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _disable_personal_operation_fee_transfer_UAH():
    yield
    admin.set_fee(tp=30, currency_id=admin.currency['UAH'], is_active=False, merchant_id=user1.merchant1.id)

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
    admin.set_currency_activity(name='BCHABC', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='ETH', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='USDT', is_disabled=False, is_active=True)
    admin.set_currency_activity(name='LTC', is_disabled=False, is_active=True)


@pytest.yield_fixture(scope='function')
def _disable_personal_exchange_fee():
    yield
    admin.set_personal_exchange_fee(merchant_id=user1.merchant1.id)


@pytest.yield_fixture(scope='function')
def _custom_fee():
    admin.set_merchant(lid=user1.merchant1.lid, is_customfee=True)
    yield
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
    admin.set_rate_exchange(rate=bl(2.46305), fee=0, in_currency='UAH', out_currency='RUB')

@pytest.yield_fixture(scope='function')
def _enable_exchange_operation_UAH_USD():
    yield
    admin.set_rate_exchange(rate=bl(25.91463), fee=bl(0.04), in_currency='UAH', out_currency='USD')

@pytest.yield_fixture(scope='function')
def _enable_exchange_operation_RUB_UAH():
    yield
    admin.set_rate_exchange(rate=bl(2.48757), fee=0, in_currency='RUB', out_currency='UAH')

@pytest.yield_fixture(scope='function')
def _enable_exchange_operation_USD_UAH():
    yield
    admin.set_rate_exchange(rate=bl(25.7355), fee=bl(0.03), in_currency='USD', out_currency='UAH')

@pytest.yield_fixture(scope='function')
def _activate_kuna():
    yield
    admin.set_payways(name='kuna')


@pytest.yield_fixture(scope='function')
def _activate_payeer():
    yield
    admin.set_payways(name='payeer')

@pytest.yield_fixture(scope='class')
def _validate_pwd_off():
    admin.set_front_params()
    yield

@pytest.yield_fixture(scope='function')
def _registration_and_delete():
    session = user1.headers['x-token']
    user1.registration(email='anymoneyuser100@mailinator.com', pwd='Aa/123')
    user1.confirm_registration(key=User.confirm_key, code=admin.get_onetime_code('anymoneyuser100@mailinator.com'),
                               user=user1)
    yield
    user1.headers['x-token'] = session
    admin.delete_user(email='anymoneyuser100@mailinator.com')


@pytest.yield_fixture(scope='class')
def _create_crypto_address():
    print('Creating crypto address. ')
    if not admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id):
        user1.merchant1.address_create(in_curr='BTC', out_curr=None, comment=None)
    if not admin.get_crypto_adress(_filter='merchant_id', value=user2.merchant1.id):
        user2.merchant1.address_create(in_curr='BTC', out_curr=None, comment=None)
    yield


@pytest.yield_fixture(scope='function')
def _delete_crypto_address():
    yield
    _id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['id']
    admin.delete_crypto_address(_id=_id)


@pytest.yield_fixture(scope='function')
def _edit_default_crypto_address():
    print('Start editing default')
    _id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['id']
    user1.merchant1.address_edit(params={'oid': str(_id), 'comment': 'BASE-COMMENT', 'rotate': False})
    yield
    user1.merchant1.address_edit(params={'oid': str(_id), 'comment': 'BASE-COMMENT', 'rotate': False})
    print('Finish editing default')


@pytest.yield_fixture(scope='class')
def create_address_list():
    """ Creating list address for test if count of address by merchant less than 5. """
    if len(admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)) < 5:
        print('Start creating list address. ')
        user1.merchant1.address_create(params={'in_curr': 'BTC', 'out_curr': None, 'comment': None})
        user1.merchant1.address_create(params={'in_curr': 'BTC', 'out_curr': 'USD', 'comment': None})
        user1.merchant1.address_create(params={'in_curr': 'ETH', 'out_curr': None, 'comment': None})
        user1.merchant1.address_create(params={'in_curr': 'BTC', 'out_curr': 'USD', 'comment': None})
        user1.merchant1.address_create(params={'in_curr': 'LTC', 'out_curr': None, 'comment':None})
    yield


@pytest.yield_fixture(scope='function')
def _activate_pwcurrency():
    yield
    admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='UAH', is_out=True, is_active=True,
                  tech_min=bl(0.01), tech_max=bl(3000))
    admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='USD', is_out=True, is_active=True,
                  tech_min=bl(0.01), tech_max=bl(3000))
    admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='RUB', is_out=True, is_active=True,
                  tech_min=bl(0.01), tech_max=bl(3000))
    admin.set_pwc(pw_id=admin.payway_id['anycash'], currency='BTC', is_out=True, is_active=True,
                  tech_min=bl(0.000001), tech_max=bl(3))


@pytest.yield_fixture(scope='function')
def _activate_merchant_payways():
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
    yield


@pytest.yield_fixture(scope='function')
def _activate_merchant_payways_after():
    yield
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
    admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)


@pytest.yield_fixture(scope='class')
def _create_other_type_order():
    print('In creating')
    if not admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 20}):
        admin.set_wallet_amount(balance=bl(20), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_curr='UAH', out_curr='USD', in_amount='20', out_amount=None)
    if not admin.get_order({'merchant_id': user1.merchant2.id, 'tp': 0}):
        print('In other merchant. ')
        admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(10), tech_max=bl(100))
        user1.merchant2.payin_create(payway='visamc', amount='10', in_curr='UAH', out_curr='UAH')
    yield


@pytest.yield_fixture(scope='class')
def _creating_payin_list():
    if len(admin.get_order({'merchant_id': user1.merchant1.id, 'tp': 0})) < 7:
        admin.set_pwc(pw_id=admin.payway['visamc']['id'], currency='UAH', is_out=False, is_active=True,
                      tech_min=bl(10), tech_max=bl(100))
        admin.set_pwc(pw_id=admin.payway['perfect']['id'], currency='USD', is_out=False, is_active=True,
                      tech_min=bl(1), tech_max=bl(100))
        user1.merchant1.payin_create(payway='visamc', amount='12', in_curr='UAH', out_curr='UAH')
        user1.merchant1.payin_create(payway='payeer', amount='50', in_curr='RUB', out_curr='RUB')
        user1.merchant1.payin_create(payway='visamc', amount='25', in_curr='UAH', out_curr='UAH')
        user1.merchant1.payin_create(payway='visamc', amount='70', in_curr='UAH', out_curr='USD')
        user1.merchant1.payin_create(payway='visamc', amount='60', in_curr='UAH', out_curr='USD')
        user1.merchant1.payin_create(payway='perfect', amount='5', in_curr='USD', out_curr='UAH')
    yield


@pytest.yield_fixture(scope='class')
def _default_crypto_address():
    admin.set_crypto_address(merchant_id=user1.merchant1.id)
    yield
    admin.set_crypto_address(merchant_id=user1.merchant1.id)


@pytest.fixture(scope='class')
def allow_many_session():
    admin.update_user(key={'id': user1.id}, data={'many_sess_allowed': True})
    user1.authorization_by_email(email=user1.email, pwd=user1.pwd)


@pytest.yield_fixture(scope='class')
def _create_convert_order():
    if not [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if ls['tp'] == 20]:
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert(method='create', params={'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None,
                                                         'externalid': user1.merchant1._id()})
    if not [ls for ls in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant2.id) if ls['tp'] == 20]:
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant2.lid)
        user1.merchant2.convert(method='create', params={'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None,
                                                         'externalid': user1.merchant2._id()})
    yield


@pytest.yield_fixture(scope='class')
def _create_sci_pay_order():
    admin.set_pwc(pw_id=admin.payway_id['visamc'], currency='UAH', is_out=False, is_active=True, tech_min=bl(1), tech_max=bl(100))
    user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH', 'payway': 'visamc',
                                                     'expiry': '60s', 'externalid': user1.merchant1._id()})
    yield



@pytest.fixture(scope='function')
def reate_payin_with_uaccount():
    if not admin.get_order(selector={'merchant_id': user1.merchant1.id, 'tp': 0, 'uaccount': '5168********7159'}):
        user1.merchant1.payin_create(payway='visamc', amount='0.01', in_curr='UAH', payer='5168********7159')


@pytest.yield_fixture(scope='class')
def _create_sci_pay_list():
    print('Calculating sci_pay orders ...')
    if len([dct for dct in admin.get_model(model='order', _filter='merchant_id', value=user1.merchant1.id) if dct['tp'] == 40]) < 5:
        print('Creating sci_pay orders ...')
        user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH', 'payway': 'visamc',
                                                         'expiry': '60s', 'externalid': user1.merchant1._id()})
        user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'USD', 'out_curr': 'UAH', 'payway': 'payeer',
                                                         'expiry': '60s', 'externalid': user1.merchant1._id()})
        user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'UAH', 'out_curr': 'USD', 'payway': 'privat24',
                                                         'expiry': '60s', 'externalid': user1.merchant1._id()})
        user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'UAH', 'out_curr': 'UAH', 'payway': 'privat24',
                                                         'expiry': '60s', 'externalid': user1.merchant1._id()})
        user1.merchant1.sci_pay(method='create', params={'amount': '50', 'in_curr': 'USD', 'out_curr': 'UAH', 'payway': 'perfect',
                                                         'expiry': '60s', 'externalid': user1.merchant1._id()})
    yield
