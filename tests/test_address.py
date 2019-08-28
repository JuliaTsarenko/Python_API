import requests
import pytest
from json import loads
from users.sign import create_sign


class TestAddressCreate:
    """ Test creating crypto address. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_create_address_1(self, _delete_crypto_address):
        """ Creating crypto adress BTC without autoconvert by MERCHANT. """
        user1.merchant1.address_create(in_curr='BTC', out_curr=None, comment=' BTC crypto wallet... ')
        assert user1.merchant1.resp_address_create['comment'] == ' BTC crypto wallet... '
        assert user1.merchant1.resp_address_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_address_create['out_curr'] is None
        assert 'confirms' in user1.merchant1.resp_address_create
        assert 'link' in user1.merchant1.resp_address_create

    def test_create_address_2(self, _delete_crypto_address):
        """ Creating crypto address LTC without autoconvert by OWNER. """
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'create',
                               'in_curr': 'LTC', 'out_curr': None, 'comment': 'Кошелек Лайткоина "№?((*Н?'})
        assert user1.resp_delegate['comment'] == 'Кошелек Лайткоина "№?((*Н?'
        assert user1.resp_delegate['in_curr'] == 'LTC'
        assert 'rotate' in user1.resp_delegate
        assert 'status' in user1.resp_delegate

    @pytest.mark.skip(reason='Disabling exchange BTC to LTC')
    def test_create_address_3(self, _delete_crypto_address):
        """ Creating crypto adress BTC with autoconvert to LTC by OWNER. """
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'create',
                               'in_curr': 'BTC', 'out_curr': 'LTC', 'comment': None})
        assert user1.resp_delegate['comment'] is None
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['out_curr'] == 'LTC'

    @pytest.mark.skip(reason='Disabling exchange LTC to UAH')
    def test_create_adress_4(self, _delete_crypto_address):
        """ Creating crypto adress LTC with autoconvert to UAH by MERCHANT. """
        user1.merchant1.address_create(in_curr='BTC', out_curr='USD', comment='')
        assert user1.merchant1.resp_address_create['comment'] == ''
        assert user1.merchant1.resp_address_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_address_create['out_curr'] == 'USD'


class TestWrongCreateAddress:
    """ Checking wrong creating crypto address. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_create_1(self):
        """ Creating address with not crypto currency in in_curr parameter. """
        user1.merchant1.address_create(in_curr='UAH', out_curr=None, comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': 'UAH'}, 'message': 'InvalidCurrency'}

    def test_wrong_create_2(self):
        """ Creating address with autoconvert to equal currency. """
        user1.merchant1.address_create(in_curr='BTC', out_curr='BTC', comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': ['BTC', 'BTC']}, 'message': 'InvalidCurrency'}

    def test_wrong_create_3(self):
        """ Creating address with NONE in_curr parameter. """
        user1.merchant1.address_create(in_curr=None, out_curr=None, comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': None}, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not deactivated crypto currency')
    def test_wrong_create_4(self):
        """ Creating address with not active currency in in_curr parameter. """
        user1.merchant1.address_create(in_curr='BCHABC', out_curr=None, comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': 'BCHABC'}, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not deactivated crypto currency')
    def test_wrong_create_5(self):
        """ Creating address with autoconvert to not active currency. """
        user1.merchant1.address_create(in_curr='BTC', out_curr='BCHABC', comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': 'BCHABC'}, 'message': 'InvalidCurrency'}

    @pytest.mark.skip
    def test_wrong_create_6(self):
        """ Creating address with autoconvert with not active exchange pair. """
        user1.merchant1.address_create(in_curr='BTC', out_curr='BCHABC', comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': 'BCHABC'}, 'message': 'InvalidCurrency'}

    def test_wrong_create_7(self):
        """ Creating address with not real in_curr. """
        user1.merchant1.address_create(in_curr='BCT', out_curr=None, comment='123')
        assert user1.merchant1.resp_address_create == {'code': -32076, 'data': {'reason': 'BCT'}, 'message': 'InvalidCurrency'}

    def test_wrong_create_8(self):
        """ Creating address with excist parameter. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123', 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'address.create' received a redundant argument 'par'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_create_9(self):
        """ Creating address without in_curr parameter. """
        data = {'method': 'address.create',
                'params': {'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'address.create' missing 1 argument: 'in_curr'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_create_10(self):
        """ Creating address with wrong merchant lid. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '1',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_create_11(self):
        """ Creating address without merchant parameter. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_create_12(self):
        """ Creating address with wrong sign. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': 'Wrong sign',
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_create_13(self):
        """ Creating address without x-signature parameter. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_create_14(self):
        """ Creating address without utc-now parameter. """
        data = {'method': 'address.create',
                'params': {'in_curr': 'BTC', 'out_curr': None, 'comment': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('create_address_list')
class TestAddressList:
    """ Checking address list with parameters. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_address_list_1(self):
        """ Getting list for first five address by MERCHANT. """
        adm_ls = [dct['id'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count=None,
                                     begin=None, end=None)
        us_list = [dct['id'] for dct in user1.merchant1.resp_address_list['data']]
        assert us_list == adm_ls

    def test_address_list_2(self):
        """ Getting list with BEGIN parameter by OWNER: getting list address adress without first. """
        adm_ls = [dct['ctime'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'first': None,
                               'count': None, 'begin': str(adm_ls[3]), 'end': None})
        us_list = [dct['ctime'] for dct in user1.resp_delegate['data']]
        assert us_list[-1] == adm_ls[3]
        assert us_list == adm_ls[:4]

    def test_address_list_3(self):
        """ Getting list with END parameter by MERCHANT: getting all adress without lust. """
        adm_ls = [dct['ctime'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count=None,
                                     begin=None, end=str(adm_ls[1] + 1))
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        assert us_list[0] == adm_ls[1]
        assert us_list == adm_ls[1:]

    def test_address_list_4(self):
        """ Getting list with BEGIN AND END parameter by OWNER: getting all address without lust and first parameter. """
        adm_ls = [dct['ctime'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'first': None,
                               'count': None, 'begin': str(adm_ls[3]), 'end': str(adm_ls[1] + 1)})
        us_list = [dct['ctime'] for dct in user1.resp_delegate['data']]
        assert us_list[0] == adm_ls[1]
        assert us_list[-1] == adm_ls[3]
        assert us_list == adm_ls[1:4]

    def test_address_list_5(self):
        """ Getting list with COUNT parameter by MERCHANT: getting 2 address. """
        adm_ls = [dct['id'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count='2',
                                     begin=None, end=None)
        us_list = [dct['id'] for dct in user1.merchant1.resp_address_list['data']]
        assert us_list == adm_ls[:2]

    def test_address_list_6(self):
        """ Getting list with FIRST parameter by OWNER: getting list without first and second address. """
        adm_ls = [dct['id'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'first': '2',
                               'count': None, 'begin': None, 'end': None})
        us_list = [dct['id'] for dct in user1.resp_delegate['data']]
        assert us_list == adm_ls[2:]

    def test_address_list_7(self):
        """ Getting list with FIRST, COUNT, BEGIN and END parameter by MERCHANT: getting list of two address. """
        adm_ls = [dct['ctime'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first='1', count='2',
                                     begin=str(adm_ls[4]), end=str(adm_ls[1] + 1))
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        assert us_list == adm_ls[2:4]

    def test_address_list_8(self):
        """ Getting list with FIRST, COUNT and END parameter by OWNER: COUNT more than number by END filter. """
        adm_ls = [dct['ctime'] for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'first': '1',
                               'count': str(len(adm_ls)), 'begin': str(adm_ls[3]), 'end': str(adm_ls[1] + 1)})
        us_list = [dct['ctime'] for dct in user1.resp_delegate['data']]
        assert us_list[0] == adm_ls[2]
        assert us_list[-1] == adm_ls[3]

    def test_address_list_9(self):
        """ Getting list with IN_CURR, BEGIN, END, FIRST, COUNT parameter by MERCHANT. """
        adm_list = [{'in_curr': dct['in_currency_id'], 'ctime': dct['ctime']} for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        adm_list = adm_list[:5]
        user1.merchant1.address_list(in_curr='BTC', out_curr=None, is_autoconvert=None, rotate=False, first='0', count='5',
                                     begin=str(adm_list[4]['ctime']), end=str(adm_list[0]['ctime'] + 1))
        adm_list = [dct['ctime'] for dct in adm_list if dct['in_curr'] == admin.currency['BTC']]
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        print(us_list, adm_list)
        assert us_list == adm_list

    def test_address_list_10(self):
        """ Getting list with OUT_CURR, BEGIN, END, FIRST, COUNT parameter by OWNER. """
        adm_list = [{'out_curr': dct['out_currency_id'], 'ctime': dct['ctime']} for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        adm_list = adm_list[:5]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': None, 'out_curr': 'USD', 'is_autoconvert': None, 'rotate': False, 'first': '0',
                               'count': '5', 'begin': str(adm_list[4]['ctime']), 'end': str(adm_list[0]['ctime'] + 1)})
        adm_list = [dct['ctime'] for dct in adm_list if dct['out_curr'] == admin.currency['USD']]
        us_list = [dct['ctime'] for dct in user1.resp_delegate['data']]
        print(us_list, adm_list)
        assert us_list == adm_list

    def test_address_list_11(self):
        """ Getting list with IN_CURR, OUT_CURR, BEGIN, END, FIRST, COUNT parameter by MERCHANT. """
        adm_list = [{'in_curr': dct['in_currency_id'], 'out_curr': dct['out_currency_id'], 'ctime': dct['ctime']} for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        adm_list = adm_list[:5]
        user1.merchant1.address_list(in_curr='BTC', out_curr='USD', is_autoconvert=None, rotate=False, first='0', count='5',
                                     begin=str(adm_list[4]['ctime']), end=str(adm_list[0]['ctime'] + 1))
        adm_list = [dct['ctime'] for dct in adm_list if dct['in_curr'] == admin.currency['BTC'] and dct['out_curr'] == admin.currency['USD']]
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        print(us_list, adm_list)
        assert us_list == adm_list

    @pytest.mark.skip(reason='Fail')
    def test_address_list_12(self):
        """ Getting list with IN_CURR, OUT_CURR, BEGIN, END, FIRST, COUNT, IS_AUTOCONVERT parameter by OWNER. """
        adm_list = [{'ctime': dct['ctime']} for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
                    if dct['in_currency_id'] == admin.currency['BTC'] and dct['out_currency_id'] == admin.currency['USD']]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': 'BTC', 'out_curr': 'USD', 'is_autoconvert': False, 'rotate': False, 'first': None,
                               'count': None, 'begin': str(adm_list[0]['ctime']), 'end': None})
        assert user1.resp_delegate == []

    def test_address_list_13(self):
        """ Getting list with BEGIN, END, OUT_CURR and ROTATE parameter by MERCHANT. """
        adm_list = [{'out_curr': dct['out_currency_id'], 'ctime': dct['ctime']} for dct in
                    admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        adm_list = adm_list[:5]
        user1.merchant1.address_list(in_curr=None, out_curr='USD', is_autoconvert=True, rotate=False, first='0', count='5',
                                     begin=str(adm_list[4]['ctime']), end=str(adm_list[0]['ctime'] + 1))
        adm_list = [dct['ctime'] for dct in adm_list if dct['out_curr'] == admin.currency['USD']]
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        print(us_list, adm_list)
        assert us_list == adm_list

    def test_address_list_14(self):
        """ Getting list with IN_CURR, BEGIN, END, FIRST, COUNT, IS_AUTOCONVERT parameter by OWNER. """
        adm_list = [{'ctime': dct['ctime'], 'in_curr': dct['in_currency_id'], 'out_curr': dct['out_currency_id']}
                    for dct in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        adm_list = adm_list[:5]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'list',
                               'in_curr': 'BTC', 'out_curr': None, 'is_autoconvert': True, 'rotate': False, 'first': None,
                               'count': None, 'begin': str(adm_list[4]['ctime']), 'end': None})
        adm_list = [dct['ctime'] for dct in adm_list if dct['in_curr'] == admin.currency['BTC'] and dct['out_curr'] is not None]
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        assert us_list == adm_list

    @pytest.mark.skip(reason='Fail')
    def test_address_list_15(self):
        """ Getting list with BEGIN, END, FIRST, COUNT, ROTATE=TRUE parameter by OWNER. """
        adm_list = [{'ctime': dct['ctime'], 'id': dct['id'], 'rotate': dct['rotate']} for dct
                    in admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)]
        print(adm_list)
        adm_list = adm_list[:5]
        print(str(adm_list[0]['id']))
        user1.merchant1.address_edit(oid=str(adm_list[0]['id']), comment=None, rotate=True)
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=True, first='0', count='5',
                                     begin=str(adm_list[4]['ctime']), end=str(adm_list[0]['ctime'] + 1))
        adm_list = [dct['ctime'] for dct in adm_list if dct['rotate'] is True]
        us_list = [dct['ctime'] for dct in user1.merchant1.resp_address_list['data']]
        print(us_list, adm_list)
        assert us_list == adm_list


class TestWrongAddressList:
    """ Test wrong address list. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_address_list_1(self):
        """ Request with not real in_curr. """
        user1.merchant1.address_list(in_curr='BCD', out_curr=None, is_autoconvert=None, rotate=True, first=None, count=None,
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32076, 'data': {'reason': 'BCD'}, 'message': 'InvalidCurrency'}

    def test_wrong_address_list_2(self):
        """ Request with not real out_curr. """
        user1.merchant1.address_list(in_curr=None, out_curr='UHA', is_autoconvert=None, rotate=True, first=None, count=None,
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32076, 'data': {'reason': 'UHA'}, 'message': 'InvalidCurrency'}

    def test_wrong_address_list_3(self):
        """ Request with negative data in first. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first='-1', count=None,
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': 'first: - has to be a positive number'}}

    def test_wrong_address_list_4(self):
        """ Request with negative data in count. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count='-1',
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'message': 'InvalidParam',
                                                     'data': {'reason': 'count: - has to be a positive number'}}

    def test_wrong_address_list_5(self):
        """ Request with int in FIRST parameter. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=1, count=None,
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'data': {'reason': "Key 'first' must not be of 'int' type"},
                                                     'message': 'InvalidParam'}

    def test_wrong_address_list_6(self):
        """ Request with int in COUNT parameter. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count=1,
                                     begin=None, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'data': {'reason': "Key 'count' must not be of 'int' type"},
                                                     'message': 'InvalidParam'}

    def test_wrong_address_list_7(self):
        """ Request with int in BEGIN parameter. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count=None,
                                     begin=1, end=None)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'data': {'reason': "Key 'begin' must not be of 'int' type"},
                                                     'message': 'InvalidParam'}

    def test_wrong_address_list_8(self):
        """ Request with int in END parameter. """
        user1.merchant1.address_list(in_curr=None, out_curr=None, is_autoconvert=None, rotate=False, first=None, count=None,
                                     begin=None, end=1)
        assert user1.merchant1.resp_address_list == {'code': -32070, 'data': {'reason': "Key 'end' must not be of 'int' type"},
                                                     'message': 'InvalidParam'}

    def test_wrong_address_list_10(self):
        """ Request with excist parameter. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None, 'par': '1'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'address.list' received a redundant argument 'par'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_address_list_11(self):
        """ Request with not real merchant. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '1',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_address_list_12(self):
        """ Request without x-merchant parameter. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_address_list_13(self):
        """ Request with wrong sign. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': 'Wrong sign',
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_address_list_14(self):
        """ Request without x-signature parameter. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_address_list_15(self):
        """ Request without utc parameter. """
        data = {'method': 'address.list',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_address_list_16(self):
        """ Request with wrong method utc parameter. """
        data = {'method': 'address.lis',
                'params': {'in_curr': None, 'out_curr': None, 'is_autoconvert': None, 'rotate': False, 'begin': None, 'end': None,
                           'first': None, 'count': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32601, 'message': 'Method not found'}


@pytest.mark.usefixtures('_create_crypto_address')
class TestGetAddress:
    """ Checking get adress method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_1(self):
        """ Getting address by oid parameter by MERCHANT. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.address_get(oid=str(address['id']), name=None)
        assert user1.merchant1.resp_address_get['comment'] == address['comment']
        assert user1.merchant1.resp_address_get['id'] == address['id']
        assert admin.currency[user1.merchant1.resp_address_get['in_curr']] == address['in_currency_id']
        assert user1.merchant1.resp_address_get['link'] == str(address['name'])
        assert user1.merchant1.resp_address_get['name'] == address['name']

    @pytest.mark.skip(reason='Need name')
    def test_2(self):
        """ Getting address by name parameter by OWNER. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'get',
                               'oid': None, 'name': str(address['name'])})
        assert user1.resp_delegate['comment'] == address['comment']
        assert admin.currency[user1.resp_delegate['in_curr']] == address['in_currency_id']
        assert 'confirm' in user1.resp_delegate
        assert 'ctime' in user1.resp_delegate
        assert 'status' in user1.resp_delegate
        assert user1.resp_delegate['rotate'] == address['rotate']


