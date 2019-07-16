import requests
import time
import random
from users import sign
from json import loads
from string import ascii_uppercase
import pprint


class Merchant:

    japi_url = 'https://anymoney-back-p3.e-cash.pro/_handler/japi/'
    wapi_url = 'https://anymoney-back-p3.e-cash.pro/_handler/wapi/'

    def __init__(self, merchant=None):
        self.id = merchant['id']
        self.lid = merchant['lid']
        self.akey = merchant['apikey']

    @staticmethod
    def time_sent():
        return str(int(time.time() * 1000))

    @staticmethod
    def _id():
        return random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000))

    def headers(self, data, time_sent):
        return {'x-merchant': str(self.lid),
                'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                'x-utc-now-ms': time_sent}

    def balance(self, curr):
        time.sleep(2)
        self.req_id = self._id()
        data = {'method': 'merchant.balance', 'params': {'curr': curr}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data,
                          headers={'x-merchant': str(self.lid),
                                   'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        self.resp_balance = loads(r.text)['result']
        return loads(r.text)['result'][curr]


    def order_get(self, o_lid, ibill=False):
        self.req_id = self._id()
        data = {'method': 'merchant.order_get', 'params': {'o_lid': o_lid, 'ibill': ibill}, 'jsonrpc': 2.0,
                'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_order_get = loads(r.text)

    def order_history(self, o_tp, in_curr, out_curr, payway, begin, end, first, count, ord_by, ord_dir, csv):
        self.req_id = self._id()
        data = {'method': 'merchant.order_history',
                'params': {'o_tp': o_tp, 'in_curr': in_curr, 'out_curr': out_curr, 'payway': payway, 'begin': begin,
                           'end': end, 'first': first, 'count': count, 'ord_by': ord_by, 'ord_dir': ord_dir, 'csv': csv},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_order_history = loads(r.text)

    def currency_list(self):
        self.req_id = self._id()
        data = {'method': 'merchant.currency_list', 'params': {}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_currency_list = loads(r.text)

    def payway_list(self):
        self.req_id = self._id()
        data = {'method': 'merchant.payway_list', 'params': {}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_payway_list = loads(r.text)

    def exchange(self, in_curr, out_curr, include_rev):
        self.req_id = self._id()
        data = {'method': 'merchant.exchange',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'include_rev': include_rev},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_exchange = loads(r.text)

    def adress_create(self, in_curr, out_curr, comment):
        self.req_id = self._id()
        data = {'method': 'adress.create', 'params': {'in_curr': in_curr, 'out_curr': out_curr, 'comment': comment},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_adress_create = loads(r.text)

    def adress_list(self, in_curr, out_curr, is_autoconvert, rotate, first, count):
        self.req_id = self._id()
        data = {'method': 'adress.list',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'is_autoconvert': is_autoconvert, 'rotate': rotate,
                           'first': first, 'count': count},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_adress_list = loads(r.text)

    def adress_get(self, oid, name):
        self.req_id = self._id()
        data = {'method': 'adress.get', 'params': {'oid': oid, 'name': name}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_adress_get = loads(r.text)

    def out_currency(self, in_curr):
        self.req_id = self._id()
        data = {'method': 'adress.out_currencies', 'params': {'in_curr': in_curr}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_adress_get = loads(r.text)

    def convert_create(self, in_curr, out_curr, in_amount, out_amount):
        self.req_id = self._id()
        data = {'method': 'convert.create',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'in_amount': in_amount, 'out_amount': out_amount,
                           'externalid': self.req_id},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_convert_create = loads(r.text)['result']
        except KeyError:
            self.resp_convert_create = loads(r.text)['error']

    def convert_params(self, in_curr, out_curr):
        self.req_id = self._id()
        data = {'method': 'convert.params',
                'params': {'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_convert_params = loads(r.text)['result']
        except KeyError:
            self.resp_convert_params = loads(r.text)['error']

    def payin_create(self, payway, amount, in_curr, out_curr, payee, contact, region, payer):
        self.req_id = self._id()
        data = {'method': 'payin.create',
                'params': {'payway': payway, 'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr,
                           'externalid': self.req_id, 'payee': payee, 'contact': contact, 'region': region, 'payer': payer},
                'jsonrpc': 2.0, 'id': self._id()}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_payin_create = loads(r.text)['result']
            self.payin_lid = loads(r.text)['result']['lid']
        except KeyError:
            self.resp_payin_create = loads(r.text)

    def payin_params(self, payway, in_curr, out_curr):
        self.req_id = self._id()
        data = {'method': 'payin.params',
                'params': {'payway': payway, 'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_payin_params = loads(r.text)

    def payout_create(self, payway, amount, in_curr, out_curr, userdata):
        self.req_id = self._id()
        data = {'method': 'payout.create',
                'params': {'payway': payway, 'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr,
                           'userdata': userdata, 'externalid': self._id()},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_payout_create = loads(r.text)

    def payout_params(self, payway, in_curr, out_curr):
        self.req_id = self._id()
        data = {'method': 'payout.params',
                'params': {'payway': payway, 'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_payout_params = loads(r.text)

    def in_curr_list(self, payway, out_curr):
        self.req_id = self._id()
        data = {'method': 'payout.in_curr_list',
                'params': {'payway': payway, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_payout_in_curr_list = loads(r.text)

    def transfer_create(self, amount, out_curr, tgt, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'transfer.create',
                'params': {'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr, 'tgt': str(tgt),
                           'externalid': self.req_id},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # pprint.pprint(loads(r.text))
        self.resp_transfer_create = loads(r.text)

    def transfer_params(self, out_curr, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'transfer.params',
                'params': {'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_transfer_params = loads(r.text)
        try:
            self.resp_transfer_params = loads(r.text)['result']
        except KeyError:
            self.resp_transfer_params = loads(r.text)

    def payout_create(self, payway, amount, out_curr, in_curr=None, payee=None, contact=None, region=None, payer=None):
        self.req_id = self._id()
        data = {'method': 'payout.create',
                'params': {'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr, 'payway': payway,
                           'externalid': self.req_id, 'payee': payee, 'contact': contact,
                           'region': region, 'payer': payer},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        # print('out_curr', out_curr)
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # pprint.pprint(loads(r.text))
        self.resp_payout_create = loads(r.text)

    def payout_params(self, payway, out_curr, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'payout.params',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'payway': payway},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_payout_params = loads(r.text)['result']
        except KeyError:
            self.resp_payout_params = loads(r.text)

