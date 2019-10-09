import requests
import random
import time
import pprint
from users.merchant import Merchant
from json import loads
from string import ascii_uppercase


requests.packages.urllib3.disable_warnings()


class User:

    wapi_url = 'https://anymoney.e-cash.pro/_handler/wapi/'
    eapi_url = 'https://anymoney.e-cash.pro/_handler/eapi/'
    json_rpc = '2.0'

    confirm_key = ''
    headers = {'x-token': ''}
    id = ''
    resp_registration = {}
    resp_confirm = {}

    def __init__(self, user=None, pwd=None, admin=None):
        if user:
            self.email = user['email']
            self.pwd = pwd
            self.id = user['id']
            self.headers = {'x-token': ''}
            common_merchants = list(admin.get_merchants(owner_id=self.id))
            i = iter(reversed(range(1, len(common_merchants) + 1)))
            for merchant in common_merchants:
                self.__dict__['merchant' + str(next(i))] = Merchant(merchant)
            pw_merchants = list(admin.get_merchants(owner_id=self.id, pw='!='))
            adm_pwid = {v: k for k, v in admin.payway_id.items()}
            for merchant in pw_merchants:
                self.__dict__['pwmerchant_' + adm_pwid[merchant['payway_id']].upper()] = Merchant(merchant)

    @staticmethod
    def ex_id():
        return str(random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000)))

    @staticmethod
    def registration(email, pwd):
        r = requests.post(url=User.wapi_url,
                          json={'method': 'account.register',
                                'params': {'email': email, 'pwd': pwd}, 'jsonrpc': User.json_rpc, 'id': User.ex_id()},
                          verify=False)
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
                                    'jsonrpc': User.json_rpc, 'id': User.ex_id()},
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
                                    'jsonrpc': User.json_rpc, 'id': User.ex_id()},
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
                      json={'method': 'account.auth2cancel', 'params': {'key': str(key)}, 'jsonrpc': User.json_rpc, 'id': User.ex_id()},
                      verify=False)

    def second_confirm(self, key, code):
        r = requests.post(url=User.wapi_url,
                          json={'method': 'account.auth2confirm', 'params': {'key': str(key), 'code': str(code)},
                                'jsonrpc': self.json_rpc, 'id': User.ex_id()},
                          verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
            self.resp_second_confirm = loads(r.text)['result']
        except KeyError:
            self.resp_second_confirm = loads(r.text)

    def authorization_by_email(self, email, pwd):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.login',
                                'params': {'email': email, 'pwd': pwd}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          verify=False)
        print(r.text)
        if 'result' in loads(r.text):
            try:
                self.headers['x-token'] = loads(r.text)['result']['session']['token']
                self.resp_authorization = loads(r.text)['result']
            except KeyError:
                self.resp_authorization = loads(r.text)
        else:
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
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.logout', 'params': {}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        time.sleep(3)
        print(r.text)

    def renew_session(self):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.renew', 'params': {}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['token']
            self.resp_renew = loads(r.text)['result']
        except KeyError:
            self.resp_renew = loads(r.text)

    def set_2type(self, tp=None):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.set_auth2type', 'params': {'tp': tp}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
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
                          json={'method': 'account.forgot', 'params': {'email': email}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          verify=False)
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
                                'params': {'email': email}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
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
                                'params': {'pwd': pwd}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
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
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
        except KeyError:
            self.resp_update_tz = loads(r.text)['error']

    def update_lang(self, lang):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_lang', 'params': {'lang': lang},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
        except KeyError:
            self.resp_update_lang = loads(r.text)

    def update_safemode(self, safemode):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'account.update_safemode', 'params': {'safemode': safemode},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.headers['x-token'] = loads(r.text)['result']['session']['token']
            self.resp_update_safemode = loads(r.text)['result']
        except KeyError:
            self.resp_update_safemode = loads(r.text)

    def currency_list(self, first, count):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'currency.list', 'params': {'first': first, 'count': count},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        self.resp_currency_list = loads(r.text)['result']

    def payway_list(self, tp):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'payway.list', 'params': {'tp': tp}, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        print(r.text)
        try:
            self.resp_payway_list = loads(r.text)['result']
        except KeyError:
            self.resp_payway_list = loads(r.text)

    def merchant(self, method, params):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'merchant.' + method, 'params': params, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_merchant = loads(r.text)['result']
        except KeyError:
            if 'key' in loads(r.text)['error']['data']:
                self.merch_2step = loads(r.text)['error']['data']['key']
                self.resp_merchant = loads(r.text)['error']
            else:
                self.resp_merchant = loads(r.text)['error']

    def pwmerchactive(self, method, params):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'pwmerchactive.' + method, 'params': params, 'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        pprint.pprint(loads(r.text))
        try:
            self.resp_pwmerchactive = loads(r.text)['result']
        except KeyError:
            self.resp_pwmerchactive = loads(r.text)['error']

    def bookmark_create(self, m_lid, title, params, order):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.insert',
                                'params': {'m_lid': m_lid, 'title': title, 'params': params, 'order': order},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
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
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        self.resp_bookmark_list = loads(r.text)['result']

    def bookmark_update(self, m_lid, oid, order, title):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.update',
                                'params': {'m_lid': m_lid, 'oid': oid, 'order': order, 'title': title},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_bookmark_update = loads(r.text)['result']
        except KeyError:
            self.resp_bookmark_update = loads(r.text)


    def bookmark_delete(self, m_lid, oid):
        r = requests.post(url=self.wapi_url,
                          json={'method': 'bookmark.delete',
                                'params': {'m_lid': m_lid, 'oid': oid},
                                'jsonrpc': self.json_rpc, 'id': self.ex_id()},
                          headers=self.headers, verify=False)
        try:
            self.resp_bookmark_delete = loads(r.text)['result']
        except KeyError:
            self.resp_bookmark_delete = loads(r.text)

    def delegate(self, params):
        data = {'method': 'merchant.delegate', 'params': params, 'jsonrpc': self.json_rpc, 'id': self.ex_id()}
        r = requests.post(url=self.wapi_url, json=data, headers=self.headers, verify=False)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_delegate = loads(r.text)['result']
        except KeyError:
            self.resp_delegate = loads(r.text)['error']


if __name__ == '__main__':
    user1 = User()
    user1.authorization_by_email(email='anymoneyuser1@mailinator.com', pwd='123456')
    user1.pwmerchactive(method='list', params={'m_lid': '37', 'curr': 'UAH', 'is_out': None})


