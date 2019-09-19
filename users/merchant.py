import requests
import time
import random
from users import sign
from json import loads
from string import ascii_uppercase
import pprint


class Merchant:

    japi_url = 'https://anymoney.e-cash.pro/_handler/japi/'
    wapi_url = 'https://anymoney.e-cash.pro/_handler/wapi/'

    def __init__(self, merchant=None):
        self.id = merchant['id']
        self.lid = str(merchant['lid'])
        self.akey = merchant['apikey']

    @staticmethod
    def time_sent():
        return str(int(time.time() * 1000))

    @staticmethod
    def _id():
        return random.choice(list(ascii_uppercase)) + str(random.randint(0, 100000))

    def headers(self, data, time_sent):
        return {'x-merchant': self.lid,
                'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                'x-utc-now-ms': time_sent}

    def balance(self, curr=None):
        time.sleep(2)
        self.req_id = self._id()
        data = {'method': 'merchant.balance', 'params': {'curr': curr}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data,
                          headers={'x-merchant': str(self.lid),
                                   'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        try:
            self.resp_balance = loads(r.text)['result']
            if curr == None:
                return loads(r.text)['result']
            else:
                return loads(r.text)['result'][curr]
        except KeyError:
            self.resp_balance = loads(r.text)
            return loads(r.text)

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

    def out_currency(self, in_curr):
        self.req_id = self._id()
        data = {'method': 'adress.out_currencies', 'params': {'in_curr': in_curr}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        self.resp_adress_get = loads(r.text)

    def address_create(self, params):
        self.req_id = self._id()
        data = {'method': 'address.create', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_address_create = loads(r.text)['result']
        except KeyError:
            self.resp_address_create = loads(r.text)['error']

    def address_list(self, params):
        self.req_id = self._id()
        data = {'method': 'address.list', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print(r.text)
        try:
            self.resp_address_list = loads(r.text)['result']
        except KeyError:
            self.resp_address_list = loads(r.text)['error']

    def address_get(self, params):
        self.req_id = self._id()
        data = {'method': 'address.get', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print(r.text)
        try:
            self.resp_address_get = loads(r.text)['result']
        except KeyError:
            self.resp_address_get = loads(r.text)['error']

    def address_edit(self, params):
        self.req_id = self._id()
        data = {'method': 'address.edit', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_address_edit = loads(r.text)['result']
        except KeyError:
            self.resp_address_edit = loads(r.text)['error']

    def address_out_currencies(self, params):
        self.req_id = self._id()
        data = {'method': 'address.out_currencies', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_address_out_currencies = loads(r.text)['result']
        except KeyError:
            self.resp_address_out_currencies = loads(r.text)['error']

    def address_history(self, params):
        self.req_id = self._id()
        data = {'method': 'address.address_history',  'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_address_history = loads(r.text)['result']
        except KeyError:
            self.resp_address_history = loads(r.text)['error']

    def address_currencies(self, params):
        self.req_id = self._id()
        data = {'method': 'address.currencies', 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_address_currencies = loads(r.text)['result']
        except KeyError:
            self.resp_address_currencies = loads(r.text)['error']

    def convert(self, method, params):
        self.req_id = self._id()
        data = {'method': 'convert.' + method, 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print(r.text)
        try:
            self.resp_convert = loads(r.text)['result']
        except KeyError:
            self.resp_convert = loads(r.text)['error']

    def convert_create(self, in_curr, out_curr, in_amount, out_amount):
        self.req_id = self._id()
        data = {'method': 'convert.create',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'in_amount': in_amount, 'out_amount': out_amount,
                           'externalid': self.req_id},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_convert_create = loads(r.text)['result']
        except KeyError:
            self.resp_convert_create = loads(r.text)['error']

    def convert_get(self, o_lid):
        self.req_id = self._id()
        data = {'method': 'convert.get',
                'params': {'o_lid': o_lid},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        return loads(r.text)

    def convert_params(self, in_curr, out_curr):
        self.req_id = self._id()
        data = {'method': 'convert.params',
                'params': {'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_convert_params = loads(r.text)['result']
        except KeyError:
            self.resp_convert_params = loads(r.text)['error']

    def convert_calc(self, in_amount, out_amount, in_curr, out_curr, validate_balance=True):
        self.req_id = self._id()
        data = {'method': 'convert.calc',
                'params': {'in_amount': in_amount, 'out_amount': out_amount,
                           'in_curr': in_curr, 'out_curr': out_curr, 'validate_balance': validate_balance},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_convert_calc = loads(r.text)['result']
        except KeyError:
            self.resp_convert_calc = loads(r.text)['error']

    def payin(self, method, params):
        self.req_id = self._id()
        data = {'method': 'payin.' + method, 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print(r.text)
        try:
            self.resp_payin = loads(r.text)['result']
        except KeyError:
            self.resp_payin = loads(r.text)['error']


    def payin_calc(self, payway, amount, in_curr, out_curr):
        self.req_id = self._id()
        data = {'method': 'payin.calc',
                'params': {'payway': payway, 'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self._id()}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_payin_calc = loads(r.text)['result']
        except KeyError:
            self.resp_payin_calc = loads(r.text)['error']

    def payin_create(self, payway, amount, in_curr, out_curr=None, payee=None, contact=None, region=None, payer=None):
        self.req_id = self._id()
        data = {'method': 'payin.create',
                'params': {'payway': payway, 'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr,
                           'externalid': self.req_id, 'payee': payee, 'contact': contact, 'region': region, 'payer': payer},
                'jsonrpc': 2.0, 'id': self._id()}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_payin_create = loads(r.text)['result']
            self.payin_lid = loads(r.text)['result']['lid']
        except KeyError:
            self.resp_payin_create = loads(r.text)['error']

    def payin_get(self, o_lid):
        self.req_id = self._id()
        data = {'method': 'payin.get',
                'params': {'o_lid': o_lid},
                'jsonrpc': 2.0, 'id': self._id()}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_payin_get = loads(r.text)['result']
        except KeyError:
            self.resp_payin_get = loads(r.text)['error']

    def payin_params(self, payway, in_curr, out_curr=None):
        self.req_id = self._id()
        data = {'method': 'payin.params',
                'params': {'payway': payway, 'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_payin_params = loads(r.text)['result']
        except KeyError:
            self.resp_payin_params = loads(r.text)['error']

    def payin_list(self, in_curr, out_curr, payway, first, count):
        self.req_id = self._id()
        data = {'method': 'payin.list',
                'params': {'payway': payway, 'in_curr': in_curr, 'out_curr': out_curr, 'first': first, 'count': count},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_payin_list = loads(r.text)['result']
        except KeyError:
            self.resp_payin_list = loads(r.text)['error']

    def cheque_verify(self, cheque):
        self.req_id = self._id()
        data = {'method': 'payin.cheque_verify',
                'params': {'cheque': cheque},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        print('\n', r.text)
        try:
            self.resp_cheque_verify = loads(r.text)['result']
        except KeyError:
            self.resp_cheque_verify = loads(r.text)['error']

    def sci_pay(self, method, params):
        self.req_id = self._id()
        data = {'method': 'sci_pay.' + method, 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_sci_pay = loads(r.text)['result']
            self.sci_pay_lid = loads(r.text).get('result', {}).get('lid')
            self.sci_pay_token = loads(r.text).get('result', {}).get('token')
        except KeyError:
            self.resp_sci_pay = loads(r.text)['error']

    def sci_subpay(self, method, params):
        self.req_id = self._id()
        data = {'method': 'sci_subpay.' + method, 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_sci_subpay = loads(r.text)['result']
            self.sci_subpay_lid = loads(r.text).get('result', {}).get('lid')
            self.sci_subpay_token = loads(r.text).get('result', {}).get('token')
        except KeyError:
            self.resp_sci_subpay = loads(r.text)['error']

    def sci_refund(self, method, params):
        self.req_id = self._id()
        data = {'method': 'sci_refund.' + method, 'params': params, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_sci_refund = loads(r.text)['result']
        except KeyError:
            self.resp_sci_refund = loads(r.text)['error']


    def transfer_create(self, amount, out_curr, tgt, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'transfer.create',
                'params': {'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr, 'tgt': str(tgt),
                           'externalid': self.req_id},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
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

    def transfer_get(self, o_lid):
        self.req_id = self._id()
        data = {'method': 'transfer.get',
                'params': {'o_lid': str(o_lid)},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            self.resp_transfer_get = loads(r.text)['result']
        except KeyError:
            self.resp_transfer_get = loads(r.text)['error']

    def transfer_calc(self, amount, out_curr, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'transfer.calc',
                'params': {'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        # print('out_curr', out_curr)
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_transfer_calc = loads(r.text)['result']
        except KeyError:
            self.resp_transfer_calc = loads(r.text)['error']

    def transfer_list(self, in_curr=None, out_curr=None, first=None, count=None):
        self.req_id = self._id()
        data = {'method': 'transfer.list',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'first': first, 'count': count},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # pprint.pprint(loads(r.text))
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)['error']

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

    def ibill_history(self, begin=None, end=None, curr=None, first='0', count='20', ord_by=None, ord_dir=False,
                      lid=None, filter_amount=None, filter_fee=None, group=None):
        self.req_id = self._id()
        data = {'method': 'merchant.ibill_history',
                'params': {'begin': begin, 'end': end, 'curr': curr, 'lid': lid, 'filter_amount':filter_amount, 'filter_fee':filter_fee,
                           'group': group, 'first': first, 'count': count, 'ord_by': ord_by, 'ord_dir': ord_dir},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)

    def inpay_history(self, begin=None, end=None, curr=None, first='0', count='20', payway=None, status=None,
                      ord_by=None, ord_dir=False, uaccount=None):
        self.req_id = self._id()
        data = {'method': 'merchant.inpay_history',
                'params': {'begin': begin, 'end': end, 'in_curr': curr, 'payway': payway, 'status': status,
                           'first': first, 'count': count, 'ord_by': ord_by, 'ord_dir': ord_dir, 'uaccount': uaccount},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)

    def outpay_history(self, begin=None, end=None, curr=None, first='0', count='20', payway=None, status=None,
                      ord_by=None, ord_dir=False, uaccount=None):
        self.req_id = self._id()
        data = {'method': 'merchant.outpay_history',
                'params': {'begin': begin, 'end': end, 'out_curr': curr, 'payway': payway, 'status': status,
                           'first': first, 'count': count, 'ord_by': ord_by, 'ord_dir': ord_dir, 'uaccount': uaccount},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)

    def convert_history(self, begin=None, end=None, in_curr=None, out_curr=None, first='0', count='20', status=None,
                      ord_by=None, ord_dir=False):
        self.req_id = self._id()
        data = {'method': 'merchant.convert_history',
                'params': {'begin': begin, 'end': end, 'in_curr': in_curr, 'out_curr': out_curr, 'status': status,
                           'first': first, 'count': count, 'ord_by': ord_by, 'ord_dir': ord_dir},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)

    def payout_in_curr_list(self, payway, out_curr):
        self.req_id = self._id()
        data = {'method': 'payout.in_curr_list',
                'params': {'out_curr': out_curr, 'payway': payway},
                'jsonrpc': 2.0, 'id': self.req_id}
        # print('data', data)
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # print('r.text', r.text)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_payout_in_curr_list = loads(r.text)['result']
        except KeyError:
            self.resp_payout_in_curr_list = loads(r.text)

    def payout_get_cheque(self, lid):
        self.req_id = self._id()
        data = {'method': 'payout.get_cheque',
                'params': {'lid': str(lid)},
                'jsonrpc': 2.0, 'id': self.req_id}
        # print('data', data)
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # print('r.text', r.text)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_payout_get_cheque = loads(r.text)['result']
        except KeyError:
            self.resp_payout_get_cheque = loads(r.text)['error']


    def payout_get(self, o_lid):
        self.req_id = self._id()
        data = {'method': 'payout.get',
                'params': {'o_lid': str(o_lid)},
                'jsonrpc': 2.0, 'id': self.req_id}
        # print('data', data)
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # print('r.text', r.text)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_payout_get = loads(r.text)['result']
        except KeyError:
            self.resp_payout_get = loads(r.text)['error']


    def payout_list(self, in_curr=None, out_curr=None, payway=None, first=None, count=None):
        self.req_id = self._id()
        data = {'method': 'payout.list',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'payway': payway, 'first': first, 'count': count},
                'jsonrpc': 2.0, 'id': self.req_id}
        # print('data', data)
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # print('r.text', r.text)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_payout_list = loads(r.text)['result']
        except KeyError:
            self.resp_payout_list = loads(r.text)['error']

    def payout_calc(self, payway, amount, out_curr, in_curr=None):
        self.req_id = self._id()
        data = {'method': 'payout.calc',
                'params': {'amount': amount, 'in_curr': in_curr, 'out_curr': out_curr, 'payway': payway},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        # print('out_curr', out_curr)
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        # pprint.pprint(loads(r.text))
        try:
            self.resp_payout_calc = loads(r.text)['result']
        except KeyError:
            self.resp_payout_calc = loads(r.text)['error']


    def currency_list(self):
        self.req_id = self._id()
        data = {'method': 'merchant.currency_list', 'params': {}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data,
                          headers={'x-merchant': str(self.lid),
                                   'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        # pprint.pprint(loads(r.text))
        self.resp_currency_list = loads(r.text)
        return loads(r.text)


    def exchange_list(self):
        self.req_id = self._id()
        data = {'method': 'merchant.exchange_list', 'params': {}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data,
                          headers={'x-merchant': str(self.lid),
                                   'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        # pprint.pprint(loads(r.text))
        self.resp_exchange_list = loads(r.text)
        return loads(r.text)


    def payway_list(self):
        self.req_id = self._id()
        data = {'method': 'merchant.payway_list', 'params': {}, 'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data,
                          headers={'x-merchant': str(self.lid),
                                   'x-signature': sign.create_sign(self.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent},
                          verify=False)
        # pprint.pprint(loads(r.text))
        self.resp_payway_list = loads(r.text)
        return loads(r.text)

    def convert_list(self, in_curr=None, out_curr=None, first=None, count=None):
        self.req_id = self._id()
        data = {'method': 'convert.list',
                'params': {'in_curr': in_curr, 'out_curr': out_curr, 'first': first, 'count': count},
                'jsonrpc': 2.0, 'id': self.req_id}
        time_sent = self.time_sent()
        r = requests.post(url=self.japi_url, json=data, headers=self.headers(data, time_sent), verify=False)
        try:
            return loads(r.text)['result']
        except KeyError:
            return loads(r.text)
