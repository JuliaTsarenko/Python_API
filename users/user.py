import requests
import random
from users.merchant import Merchant
from json import loads
from string import ascii_uppercase
from users.admin import Admin
import pprint


requests.packages.urllib3.disable_warnings()


class User:

    wapi_url = 'https://anymoney-back-p3.e-cash.pro/_handler/wapi/'
    eapi_url = 'https://anymoney-back-p3.e-cash.pro/_handler/eapi/'

    confirm_key = ''
    headers = {'x-token': ''}
    id = ''
    resp_registration = {}
    resp_confirm = {}

    def __init__(self, user=None, pwd=None, admin=None):
        if user:
            print(user)
            print(pwd)
            self.params = {'token': ''}
            self.email = user['email']
            self.pwd = pwd
            self.id = user['id']
            self.headers = {'x-token': ''}
            merchants = admin.get_merchants(owner_id=self.id)
            print(merchants)
            self.merchant2 = Merchant(next(merchants))
            self.merchant1 = Merchant(next(merchants))

    @staticmethod
    def ex_id():
        return random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000))

    @staticmethod
    def registration(email, pwd):
        r = requests.post(url=User.wapi_url,
                          json={'method': 'account.register',
                                'params': {'email': email, 'pwd': pwd}, 'jsonrpc': 2.0, 'id': User.ex_id()},
                          verify=False)
        print(r.text)
        try:
            if type(loads(r.text)['error']['data']) == dict:
                User.confirm_key = loads(r.text)['error']['data']['key']
                return loads(r.text)['error']['data']['key']
            else:
                User.resp_registration = loads(r.text)
        except KeyError:
                User.resp_registration = loads(r.text)

    @staticmethod
    def confirm_registration(key, code, user=None):
        if not user:
            r = requests.post(url=User.wapi_url,
                              json={'method': 'account.auth2confirm', 'params': {'key': str(key), 'code': str(code)},
                                    'jsonrpc': 2.0, 'id': User.ex_id()},
                              verify=False)
            print(r.text)
            try:
                User.headers['x-token'] = loads(r.text)['result']['session']['token']
                User.resp_confirm = loads(r.text)['result']
            except KeyError:
                User.resp_confirm = loads(r.text)
        else:
            r = requests.post(url=User.wapi_url,
                              json={'method': 'account.auth2confirm', 'params': {'key': str(key), 'code': str(code)},
                                    'jsonrpc': 2.0, 'id': User.ex_id()},
                              verify=False)
            print(r.text)
            if 'result' in loads(r.text):
                try:
                    user.headers['x-token'] = loads(r.text)['result']['session']['token']
                    user.resp_confirm = loads(r.text)['result']
                except KeyError:
                    user.resp_confirm = loads(r.text)['result']
            else:
                try:
                    if type(loads(r.text)['error']['data']) == dict:
                        try:
                            user.confirm_key = loads(r.text)['error']['data']['key']
                            return loads(r.text)['error']['data']['key']
                        except KeyError:
                            user.resp_confirm = loads(r.text)
                    else:
                        user.resp_confirm = loads(r.text)
                except KeyError:
                    user.resp_confirm = loads(r.text)

    @staticmethod
    def cancel_2auth(key):
        requests.post(url=User.wapi_url,
                      json={'method': 'account.auth2cancel', 'params': {'key': str(key)}, 'jsonrpc': 2.0, 'id': User.ex_id()},
                      verify=False)

    def second_confirm(self, key, code):
        r = requests.post(url=User.wapi_url,
                          json={'method': 'account.auth2confirm', 'params': {'key': str(key), 'code': str(code)},
                                'jsonrpc': 2.0, 'id': User.ex_id()},
                          verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
            self.resp_second_confirm = loads(r.text)['result']
        except KeyError:
            self.resp_second_confirm = loads(r.text)

    def authorization_by_email(self, email, pwd):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.login',
                                'params': {'email': email, 'pwd': pwd}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          verify=False)
        print(r.text)
        if 'result' in loads(r.text):
            try:
                self.headers['x-token'] = loads(r.text)['result']['session']['token']
                self.resp_authorization = loads(r.text)['result']
            except KeyError:
                self.resp_authorization = loads(r.text)
        else:
            print('2')
            try:
                if type(loads(r.text)['error']['data']) == dict:
                    self.confirm_key = loads(r.text)['error']['data']['key']
                    self.resp_authorization = loads(r.text)
                else:
                    self.resp_authorization = loads(r.text)
            except KeyError:
                print('3')
                self.resp_authorization = loads(r.text)

    def logout(self):
        requests.post(url=self.wapi_url,
                      json={'method': 'account.logout', 'params': {}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                      headers=self.headers, verify=False)

    def renew_session(self):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.renew', 'params': {}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print('\n', 'self.headers', self.headers)
        print(r.text)
        try:
            self.headers['x-token'] = loads(r.text)['result']['token']
            self.resp_renew = loads(r.text)['result']
        except KeyError:
            self.resp_renew = loads(r.text)

    def set_2type(self, tp=None):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.set_auth2type', 'params': {'tp': str(tp)}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            if type(loads(r.text)['error']['data']) == dict:
                self.confirm_key = loads(r.text)['error']['data']['key']
        except KeyError:
            try:
                self.headers['x-token'] = loads(r.text)['result']['session']['token']
            except KeyError:
                self.resp_2type = loads(r.text)

    def forgot(self, email):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.forgot', 'params': {'email': email}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          verify=False)
        print(r.text)
        try:
            if type(loads(r.text)['error']['data']) == dict:
                self.forgot_key = loads(r.text)['error']['data']['key']
                self.resp_forgot = loads(r.text)
            else:
                self.resp_forgot = loads(r.text)
        except KeyError:
            self.resp_forgot = loads(r.text)

    def update_email(self, email):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_email',
                                'params': {'email': email}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            if type(loads(r.text)['error']['data']) == dict:
                self.confirm_key = loads(r.text)['error']['data']['key']
                return loads(r.text)['error']['data']['key']
            else:
                self.resp_update_email = loads(r.text)
        except KeyError:
            self.resp_update_email = loads(r.text)

    def update_pwd(self, pwd):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_pwd',
                                'params': {'pwd': pwd}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        if 'result' in loads(r.text):
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
            self.resp_update_pwd = loads(r.text)['result']
        else:
            try:
                if type(loads(r.text)['error']['data']) == dict:
                    self.confirm_key = loads(r.text)['error']['data']['key']
                    return loads(r.text)['error']['data']['args']['key']
                else:
                    self.resp_update_pwd = loads(r.text)
            except KeyError:
                self.resp_update_pwd = loads(r.text)

    def update_tz(self, tz):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_tz', 'params': {'tz': tz},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print('Update tz - ', r.text)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
        except KeyError:
            self.resp_update_tz = loads(r.text)

    def update_lang(self, lang):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_lang', 'params': {'lang': lang},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print('Update lang - ', r.text)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
        except KeyError:
            self.resp_update_lang = loads(r.text)

    def update_safemode(self, safemode):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_safemode', 'params': {'safemode': safemode},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print('Update safemode - ', r.text)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
            self.resp_update_safemode = loads(r.text)['result']
        except KeyError:
            self.resp_update_safemode = loads(r.text)

    def currency_list(self, first, count):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'currency.list', 'params': {'first': first, 'count': count},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        self.resp_currency_list = loads(r.text)['result']

    def payway_list(self, tp):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'payway.list', 'params': {'tp': tp}, 'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_payway_list = loads(r.text)['result']
        except KeyError:
            self.resp_payway_list = loads(r.text)

    def merchant_create(self, title):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.create', 'params': {'title': title},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_merch_create = loads(r.text)['result']
            self.merch_lid = loads(r.text)['result']['lid']
            param_list = list(loads(r.text)['result'])
            param_list.sort()
            self.merch_create_param_list = param_list
        except KeyError:
            self.resp_merch_create = loads(r.text)

    def merchant_switch(self, m_lid, is_active):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.switch', 'params': {'m_lid': m_lid, 'is_active': is_active},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_merch_switch = loads(r.text)['result']
            ls = list(loads(r.text)['result'])
            ls.sort()
            self.resp_merch_switch_params = ls
        except KeyError:
            self.resp_merch_switch = loads(r.text)

    def merchant_list(self, first, count):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.list', 'params': {'first': first, 'count': count},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_merch_list = loads(r.text)['result']
        except KeyError:
            self.resp_merch_list = loads(r.text)


    def merchant_get(self, m_lid, balance):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.get', 'params': {'m_lid': m_lid, 'balance': balance},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text, self.headers)
        try:
            self.resp_merch_get = loads(r.text)['result']
        except KeyError:
            self.resp_merch_get = loads(r.text)

    def merchant_get_key(self, m_lid):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.get_key', 'params': {'m_lid': m_lid},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print('\n', r.text)
        if 'result' in loads(r.text):
            self.resp_merch_get_key = loads(r.text)['result']
        else:
            try:
                if type(loads(r.text)['error']['data']) == dict:
                    self.get_key_2step = loads(r.text)['error']['data']['key']
                    self.resp_merch_get_key = loads(r.text)
                else:
                    self.resp_merch_get_key = loads(r.text)
            except KeyError:
                    self.resp_merch_get_key = loads(r.text)


    def merchant_renew_key(self, m_lid):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.renew_key', 'params': {'m_lid': m_lid},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        if 'result' in loads(r.text):
            self.resp_merch_renew_key = loads(r.text)['result']
        else:
            try:
                if type(loads(r.text)['error']['data']) == dict:
                    self.renew_key_2step = loads(r.text)['error']['data']['key']
                    self.resp_merch_renew_key = loads(r.text)
                else:
                    self.resp_merch_renew_key = loads(r.text)
            except KeyError:
                self.resp_merch_renew_key = loads(r.text)


    def merchant_update(self, m_lid, title, params, payment_expiry, rotate_addr, apiip):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.update',
                                'params': {'m_lid': m_lid, 'title': title, 'params': params,
                                           'payment_expiry': payment_expiry, 'rotate_addr': rotate_addr, 'apiip': apiip},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_merch_update = loads(r.text)['result']
        except KeyError:
            self.resp_merch_update = loads(r.text)

    def pwmerchactive_public_list(self):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'pwmerchactive.public_list', 'params': {},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        self.resp_merch_public_list = loads(r.text)['result']

    def pwmerchactive_list(self, m_lid, curr, is_out):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'pwmerchactive.list',
                                'params': {'m_lid': m_lid, 'curr': curr, 'is_out': is_out},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_pwmerchactive_list = loads(r.text)['result']
        except KeyError:
            self.resp_pwmerchactive_list = loads(r.text)

    def pwmerchactive_update(self, m_lid, is_active, payway_name):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'pwmerchactive.update',
                                'params': {'m_lid': m_lid, 'is_active': is_active, 'payway_name': payway_name},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_pwmerchactive_update = loads(r.text)['result']
        except KeyError:
            self.resp_pwmerchactive_update = loads(r.text)

    def bookmark_create(self, m_lid, title, params, order):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.insert',
                                'params': {'m_lid': m_lid, 'title': title, 'params': params, 'order': order},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.bookmark_oid = loads(r.text)['result']['id']
            self.resp_bookmark_create = loads(r.text)['result']
        except KeyError:
            self.resp_bookmark_create = loads(r.text)

    def bookmark_list(self, m_lid, first, count):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.list',
                                'params': {'m_lid': m_lid, 'first': first, 'count': count},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        self.resp_bookmark_list = loads(r.text)['result']

    def bookmark_update(self, m_lid, oid, order, title):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.update',
                                'params': {'m_lid': m_lid, 'oid': oid, 'order': order, 'title': title},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_bookmark_update = loads(r.text)['result']
        except KeyError:
            self.resp_bookmark_update = loads(r.text)


    def bookmark_delete(self, m_lid, oid):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.delete',
                                'params': {'m_lid': m_lid, 'oid': oid},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_bookmark_delete = loads(r.text)['result']
        except KeyError:
            self.resp_bookmark_delete = loads(r.text)

    def delegate(self, params):
        data = {'method': 'merchant.delegate', 'params': params, 'jsonrpc': 2.0, 'id': self.ex_id()}
        r = requests.post(url=self.wapi_url, json=data, headers=self.headers, verify=False)
        # print('\n', r.text)
        try:
            self.resp_delegate = loads(r.text)['result']
        except KeyError:
            self.resp_delegate = loads(r.text)['error']


if __name__ == '__main__':
    admin1 = Admin(token='_RmwXc_7QNNxBbOMwQLAZ3xu7UlR8iHuT0cSehrPDcA4QFeRfY2S2vmhGE3B9ePGpw0q')
    user1 = User()
    user1.authorization_by_email(email='testjcash@gmail.com', pwd='aA/123')
    user1.logout()
    # user1.forgot('testjcash@gmail.com')
    # user1.confirm_registration(key=user1.forgot_key, code=admin1.get_onetime_code(email='testjcash@gmail.com'))
    # user1.update_pwd('aA/123')
    # print(user1.resp_authorization)
