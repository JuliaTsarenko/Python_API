import requests
import time
from users.tools import getting_email_code
from json import loads
import random
from string import ascii_uppercase
import pprint


requests.packages.urllib3.disable_warnings()


class Admin:

    user_url = 'https://anymoney-back-p3.e-cash.pro/_handler/wapi/'
    admin_url = 'https://amadm.e-cash.pro/_handler/api'

    def __init__(self, email=None, pwd=None, token=None):
        if not token:
            self.params = self.autorization(email, pwd)
        else:
            self.params = {'token': token}
        self.currency = self._curr_id()
        self.payway = self.get_payways()
        self.lang_id = self._lang_id()

    @staticmethod
    def ex_id():
        return random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000))

    def _curr_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'currency', 'method': 'select', 'selector': {}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return {curr[numb.index('name')]: curr[numb.index('id')] for curr in loads(response.text)[0]['data']}

    def _payway_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'payway', 'method': 'select', 'selector': {}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return {pw[numb.index('name')]: pw[numb.index('id')] for pw in loads(response.text)[0]['data']}

    def _lang_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'lang', 'method': 'select', 'selector': {}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return {ln[numb.index('name')]: ln[numb.index('id')] for ln in loads(response.text)[0]['data']}

    def autorization(self, email, pwd):
        r = requests.post(url=self.user_url,
                          json={'method': 'account.login',
                                'params': {'email': email, 'pwd': pwd},
                                'jsonrpc': 2.0, 'id': self.ex_id()}, verify=False)
        print(r.text)
        r = requests.post(url=self.user_url,
                          json={'method': 'account.auth2confirm',
                                'params': {'code': getting_email_code(),
                                           'key': loads(r.text)['error']['data']['key']},
                                'jsonrpc': 2.0, 'id': self.ex_id()},
                          verify=False)
        print(r.text)
        return {'token': loads(r.text)['result']['session']['token']}

    def get_user(self, email):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'user', 'method': 'select',
                                       'selector': {'email': ['like', '%' + email + '%']}},
                                 params=self.params, verify=False)
        # pprint.pprint(loads(response.text))
        try:
            fields = loads(response.text)[0]['fields']
            data = loads(response.text)[0]['data'][0]
            return dict(zip(fields, data))
        except IndexError:
            return {'exception': "User wasn't found"}

    def get_session(self, email):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'session', 'method': 'select',
                                       'selector': {'owner_id': ['parent_in', {'email': ['=', email]}]}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        try:
            return loads(response.text)[0]['data'][0][numb.index('token')]
        except IndexError:
            return {'exception': "Session wasn't found"}

    def delete_sessions(self, email):
        requests.post(url=self.admin_url,
                      json={'model': 'session', 'method': 'delete',
                            'selector': {'owner_id': ['parent_in', {'email': ["like", '%' + email + '%']}]}},
                      params=self.params, verify=False)

    def delete_auth2type_token(self, email):
        requests.post(url=self.admin_url,
                      json={'model': 'twostepauth', 'method': 'delete',
                            'selector': {'owner_id': ['parent_in', {'email': ['like', '%' + email + '%']}]}},
                      params=self.params, verify=False)

    def set_merchant(self, lid, is_active=True, is_customfee=False, payout_allowed=True):
        requests.post(url=self.admin_url,
                      json={'model': 'merchant', 'method': 'update',
                            'data': {'is_active': is_active, 'is_customfee': is_customfee,
                                     'payout_allowed': payout_allowed},
                            'selector': {'lid': ['in', [lid]]}},
                      params=self.params, verify=False)

    def set_wallet_amount(self, balance, currency, merch_lid):
        requests.post(url=self.admin_url,
                      json={'model': 'wallet', 'method': 'update', 'data': {'balance': balance},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'merchant_id': ['eq', self.get_merchant(merch_lid)['id']]}},
                      params=self.params, verify=False)

    def get_wallet_amount(self, currency, merch_lid):
        response = requests.post(url=self.admin_url,
                      json={'model': 'wallet', 'method': 'select',
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'merchant_id': ['eq', self.get_merchant(merch_lid)['id']]}},
                      params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return loads(response.text)[0]['data'][0][numb.index('balance')]

    def delete_user(self, email):
        requests.post(url=self.admin_url, json={'model': 'user', 'method': 'delete',
                                                'selector': {'email': ['eq', email]}},
                      params=self.params, verify=False)

    def delete_merchant(self, lid):
        requests.post(url=self.admin_url, json={'model': 'merchant', 'method': 'delete',
                                                'selector': {'lid': ['eq', lid]}},
                      params=self.params, verify=False)

    def set_pwcurrency(self, payway, is_out, currency, is_active, tech_min, tech_max):
        requests.post(url=self.admin_url,
                      json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'payway_id': ['eq', self.payway[payway]], 'is_out': ['=', is_out]}},
                      params=self.params, verify=False)


    def set_pwcurrency_min_max(self, payway, is_out, currency, is_active, tech_min, tech_max):
        r = requests.post(url=self.admin_url,
                          json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['=', self.currency[currency]],
                                         'payway_id': ['=', payway], 'is_out': ['=', is_out]}},
                          params=self.params, verify=False)

    def set_pwc(self, pw_id, is_out, currency, is_active, tech_min, tech_max):
        requests.post(url=self.admin_url,
                      json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'payway_id': ['eq', pw_id], 'is_out': ['=', is_out]}},
                      params=self.params, verify=False)

    def get_onetime_code(self, email):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'twostepauth', 'method': 'select',
                                       'selector': {'owner_id': ['parent_in', {'email': ['=', email]}]}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return loads(response.text)[0]['data'][0][numb.index('code')]

    def set_currency(self, is_crypto, admin_min, admin_max):
        requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'admin_min': admin_min, 'admin_max': admin_max},
                            'selector': {'is_crypto': ['=', is_crypto]}},
                      params=self.params, verify=False)

    def set_currency_precision(self, is_crypto, admin_min, admin_max, precision):
        requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'admin_min': admin_min, 'admin_max': admin_max, 'precision': precision},
                            'selector': {'is_crypto': ['=', is_crypto]}},
                      params=self.params, verify=False)

    def set_currency_activity(self, name, is_disabled=False, is_active=True):
        requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'is_disabled': is_disabled, 'is_active': is_active},
                            'selector': {'name': ['eq', name]}},
                      params=self.params, verify=False)

    def set_payways(self, name, is_active=True, is_public=True, is_disabled=False):
        requests.post(url=self.admin_url,
                      json={'model': 'payway', 'method': 'update',
                            'data': {'is_active': is_active, 'is_public': is_public, 'is_disabled': is_disabled},
                            'selector': {'name': ['eq', name]}},
                      params=self.params, verify=False)

    def get_payways(self):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'payway', 'method': 'select', 'selector': {}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return {pw[numb.index('name')]: {'is_active': pw[numb.index('is_active')], 'is_public': pw[numb.index('is_public')],
                                         'id': pw[numb.index('id')]} for pw in loads(response.text)[0]['data']}

    def set_pwmerchactive(self, merch_id, payway_id, is_active):
        r = requests.post(url=self.admin_url,
                      json={'model': 'pwmerchactive', 'method': 'update',
                            'data': {'is_active': is_active},
                            'selector': {'merchant_id': ['in', [merch_id]], 'payway_id': ['in', [payway_id]]}},
                      params=self.params, verify=False)

    def get_pwmerchactive(self, is_active, merch_id):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'pwmerchactive', 'method': 'select',
                                       'selector': {'merchant_id': ['in', [merch_id]],
                                                    'is_active': ['eq', is_active]}},
                                 params=self.params, verify=False)
        numb = loads(response.text)[0]['fields']
        return [pw[numb.index('payway_id')] for pw in loads(response.text)[0]['data']]

    def get_merchant(self, lid):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'merchant', 'method': 'select',
                                       'selector': {'lid': ['in', [lid]]}},
                                 params=self.params, verify=False)
        try:
            fields = loads(response.text)[0]['fields']
            data = loads(response.text)[0]['data'][0]
            return dict(zip(fields, data))
        except IndexError:
            return {'exception': "Merchant wasn't found"}

    def get_merchants(self, owner_id):
        r = requests.post(url=self.admin_url,
                          json={'model': 'merchant', 'method': 'select',
                                'selector': {'owner_id': ['in', [owner_id]]}},
                          params=self.params, verify=False)
        fields = loads(r.text)[0]['fields']
        data = loads(r.text)[0]['data']
        for data in data:
            yield dict(zip(fields, data))

    def create_personal_fee(self, mult=0, add=0, _min=0, _max=0, around='ceil', tp=0, currency=None, is_active=False,
                            payway_id=None, merchant_id=None):
        requests.post(url=self.admin_url,
                      json={'model': 'fee',
                            'method': 'insert',
                            'data': {'fee': {'max': _max, 'add': add, 'm': around, 'mult': mult, 'min': _min},
                                     'tp': tp, 'currency_id': currency[currency], 'payway_id': payway_id,
                                     'merchant_id': merchant_id, 'is_active': is_active}, 'selector': {}},
                      params=self.params, verify=False)

    def set_fee(self, mult=0, add=0, _min=0, _max=0, around='ceil', tp=0, currency=None, payway=None,
                is_active=True, merchant_id=None):
        r = requests.post(url=self.admin_url,
                      json={'model': 'fee',
                            'method': 'update',
                            'data': {'fee': {'max': _max, 'add': add, 'm': around, 'mult': mult, 'min': _min},
                                     'is_active': is_active},
                            'selector': {'currency_id': ['=', self.currency[currency]],
                                         'payway_id': ['=', payway],
                                         'tp': ['=', tp],
                                         'merchant_id': ['=', merchant_id]}},
                      params=self.params, verify=False)
        # pprint.pprint(r.text)

    def delete_personal_fee(self, merchant_id):
        requests.post(url=self.admin_url,
                      json={'model': 'fee', 'method': 'delete',
                            'selector': {'merchant_id': ['eq', merchant_id]}},
                      params=self.params, verify=False)

    def create_personal_exchange_fee(self, in_curr, out_curr, merchant_id, fee, is_active):
        requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'insert',
                            'data': {'in_currency_id': in_curr,
                                     'out_currency_id': out_curr,
                                     'merchant_id': merchant_id, 'fee': fee, 'is_active': is_active},
                            'selector': {}},
                      params=self.params, verify=False)

    def set_personal_exchange_fee(self, fee=0, in_curr=None, out_curr=None, merchant_id=None, is_active=False):
        r = requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'update',
                            'data': {'is_active': is_active, 'fee': fee},
                            'selector': {'in_currency_id': ['=', in_curr],
                                         'out_currency_id': ['=', out_curr],
                                         'merchant_id': ['eq', merchant_id]}},
                      params=self.params, verify=False)

    def delete_personal_exchange_fee(self, merchant_id):
        requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'delete',
                            'selector': {'merchant_id': ['eq', merchant_id]}},
                      params=self.params, verify=False)

    def set_rate_exchange(self, rate, fee, in_currency, out_currency, tech_min=None, tech_max=None, is_active=True):
        if tech_min is None and tech_max is None:
            requests.post(url=self.admin_url,
                          json={'model': 'exchange', 'method': 'update',
                                'data': {'fee': fee, 'rate': rate, 'is_active': is_active},
                                'selector': {'in_currency_id': ['eq', self.currency[in_currency]],
                                             'out_currency_id': ['eq', self.currency[out_currency]]}},
                          params=self.params, verify=False)
        else:
            r = requests.post(url=self.admin_url,
                          json={'model': 'exchange', 'method': 'update',
                                'data': {'fee': fee, 'rate': rate, 'tech_min': tech_min, 'tech_max': tech_max,
                                         'is_active': is_active},
                                'selector': {'in_currency_id': ['eq', self.currency[in_currency]],
                                             'out_currency_id': ['eq', self.currency[out_currency]]}},
                          params=self.params, verify=False)


    def set_limit_exchange(self, tech_min, tech_max, in_curr, out_curr):
        requests.post(url=self.admin_url,
                      json={'model': 'exchange', 'method': 'update', 'data': {'tech_min': tech_min, 'tech_max': tech_max},
                            'selector': {'in_currency_id': ['eq', self.currency[in_curr]],
                                         'out_currency_id': ['eq', self.currency[out_curr]]}},
                      params=self.params, verify=False)

    def set_order_status(self, lid, status):
        requests.post(url=self.admin_url,
                      json={'model': 'order', 'method': 'update', 'data': {'status': status},
                            'selector': {'lid': ['in', [lid]]}},
                      params=self.params, verify=False)
        time.sleep(1)


    def set_st_value(self, name, value=False):
        r = requests.post(url=self.admin_url,
                      json={'model': 'st', 'method': 'update', 'data': {'value': {'value': value}},
                            'key': {'name': name}},
                      params=self.params, verify=False)
        self.resp_st_value = r.text




if __name__ == '__main__':
    admin = Admin(email='viktor.yahoda@gmail.com', pwd='*Anycash15')
    # admin.create_personal_exchange_fee(in_curr='UAH', out_curr='USD', merchant_id=703687441778420, fee=0, is_active=True)
    # admin.set_fee(tp=10, add=1000000000, currency_id='580542139465839', payway_id='598134325510280', is_active=True, merchant_id='703687441778420')
    #print(len(admin.get_payways()))
    #print(admin.payway)
    # admin.delete_personal_exchange_fee(merchant_id='703687441778420')


