import requests
import time
from users.tools import getting_email_code
from json import loads
import random
from string import ascii_uppercase



requests.packages.urllib3.disable_warnings()


class Admin:

    user_url = 'https://anymoney-back-p3.e-cash.pro/_handler/wapi/'
    admin_url = 'https://amadm.e-cash.pro/_handler/api'

    def __init__(self, email=None, pwd=None, token=None):
        if not token:
            self.headers = self.autorization(email, pwd)
        else:
            print('In else')
            self.headers = {'x-token': token}
        self.currency = self._curr_id()
        self.payway = self.get_payways()
        self.lang_id = self._lang_id()
        self.front_params = self.get_front_params()

    @staticmethod
    def ex_id():
        return random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000))

    def _curr_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'currency', 'method': 'select', 'selector': {}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return {curr[numb.index('name')]: curr[numb.index('id')] for curr in loads(response.text)[0]['data']}

    def _payway_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'payway', 'method': 'select', 'selector': {}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return {pw[numb.index('name')]: pw[numb.index('id')] for pw in loads(response.text)[0]['data']}

    def _lang_id(self):
        response = requests.post(url=self.admin_url, json={'model': 'lang', 'method': 'select', 'selector': {}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return {ln[numb.index('name')]: ln[numb.index('id')] for ln in loads(response.text)[0]['data']}

    def autorization(self, email, pwd):
        r = requests.post(url=self.admin_url,
                          json={'model': 'auth', 'method': 'login',
                                'data': {'email': email, 'pwd': pwd},
                                'selector': {}}, verify=False)
        r = requests.post(url=self.admin_url,
                          json={'model': 'auth', 'method': 'auth2confirm',
                                'data': {'code': str(getting_email_code()), 'key': str(loads(r.text)['statusData']['data']['key'])},
                                'selector': {}},
                          verify=False)
        fields = loads(r.content)[1]['fields']
        data = loads(r.content)[1]['data'][0]
        admin_session = dict(zip(fields, data))
        return {'x-token': admin_session['token']}

    def set_st(self, name, data):
        requests.post(url=self.admin_url, json={'model': 'st', 'method': 'update', 'data': data, 'selector': {'name': ['eq', name]}},
                      headers=self.headers, verify=False)

    def get_user(self, email):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'user', 'method': 'select',
                                       'selector': {'email': ['in', [email]]}},
                                 headers=self.headers, verify=False)
        print(response.text)
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
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        try:
            return loads(response.text)[0]['data'][0][numb.index('token')]
        except IndexError:
            return {'exception': "Session wasn't found"}

    def delete_sessions(self, email):
        requests.post(url=self.admin_url,
                      json={'model': 'session', 'method': 'delete',
                            'selector': {'owner_id': ['parent_in', {'email': ["like", '%' + email + '%']}]}},
                      headers=self.headers, verify=False)

    def delete_auth2type_token(self, email):
        requests.post(url=self.admin_url,
                      json={'model': 'twostepauth', 'method': 'delete',
                            'selector': {'owner_id': ['parent_in', {'email': ['like', '%' + email + '%']}]}},
                      headers=self.headers, verify=False)

    def set_merchant(self, lid, is_active=True, is_customfee=False, payout_allowed=True):
        requests.post(url=self.admin_url,
                      json={'model': 'merchant', 'method': 'update',
                            'data': {'is_active': is_active, 'is_customfee': is_customfee,
                                     'payout_allowed': payout_allowed},
                            'selector': {'lid': ['in', [lid]]}},
                      headers=self.headers, verify=False)

    def set_wallet_amount(self, balance, currency, merch_lid):
        requests.post(url=self.admin_url,
                      json={'model': 'wallet', 'method': 'update', 'data': {'balance': balance},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'merchant_id': ['eq', self.get_merchant(merch_lid)['id']]}},
                      headers=self.headers, verify=False)

    def get_wallet_amount(self, currency, merch_lid):
        response = requests.post(url=self.admin_url,
                      json={'model': 'wallet', 'method': 'select',
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'merchant_id': ['eq', self.get_merchant(merch_lid)['id']]}},
                      headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return loads(response.text)[0]['data'][0][numb.index('balance')]

    def delete_user(self, email):
        requests.post(url=self.admin_url, json={'model': 'user', 'method': 'delete',
                                                'selector': {'email': ['eq', email]}},
                      headers=self.headers, verify=False)

    def delete_merchant(self, lid):
        requests.post(url=self.admin_url, json={'model': 'merchant', 'method': 'delete',
                                                'selector': {'lid': ['eq', lid]}},
                      headers=self.headers, verify=False)

    def set_pwcurrency(self, payway, is_out, currency, is_active, tech_min, tech_max):
        requests.post(url=self.admin_url,
                      json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'payway_id': ['eq', self.payway[payway]], 'is_out': ['=', is_out]}},
                      headers=self.headers, verify=False)


    def set_pwcurrency_min_max(self, payway, is_out, currency, is_active, tech_min, tech_max):
        r = requests.post(url=self.admin_url,
                          json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['=', self.currency[currency]],
                                         'payway_id': ['=', payway], 'is_out': ['=', is_out]}},
                          headers=self.headers, verify=False)

    def set_pwc(self, pw_id, is_out, currency, is_active, tech_min, tech_max):
        requests.post(url=self.admin_url,
                      json={'model': 'pwcurrency', 'method': 'update',
                            'data': {'tech_min': tech_min, 'tech_max': tech_max, 'is_active': is_active},
                            'selector': {'currency_id': ['eq', self.currency[currency]],
                                         'payway_id': ['eq', pw_id], 'is_out': ['=', is_out]}},
                      headers=self.headers, verify=False)

    def get_onetime_code(self, email):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'twostepauth', 'method': 'select',
                                       'selector': {'owner_id': ['parent_in', {'email': ['=', email]}]}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return loads(response.text)[0]['data'][0][numb.index('code')]

    def set_currency(self, is_crypto, admin_min, admin_max):
        requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'admin_min': admin_min, 'admin_max': admin_max},
                            'selector': {'is_crypto': ['=', is_crypto]}},
                      headers=self.headers, verify=False)

    def set_currency_precision(self, is_crypto, admin_min, admin_max, precision):
        r = requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'admin_min': admin_min, 'admin_max': admin_max, 'precision': precision},
                            'selector': {'is_crypto': ['=', is_crypto]}},
                      headers=self.headers, verify=False)

    def set_currency_activity(self, name, is_disabled=False, is_active=True):
        requests.post(url=self.admin_url,
                      json={'model': 'currency', 'method': 'update',
                            'data': {'is_disabled': is_disabled, 'is_active': is_active},
                            'selector': {'name': ['eq', name]}},
                      headers=self.headers, verify=False)

    def set_payways(self, name, is_active=True, is_public=True, is_disabled=False):
        requests.post(url=self.admin_url,
                      json={'model': 'payway', 'method': 'update',
                            'data': {'is_active': is_active, 'is_public': is_public, 'is_disabled': is_disabled},
                            'selector': {'name': ['eq', name]}},
                      headers=self.headers, verify=False)

    def get_payways(self):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'payway', 'method': 'select', 'selector': {}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return {pw[numb.index('name')]: {'is_active': pw[numb.index('is_active')], 'is_public': pw[numb.index('is_public')],
                                         'id': pw[numb.index('id')]} for pw in loads(response.text)[0]['data']}

    def get_exchange(self, _filter=None, value=None):
        r = requests.post(url=self.admin_url,
                          json={'model': 'exchange', 'method': 'select', 'selector': {}},
                          headers=self.headers, verify=False)
        ls = []
        fields = loads(r.text)[0]['fields']
        for i in loads(r.text)[0]['data']:
            dct = dict(zip(fields, i))
            try:
                if dct[_filter] == value:
                    ls.append(dct)
            except KeyError:
                ls.append(dct)
        return ls

    def set_pwmerchactive(self, merch_id, payway_id, is_active):
        r = requests.post(url=self.admin_url,
                          json={'model': 'pwmerchactive', 'method': 'update',
                                'data': {'is_active': is_active},
                                'selector': {'merchant_id': ['in', [merch_id]], 'payway_id': ['in', [payway_id]]}},
                          headers=self.headers, verify=False)

    def get_pwmerchactive(self, is_active, merch_id):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'pwmerchactive', 'method': 'select',
                                       'selector': {'merchant_id': ['in', [merch_id]],
                                                    'is_active': ['eq', is_active]}},
                                 headers=self.headers, verify=False)
        numb = loads(response.text)[0]['fields']
        return [pw[numb.index('payway_id')] for pw in loads(response.text)[0]['data']]

    def get_merchant(self, lid):
        response = requests.post(url=self.admin_url,
                                 json={'model': 'merchant', 'method': 'select',
                                       'selector': {'lid': ['in', [lid]]}},
                                 headers=self.headers, verify=False)
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
                          headers=self.headers, verify=False)
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
                                     'tp': tp, 'currency_id': self.currency[currency], 'payway_id': payway_id,
                                     'merchant_id': merchant_id, 'is_active': is_active}, 'selector': {}},
                      headers=self.headers, verify=False)

    def set_fee(self, mult=0, add=0, _min=0, _max=0, around='ceil', tp=0, currency_id=None, payway_id=None,
                is_active=True, merchant_id=None):
        requests.post(url=self.admin_url,
                      json={'model': 'fee', 'method': 'update',
                            'data': {'fee': {'max': _max, 'add': add, 'm': around, 'mult': mult, 'min': _min},
                                     'is_active': is_active},
                            'selector': {'currency_id': ['=', currency_id], 'payway_id': ['=', payway_id], 'tp': ['=', tp],
                                         'merchant_id': ['=', merchant_id]}},
                      headers=self.headers, verify=False)

    def delete_personal_fee(self, merchant_id):
        requests.post(url=self.admin_url,
                      json={'model': 'fee', 'method': 'delete', 'selector': {'merchant_id': ['eq', merchant_id]}},
                      headers=self.headers, verify=False)

    def create_personal_exchange_fee(self, in_curr, out_curr, merchant_id, fee, is_active):
        requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'insert',
                            'data': {'in_currency_id': in_curr, 'out_currency_id': out_curr,
                                     'merchant_id': merchant_id, 'fee': fee, 'is_active': is_active}, 'selector': {}},
                      headers=self.headers, verify=False)

    def set_personal_exchange_fee(self, fee=0, in_curr=None, out_curr=None, merchant_id=None, is_active=False):
        requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'update',
                            'data': {'is_active': is_active, 'fee': fee},
                            'selector': {'in_currency_id': ['=', in_curr], 'out_currency_id': ['=', out_curr],
                                         'merchant_id': ['eq', merchant_id]}},
                      headers=self.headers, verify=False)

    def delete_personal_exchange_fee(self, merchant_id):
        requests.post(url=self.admin_url,
                      json={'model': 'exchfee', 'method': 'delete',
                            'selector': {'merchant_id': ['eq', merchant_id]}},
                      headers=self.headers, verify=False)

    def set_rate_exchange(self, rate, fee, in_currency, out_currency, tech_min=None, tech_max=None, is_active=True,
                          extfee=0):
        if tech_min is None and tech_max is None:
            requests.post(url=self.admin_url,
                          json={'model': 'exchange', 'method': 'update',
                                'data': {'fee': fee, 'rate': rate, 'is_active': is_active, 'extfee': extfee},
                                'selector': {'in_currency_id': ['eq', self.currency[in_currency]],
                                             'out_currency_id': ['eq', self.currency[out_currency]]}},
                          headers=self.headers, verify=False)
        else:
            requests.post(url=self.admin_url,
                          json={'model': 'exchange', 'method': 'update',
                                'data': {'fee': fee, 'rate': rate, 'tech_min': tech_min, 'tech_max': tech_max,
                                         'is_active': is_active, 'extfee': extfee},
                                'selector': {'in_currency_id': ['eq', self.currency[in_currency]],
                                             'out_currency_id': ['eq', self.currency[out_currency]]}},
                          headers=self.headers, verify=False)

    def set_limit_exchange(self, tech_min, tech_max, in_curr, out_curr):
        requests.post(url=self.admin_url,
                      json={'model': 'exchange', 'method': 'update', 'data': {'tech_min': tech_min, 'tech_max': tech_max},
                            'selector': {'in_currency_id': ['eq', self.currency[in_curr]],
                                         'out_currency_id': ['eq', self.currency[out_curr]]}},
                      headers=self.headers, verify=False)

    def set_order_status(self, lid, status):
        time.sleep(1)
        requests.post(url=self.admin_url,
                      json={'model': 'order', 'method': 'update', 'data': {'status': status},
                            'selector': {'lid': ['in', [lid]]}},
                      headers=self.headers, verify=False)

    def set_st_value(self, name, value=False):
        r = requests.post(url=self.admin_url,
                      json={'model': 'st', 'method': 'update', 'data': {'value': {'value': value}},
                            'key': {'name': name}},
                      headers=self.headers, verify=False)
        self.resp_st_value = r.text

    def get_front_params(self):
        r = requests.post(url=self.admin_url,
                          json={'model': 'domain', 'method': 'select',
                                'key': {'name': 'anymoney-back-p3.e-cash.pro'}},
                          headers=self.headers, verify=False)
        fields = loads(r.text)[0]['fields']
        data = loads(r.text)[0]['data'][0]
        return dict(zip(fields, data))['front_params']

    def set_front_params(self, pass_length_min=6, pass_length_max=50, min_digits_qty=0, min_low_case_char=0,
                         min_spec_char_qty=0, min_upp_case_char=0):
        requests.post(url=self.admin_url,
                      json={'model': 'domain', 'method': 'update',
                            'key': {'name': 'anymoney-back-p3.e-cash.pro'},
                            'data': {'front_params': {'validate': {'pass': {
                                'pass_length_min': pass_length_min, 'pass_length_max': pass_length_max,
                                'min_digits_qty': min_digits_qty, 'min_low_case_char': min_low_case_char,
                                'min_spec_char_qty': min_spec_char_qty, 'min_upp_case_char': min_upp_case_char}}}}},
                      headers=self.headers, verify=False)

    def get_ibill(self, merchant_id, count=20, id=None):
        json = {'model': 'ibill', 'method': 'select', 'rng': [0, count],
                            'key': {'merchant_id': merchant_id}}
        if id: json['key']['id'] = id
        r = requests.post(url=self.admin_url,
                      json= json,
                      headers=self.headers, verify=False)
        fields = loads(r.text)[0]['fields']
        data = loads(r.text)[0]['data']
        ibill_list = {}
        ibill_list['count']=loads(r.text)[0]['count']
        ibill_list['data'] = dict(zip(fields, data))
        if ibill_list['data']:
            return ibill_list
        else:
            return 'No ibills for this query.'

    def get_order(self, selector={}):
        json = {'model': 'order', 'method': 'select', 'rng': [0, 20]}
        if selector:
            json['key'] = selector
        r = requests.post(url=self.admin_url, json=json,
                          headers=self.headers, verify=False)
        order_list = ['count: ' + str(loads(r.text)[0]['count'])]
        fields = loads(r.text)[0]['fields']
        for i in loads(r.text)[0]['data']:
            order_list.append(dict(zip(fields, i)))
        if loads(r.text)[0]['data']:
            return order_list
        else:
            return []

    def get_crypto_adress(self, _filter, value):
        print('In crypto')
        r = requests.post(url=self.admin_url,
                          json={'model': 'address', 'method': 'select', 'selector': {}},
                          headers=self.headers, verify=False)
        ls = []
        fields = loads(r.text)[0]['fields']
        for i in loads(r.text)[0]['data']:
            dct = dict(zip(fields, i))
            try:
                if dct[_filter] == value:
                    ls.append(dct)
            except KeyError:
                ls.append(dct)
        return ls

    def set_crypto_address(self, oid, rotate):
        r = requests.post(url=self.admin_url,
                          json={'model': 'address', 'method': 'update', 'data': {'rotate': rotate},
                                'selector': {'id': ['eq', [oid]]}},
                          headers=self.headers, verify=False)

    def delete_crypto_address(self, _id):
        requests.post(url=self.admin_url,
                      json={'model': 'address', 'method': 'delete', 'selector': {'id': ['in', [_id]]}},
                      headers=self.headers, verify=False)

    def get_currency(self, id):
        for name in self.currency.keys():
            if self.currency[name] == id: break
        return name


if __name__ == '__main__':
    admin = Admin(token='Ja2SN5_wTu51SOVvhsK_WDSB4US9eEe_dEHf_w_3zkr9I_uf0sI_kLyDdkSkEQTtNBt8')
    print(admin.currency)
    # print(admin.get_order({'merchant_id': 703687441778495, 'tp': 0}))


