import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint

class TestPaywayList:
    """ PaywayLis """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        admin.set_currency(is_crypto=False, admin_min=bl(0.01), admin_max=bl(3000))
        admin.set_currency(is_crypto=True, admin_min=bl(0.000001), admin_max=bl(3))

    def test_PaywayList_1(self):
        """ Payway List. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdterc20']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['bchabc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_moscow']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc_p2p']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdt']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['nixmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['tinkoff_cs']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['anycash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['alfa_bank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['vtb24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['advcash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['monobank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['sberbank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=True)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=True)
        admin.set_pwcurrency_min_max(payway=admin.payway['kuna']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='UAH',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['visamc']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['payeer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(1), tech_max=bl(100))
        admin.set_pwcurrency_min_max(payway=admin.payway['paymer']['id'], is_out=True, currency='RUB',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_pwcurrency_min_max(payway=admin.payway['btc']['id'], is_out=True, currency='BTC',
                                     is_active=True, tech_min=bl(0.000001), tech_max=bl(3))
        admin.set_pwcurrency_min_max(payway=admin.payway['exmo']['id'], is_out=True, currency='USD',
                                     is_active=True, tech_min=bl(0.01), tech_max=bl(3000))
        admin.set_fee(tp=10, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'],
                      merchant_id=user1.merchant1.id)
        admin.set_fee(tp=10, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(tp=10, currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'],
                      merchant_id=user1.merchant1.id)
        admin.set_fee(tp=10, currency_id=admin.currency['UAH'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(tp=0, currency_id=admin.currency['RUB'], payway_id=admin.payway['visamc']['id'])
        admin.set_fee(mult=bl(0.05), add=bl(2), _min=0, _max=0, tp=0, currency_id=admin.currency['UAH'],
                      payway_id=admin.payway['visamc']['id'])
        user1.merchant1.payway_list()
        # pprint.pprint(user1.merchant1.resp_payway_list)
        assert user1.merchant1.resp_payway_list['result'] == {'btc': {'currencies': [{'fee': {},
                                                  'is_crypto': True,
                                                  'is_out': True,
                                                  'name': 'BTC',
                                                  'precision': 8,
                                                  'tech_max': '3',
                                                  'tech_min': '0.000001'},
                                                 {'fee': {'add': '0.0003',
                                                          'max': '0',
                                                          'method': 'ceil',
                                                          'min': '0',
                                                          'mult': '0.05'},
                                                  'is_crypto': True,
                                                  'is_out': False,
                                                  'name': 'BTC',
                                                  'precision': 8,
                                                  'tech_max': '3000',
                                                  'tech_min': '10'}],
                                  'is_active': True,
                                  'is_public': True,
                                  'type': 'crypto'},
                          'cash_kiev': {'currencies': [],
                                        'is_active': True,
                                        'is_public': True,
                                        'type': 'sci'},
                          'eth': {'currencies': [{'fee': {'add': '0',
                                                          'max': '0',
                                                          'method': 'ceil',
                                                          'min': '0',
                                                          'mult': '0'},
                                                  'is_crypto': True,
                                                  'is_out': False,
                                                  'name': 'ETH',
                                                  'precision': 8,
                                                  'tech_max': '3',
                                                  'tech_min': '0.000001'}],
                                  'is_active': True,
                                  'is_public': True,
                                  'type': 'crypto'},
                          'exmo': {'currencies': [{'fee': {},
                                                   'is_crypto': False,
                                                   'is_out': True,
                                                   'name': 'USD',
                                                   'precision': 2,
                                                   'tech_max': '3000',
                                                   'tech_min': '0.01'},
                                                  {'fee': {'add': '1',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0.05'},
                                                   'is_crypto': False,
                                                   'is_out': False,
                                                   'name': 'USD',
                                                   'precision': 2,
                                                   'tech_max': '2',
                                                   'tech_min': '0.01'},
                                                  {'fee': {'add': '0',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0'},
                                                   'is_crypto': False,
                                                   'is_out': True,
                                                   'name': 'UAH',
                                                   'precision': 2,
                                                   'tech_max': '15.48',
                                                   'tech_min': '0.01'},
                                                  {'fee': {'add': '0',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0'},
                                                   'is_crypto': False,
                                                   'is_out': False,
                                                   'name': 'UAH',
                                                   'precision': 2,
                                                   'tech_max': '3000',
                                                   'tech_min': '0.01'}],
                                   'is_active': True,
                                   'is_public': True,
                                   'type': 'cheque'},
                          'kuna': {'currencies': [{'fee': {'add': '0',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0'},
                                                   'is_crypto': False,
                                                   'is_out': True,
                                                   'name': 'UAH',
                                                   'precision': 2,
                                                   'tech_max': '100',
                                                   'tech_min': '1'},
                                                  {'fee': {'add': '0.33',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0'},
                                                   'is_crypto': False,
                                                   'is_out': False,
                                                   'name': 'UAH',
                                                   'precision': 2,
                                                   'tech_max': '3000',
                                                   'tech_min': '0.01'}],
                                   'is_active': True,
                                   'is_public': True,
                                   'type': 'cheque'},
                          'ltc': {'currencies': [{'fee': {},
                                                  'is_crypto': True,
                                                  'is_out': True,
                                                  'name': 'LTC',
                                                  'precision': 8,
                                                  'tech_max': '0.87627',
                                                  'tech_min': '0.002'},
                                                 {'fee': {'add': '0.001',
                                                          'max': '0',
                                                          'method': 'ceil',
                                                          'min': '0',
                                                          'mult': '0'},
                                                  'is_crypto': True,
                                                  'is_out': False,
                                                  'name': 'LTC',
                                                  'precision': 8,
                                                  'tech_max': '3',
                                                  'tech_min': '0.002'}],
                                  'is_active': True,
                                  'is_public': True,
                                  'type': 'crypto'},
                          'payeer': {'currencies': [{'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'USD',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '0.01'},
                                                    {'fee': {},
                                                     'is_crypto': False,
                                                     'is_out': True,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '100',
                                                     'tech_min': '1'},
                                                    {'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '10'}],
                                     'is_active': True,
                                     'is_public': True,
                                     'type': 'sci'},
                          'paymer': {'currencies': [{'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '0.01'},
                                                    {'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'USD',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '0.01'},
                                                    {'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': True,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '0.01'}],
                                     'is_active': True,
                                     'is_public': True,
                                     'type': 'cheque'},
                          'perfect': {'currencies': [{'fee': {},
                                                      'is_crypto': False,
                                                      'is_out': True,
                                                      'name': 'USD',
                                                      'precision': 2,
                                                      'tech_max': '2.24',
                                                      'tech_min': '0.01'},
                                                     {'fee': {'add': '2',
                                                              'max': '0',
                                                              'method': 'ceil',
                                                              'min': '0',
                                                              'mult': '0.05'},
                                                      'is_crypto': False,
                                                      'is_out': False,
                                                      'name': 'USD',
                                                      'precision': 2,
                                                      'tech_max': '3000',
                                                      'tech_min': '0.01'}],
                                      'is_active': True,
                                      'is_public': True,
                                      'type': 'sci'},
                          'privat24': {'currencies': [{'fee': {'add': '0',
                                                               'max': '0',
                                                               'method': 'ceil',
                                                               'min': '0',
                                                               'mult': '0'},
                                                       'is_crypto': False,
                                                       'is_out': False,
                                                       'name': 'UAH',
                                                       'precision': 2,
                                                       'tech_max': '3000',
                                                       'tech_min': '10'},
                                                      {'fee': {},
                                                       'is_crypto': False,
                                                       'is_out': True,
                                                       'name': 'UAH',
                                                       'precision': 2,
                                                       'tech_max': '93.97',
                                                       'tech_min': '1'}],
                                       'is_active': True,
                                       'is_public': True,
                                       'type': 'sci'},
                          'qiwi': {'currencies': [{'fee': {'add': '0',
                                                           'max': '0',
                                                           'method': 'ceil',
                                                           'min': '0',
                                                           'mult': '0'},
                                                   'is_crypto': False,
                                                   'is_out': False,
                                                   'name': 'RUB',
                                                   'precision': 2,
                                                   'tech_max': '3000',
                                                   'tech_min': '1'}],
                                   'is_active': True,
                                   'is_public': True,
                                   'type': 'sci'},
                          'visamc': {'currencies': [{'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '10'},
                                                    {'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': True,
                                                     'name': 'RUB',
                                                     'precision': 2,
                                                     'tech_max': '100',
                                                     'tech_min': '1'},
                                                    {'fee': {'add': '0',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0'},
                                                     'is_crypto': False,
                                                     'is_out': True,
                                                     'name': 'UAH',
                                                     'precision': 2,
                                                     'tech_max': '100',
                                                     'tech_min': '1'},
                                                    {'fee': {'add': '2',
                                                             'max': '0',
                                                             'method': 'ceil',
                                                             'min': '0',
                                                             'mult': '0.05'},
                                                     'is_crypto': False,
                                                     'is_out': False,
                                                     'name': 'UAH',
                                                     'precision': 2,
                                                     'tech_max': '3000',
                                                     'tech_min': '10'}],
                                     'is_active': True,
                                     'is_public': True,
                                     'type': 'sci'},
                          'webmoney': {'currencies': [],
                                       'is_active': True,
                                       'is_public': True,
                                       'type': 'sci'}}

    def test_PaywayList_2(self, _activate_merchant_payways):
        """ Payway List. """
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdterc20']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['bchabc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_moscow']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc_p2p']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['usdt']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['nixmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['eth']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['tinkoff_cs']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['kuna']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['ltc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['anycash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['qiwi']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['exmo']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['alfa_bank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['webmoney']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['cash_kiev']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['vtb24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['advcash']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['perfect']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['monobank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['sberbank']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['payeer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['privat24']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['paymer']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['visamc']['id'], is_active=False)
        admin.set_pwmerchactive(merch_id=user1.merchant1.id, payway_id=admin.payway['btc']['id'], is_active=False)
        user1.merchant1.payway_list()
        # pprint.pprint(user1.merchant1.resp_payway_list)
        assert user1.merchant1.resp_payway_list['error']['message'] == 'NotFound'
        assert user1.merchant1.resp_payway_list['error']['data']['reason'] == 'No payway available'