@pytest.mark.usefixtures('_create_crypto_address')
class TestWrongGetAddress:
    """ Wrong request to get address method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_get_adress_1(self):
        """ Getting not own address. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user2.merchant1.id)[0]
        user1.merchant1.address_get(oid=str(address['id']), name=None)
        assert user1.merchant1.resp_address_get['message'] == 'NotFound'

    def test_wrong_get_address_2(self):
        """ Getting address by oid and name. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.address_get(oid=str(address['id']), name='3MCEhmhitQFBWvE8x7mvhSmVfgneiPoSWr')
        assert user1.merchant1.resp_address_get == {'code': -32090, 'data': {'reason': 'name 3MCEhmhitQFBWvE8x7mvhSmVfgneiPoSWr, '
                                                                             + 'oid ' + str(address['id'])}, 'message': 'NotFound'}

    def test_wrong_get_address_3(self):
        """ Getting address with oid and name NONE. """
        user1.merchant1.address_get(oid=None, name=None)
        assert user1.merchant1.resp_address_get == {'code': -32070, 'data': {'reason': "Missing required parameter 'name' or 'oid'"},
                                                    'message': 'InvalidParam'}

    def test_wrong_get_address_4(self):
        """ Getting address with not real oid. """
        user1.merchant1.address_get(oid='111', name=None)
        assert user1.merchant1.resp_address_get == {'code': -32090, 'data': {'reason': 'name None, oid 111'}, 'message': 'NotFound'}

    def test_wrong_get_address_5(self):
        """ Getting address with not real name. """
        user1.merchant1.address_get(oid=None, name='3MCEhmhitQFBWv11x7mvhSmVfgneiPoSWr')
        assert user1.merchant1.resp_address_get == {'code': -32090, 'data': {'reason': 'name 3MCEhmhitQFBWv11x7mvhSmVfgneiPoSWr, oid None'},
                                                    'message': 'NotFound'}

    def test_wrong_get_address_6(self):
        """ Getting address without oid and name parameter. """
        data = {'method': 'address.get',
                'params': {},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32070, 'data': {'reason': "Missing required parameter 'name' or 'oid'"},
                                          'message': 'InvalidParam'}

    def test_wrong_get_address_7(self):
        """ Getting address with wrong x-merchant. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.get',
                'params': {'oid': str(address['id']), 'name': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '1',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'}, 'message': 'InvalidMerchant'}

    def test_wrong_get_address_8(self):
        """ Getting address without x-merchant parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.get',
                'params': {'oid': str(address['id']), 'name': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_get_address_9(self):
        """ Getting address with wrong signature: Api key from other user's merchant. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.get',
                'params': {'oid': str(address['id']), 'name': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_get_address_10(self):
        """ Getting address without signature parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.get',
                'params': {'oid': str(address['id']), 'name': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_get_address_11(self):
        """ Getting address without utc-now parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.get',
                'params': {'oid': str(address['id']), 'name': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}


@pytest.mark.usefixtures('_create_crypto_address')
class TestAddressEdit:
    """ Test editing address. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_address_edit_1(self, _edit_default_crypto_address):
        """ Editing all parameter in address by MERCHANT. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.address_edit(oid=str(address['id']), comment='Comment', rotate=True)
        assert user1.merchant1.resp_address_edit['comment'] == 'Comment'
        assert user1.merchant1.resp_address_edit['rotate'] is True
        assert 'confirms' in user1.merchant1.resp_address_edit
        assert 'in_curr' in user1.merchant1.resp_address_edit
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['comment'] == 'Comment'
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['rotate'] is True

    def test_address_edit_2(self, _edit_default_crypto_address):
        """ Editing comment in address by OWNER. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'edit',
                               'oid': str(address['id']), 'comment': 'Комментарий от овнера :?*', 'rotate': None})
        assert user1.resp_delegate['comment'] == 'Комментарий от овнера :?*'
        assert user1.resp_delegate['rotate'] == address['rotate']
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['comment'] == 'Комментарий от овнера :?*'
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['rotate'] is False
        assert 'confirms' in user1.resp_delegate
        assert 'id' in user1.resp_delegate
        assert 'status' in user1.resp_delegate
        assert 'name' in user1.resp_delegate

    def test_address_edit_3(self, _edit_default_crypto_address):
        """ Editing ROTATE param in address by MERCHANT. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.address_edit(oid=str(address['id']), comment=None, rotate=True)
        assert user1.merchant1.resp_address_edit['comment'] == 'BASE-COMMENT'
        assert user1.merchant1.resp_address_edit['rotate'] is True
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['comment'] == 'BASE-COMMENT'
        assert admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]['rotate'] is True
        assert 'ctime' in user1.merchant1.resp_address_edit
        assert 'in_curr' in user1.merchant1.resp_address_edit
        assert 'link' in user1.merchant1.resp_address_edit


@pytest.mark.usefixtures('_create_crypto_address')
class TestWrongEditAddress:
    """ Test wrong editing address. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_address_editing_1(self):
        """ Editing without NONE all parameters. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user1.merchant1.address_edit(oid=str(address['id']), comment=None, rotate=None)
        assert user1.merchant1.resp_address_edit == {'code': -32070, 'data': {'reason': 'Missing equired parameter "comment" or "rotate"'},
                                                     'message': 'InvalidParam'}

    def test_wrong_address_editing_2(self):
        """ Editing with not own oid parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        user2.merchant1.address_edit(oid=str(address['id']), comment='1', rotate=True)
        assert user2.merchant1.resp_address_edit == {'code': -32090, 'data': {'reason': str(address['id'])}, 'message': 'NotFound'}

    def test_wrong_address_editing_3(self):
        """ Editing with NONE oid parameter. """
        user1.merchant1.address_edit(oid=None, comment='1', rotate=True)
        assert user1.merchant1.resp_address_edit == {'code': -32090, 'data': {'reason': None}, 'message': 'NotFound'}

    def test_wrong_address_editing_4(self):
        """ Editing without oid parameter. """
        data = {'method': 'address.edit',
                'params': {'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'address.edit' missing 1 argument: 'oid'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_address_editing_5(self):
        """ Editing with excist parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True, 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'data': {'reason': "method 'address.edit' received a redundant argument 'par'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_address_editing_6(self):
        """ Editing with not real merchant. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '1',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'data': {'reason': 'Merchant Is Not Active'},  'message': 'InvalidMerchant'}

    def test_wrong_address_editing_7(self):
        """ Editing without x-merchant parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-merchant to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_address_editing_8(self):
        """ Editing with wrong signature. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': 'WRONG SIGN',
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'data': {'reason': 'Invalid signature'}, 'message': 'InvalidSign'}

    def test_wrong_address_editing_9(self):
        """ Editing without sign parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-signature to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_editing_address_10(self):
        """ Editing without utc-now parameter. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.edit',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent)}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'data': {'reason': 'Add x-utc-now-ms to headers'}, 'message': 'InvalidHeaders'}

    def test_wrong_editing_address_11(self):
        """ Editing request to not real method. """
        address = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)[0]
        data = {'method': 'address.editt',
                'params': {'oid': str(address['id']), 'comment': 'Comment', 'rotate': True},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        assert loads(r.text)['error'] == {'code': -32601, 'message': 'Method not found'}


class TestOutCurrencies:
    """ Checking out currencies in result."""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_address_out_currencies_1(self):
        """ Getting out_currencies for in_curr BTC by MERCHANT. """
        adm_ls = [dct['out_currency_id'] for dct in admin.get_exchange(_filter='in_currency_id', value=admin.currency['BTC'])
                  if dct['is_active'] is True]
        adm_ls.sort()
        user1.merchant1.address_out_currencies(params={'in_curr': 'BTC'})
        us_ls = [admin.currency[dct] for dct in user1.merchant1.resp_address_out_currencies.values()]
        us_ls.sort()
        print(adm_ls, us_ls)
        assert us_ls == adm_ls

    @pytest.mark.skip(reason='Fail')
    def test_address_out_currencies_2(self):
        """ Getting out_currencies for in_curr ETH by OWNER. """
        adm_ls = [dct['out_currency_id'] for dct in admin.get_exchange(_filter='in_currency_id', value=admin.currency['LTC'])
                  if dct['is_active'] is True]
        adm_ls.sort()
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'address', 'merch_method': 'out_currencies', 'in_curr': 'ETH'})
        us_ls = [admin.currency[dct] for dct in user1.resp_delegate.values()]
        us_ls.sort()
        print(adm_ls, us_ls)
        assert us_ls == adm_ls


class TestWrongOutCurrencies:
    """ Checked wrong request to method address out_currencies. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_address_out_currencies_1(self):
        """ Request with not crypto currency. """
        user1.merchant1.address_out_currencies(params={'in_curr': 'USD'})
        assert user1.merchant1.resp_address_out_currencies == {'code': -32076, 'message': 'InvalidCurrency',
                                                               'data': {'reason': 'USD is not cryptocurrency'}}

    def test_wrong_address_out_currencies_2(self):
        """ Request with not active crypto currency. """
        user1.merchant1.address_out_currencies(params={'in_curr': 'BCHABC'})
        assert user1.merchant1.resp_address_out_currencies == {'code': -32077, 'message': 'InactiveCurrency', 'data': {'reason': 'BCHABC'}}

    def test_wrong_address_out_currencies_3(self):
        """ Request with NONE  crypto currency. """
        user1.merchant1.address_out_currencies(params={'in_curr': None})
        assert user1.merchant1.resp_address_out_currencies['message'] == 'InvalidCurrency'

    def test_wrong_address_out_currencies_4(self):
        """ Request without in_curr parameter. """
        user1.merchant1.address_out_currencies(params={})
        assert user1.merchant1.resp_address_out_currencies == {'code': -32602, 'message': 'InvalidInputParams',
                                                               'data': {'reason': "method 'address.out_currencies' missing 1 argument: 'in_curr'"}}

    def test_wrong_address_out_currencies_5(self):
        """ Request without excist parameter 'out_cur'. """
        user1.merchant1.address_out_currencies(params={'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.merchant1.resp_address_out_currencies == {'code': -32602, 'message': 'InvalidInputParams',
                                                               'data': {'reason': "method 'address.out_currencies' "
                                                                                  "received a redundant argument 'out_curr'"}}

    def test_wrong_address_out_currencies_6(self):
        """ Request with not real merchant. """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '1',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_address_out_currencies_7(self):
        """ Request with NONE merchant. """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_address_out_currencies_8(self):
        """ Request without x-merchant parameter. """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_address_out_currencies_9(self):
        """ Request with wrong sign: api-key from other user parameter. """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Invalid signature'}}

    def test_wrong_address_out_currencies_10(self):
        """ Request without x-signature parameter . """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_address_out_currencies_11(self):
        """ Request without x-utc-now-ms parameter . """
        data = {'method': 'address.out_currencies', 'params': {'in_curr': 'BTC'}, 'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user2.merchant1.akey, data['params'], time_sent)}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-utc-now-ms to headers'}}


@pytest.mark.skip(reason='Need payin on crypto address')
class TestAddressHistory:
    """ Checking address history method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_address_history_1(self):
        """ Getting full information by payin type on address by MERCHANT. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.merchant1.address_history(params={'addr_id': addr_id, 'is_autoconvert': None, 'tp': 'payin', 'status': None,
                                                'first': None, 'count': None})
        assert user1.merchant1.resp_address_history == {'code': -32076, 'message': 'InvalidCurrency',
                                                        'data': {'reason': 'USD is not cryptocurrency'}}

    def test_address_history_2(self):
        """ Getting full information by autopayin type on address by OWNER. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.delegate(params={'m_lid': addr_id, 'merch_model': 'address', 'merch_method': 'address_history',
                               'addr_id': None, 'is_autoconvert': None, 'tp': 'autopayin', 'status': None, 'first': None, 'count': None})
        assert user1.resp_delegate == ''

    def test_address_history_3(self):
        """ Getting full information by payin type on address with first  and count parameter by OWNER. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.delegate(params={'m_lid': addr_id, 'merch_model': 'address', 'merch_method': 'address_history',
                               'addr_id': None, 'is_autoconvert': None, 'tp': 'autopayin', 'status': None, 'first': '1', 'count': '2'})
        assert user1.resp_delegate == ''

    def test_address_history_4(self):
        """ Getting information by payin type on address with first and count parameter by OWNER. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.merchant1.address_history(params={'addr_id': addr_id, 'is_autoconvert': None, 'tp': 'payin', 'status': None, 'first': None,
                                                'count': None})
        assert user1.resp_delegate == ''

    def test_address_history_5(self):
        """ Getting information by autopayin type on address with first and count and is autoconvert type by MERCHANT. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.merchant1.address_history(params={'addr_id': addr_id, 'is_autoconvert': None, 'tp': 'payin', 'status': None, 'first': None,
                                                'count': None})
        assert user1.merchant1.resp_address_history == ''

    def test_address_history_6(self):
        """ Getting information by autopayin type on address with first and count and is autoconvert with status by OWNER. """
        addr_id = admin.get_crypto_adress(_filter='merchant_id', value=user1.merchant1.id)
        user1.delegate(params={'m_lid': addr_id, 'merch_model': 'address', 'merch_method': 'address_history',
                               'addr_id': None, 'is_autoconvert': None, 'tp': 'autopayin', 'status': None, 'first': '1', 'count': '3'})
        assert user1.delegaet == ''


@pytest.mark.usefixtures('_create_crypto_address')
class TestWrongAddressHistory:
    """ Checking wrong request address_history method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_address_history_1(self):
        """ Request with not own addr_id. """
        addr_id = [dct['id'] for dct in admin.get_crypto_adress(_filter=None, value=None) if dct['merchant_id'] != user1.merchant1.id]
        user1.merchant1.address_history(params={'addr_id': addr_id, 'is_autoconvert': None, 'tp': 'payin', 'status': None, 'first': None,
                                                'count': None})







