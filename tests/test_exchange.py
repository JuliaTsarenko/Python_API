import requests
import pytest
from json import loads
from users.tools import *
from users.sign import create_sign


@pytest.mark.usefixtures('_personal_exchange_fee')
class TestExchange:
    """ Exchanging currency. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session


    def test_exchange_1(self):
        """ Exchange UAH to USD: baying 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.29),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid,  'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': None, 'out_amount': '0.01'})
        assert user1.resp_delegate['in_amount'] == '0.29'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.01'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']


    def test_exchange_2(self):
        """ Exchange UAH to USD: baying 2.78 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount=None, out_amount='2.78', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '78.4'
        assert user1.merchant1.resp_convert_create['out_amount'] == '2.78'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        '''
        assert user1.merchant1.balance(curr='UAH') == '21.6'
        assert user1.merchant1.balance(curr='USD') == '2.78'
        '''


    def test_exchange_3(self):
        """ Exchange USD to UAH: baying 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.01', in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '28.1999']


    def test_exchange_4(self):
        """ Exchange USD to UAH: baying 33.15 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'UAH',
                               'in_amount': None, 'out_amount': '33.15'})
        assert user1.resp_delegate['in_amount'] == '1.18'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '33.15'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.82'
        assert user1.merchant1.balance(curr='UAH') == '33.15'
        '''


    def test_exchange_5(self):
        """ Exchange USD to UAH: selling 0.01 USD by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.1), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'UAH',
                               'in_amount': '0.01', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '0.28'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '28.1999']


    def test_exchange_6(self):
        """ Exchange USD to UAH: selling 2.15 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(7.55), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH')
        user1.merchant1.convert_create(in_amount='2.15', out_amount=None, in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '2.15'
        assert user1.merchant1.resp_convert_create['out_amount'] == '60.62'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '28.1999']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.85'
        assert user1.merchant1.balance(curr='UAH') == '68.17'
        '''


    def test_exchange_7(self):
        """ Exchange UAH to USD: selling 45.19 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='45.19', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '45.19'
        assert user1.merchant1.resp_convert_create['out_amount'] == '1.6'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.1999', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '4.81'
        assert user1.merchant1.balance(curr='USD') == '1.6'
        '''


    def test_exchange_8(self):
        """ Exchange UAH to USD: selling 0.28 UAH by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': '0.28', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.28'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.1999', '1']

    def test_exchange_9(self):
        """ Exchange UAH to BTC: baying 0.000 01 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.00001', in_curr='UAH', out_curr='BTC')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.18'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.00001'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['rate'] == ['17919.3156', '1']


    def test_exchange_10(self):
        """ Exchange UAH to BTC: baying 0.000 000 01 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.00000001'})
        assert user1.resp_delegate['in_amount'] == '0.01'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '0.00000001'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['rate'] == ['17919.3156', '1']

    def test_exchange_11(self):
        """ Exchange USD to BTC: baying 0.005 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(18), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.0003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'USD', 'out_curr': 'BTC',
                               'in_amount': None, 'out_amount': '0.005'})
        assert user1.resp_delegate['in_amount'] == '17.91'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_amount'] == '0.005'
        assert user1.resp_delegate['out_curr'] == 'BTC'
        assert user1.resp_delegate['rate'] == ['3580.6541', '1']
        '''
        assert user1.merchant1.balance(curr='USD') == '0.09'
        assert user1.merchant1.balance(curr='BTC') == '0.0053'
        '''


    def test_exchange_12(self):
        """ Exchange BTC to USD: baying 0.01 USD by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.003), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.0000001),
                                tech_max=bl(3))
        user1.merchant1.convert_create(in_amount=None, out_amount='0.01', in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.0000028'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3580.6541']


    def test_exchange_13(self):
        """ Exchange UAH to BTC: selling 0.01 UAH by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='UAH', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))
        user1.merchant1.convert_create(in_amount='0.01', out_amount=None, in_curr='UAH', out_curr='BTC')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.01'
        assert user1.merchant1.resp_convert_create['out_amount'] == '0.00000055'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['rate'] == ['17919.3156', '1']


    def test_exchange_14(self):
        """ Exchange BTC to UAH: selling 0.000 000 55 BTC by OWNER without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.01), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(17919.3156), fee=0, in_currency='BTC', out_currency='UAH', tech_min=bl(0.00000055),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'BTC', 'out_curr': 'UAH',
                               'in_amount': '0.00000055', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '0.00000055'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['out_amount'] == '0'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '17919.3156']


    def test_exchange_15(self):
        """ Exchange BTC to USD: selling 0.005 BTC by MERCHANT without fee for exchange. """
        admin.set_wallet_amount(balance=bl(0.5), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD')
        user1.merchant1.convert_create(in_amount='0.005', out_amount=None, in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.005'
        assert user1.merchant1.resp_convert_create['out_amount'] == '17.9'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3580.6541']
        '''
        assert user1.merchant1.balance(curr='BTC') == '0'
        assert user1.merchant1.balance(curr='USD') == '17.9'
        '''


    def test_exchange_16(self):
        """ Exchange UAH to USD: baying 2 USD by OWNER with common fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(80), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(0.1), in_currency='UAH', out_currency='USD')
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'USD',
                               'in_amount': None, 'out_amount': '2'})
        assert user1.resp_delegate['in_amount'] == '56.46'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '2'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['28.2281', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '23.54'
        assert user1.merchant1.balance(curr='USD') == '2'
        '''


    def test_exchange_17(self):
        """ Exchange USD to UAH: selling 2 USD by MERCHANT with common fee 50% for exchange. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(50), in_currency='USD', out_currency='UAH')
        user1.merchant1.convert_create(in_amount='2', out_amount=None, in_curr='USD', out_curr='UAH')
        assert user1.merchant1.resp_convert_create['in_amount'] == '2'
        assert user1.merchant1.resp_convert_create['out_amount'] == '28.19'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '14.09995']
        '''
        assert user1.merchant1.balance(curr='USD') == '0'
        assert user1.merchant1.balance(curr='UAH') == '28.19'
        '''

    def test_exchange_18(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to USD: selling 45.15 UAH by MERCHANT with personal fee 0.1% for exchange. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(2.3), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(0.1))
        user1.merchant1.convert_create(in_amount='45.15', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '45.15'
        assert user1.merchant1.resp_convert_create['out_amount'] == '1.59'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.2281', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '4.85'
        assert user1.merchant1.balance(curr='USD') == '3.89'
        '''

    def test_exchange_19(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to RUB: baying 35 RUB by OWNER with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(14), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(10), currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': None, 'out_amount': '35'})
        assert user1.resp_delegate['in_amount'] == '13.4'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '35'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0.6'
        assert user1.merchant1.balance(curr='USD') == '45'
        '''

    def test_exchange_20(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to USD: baying 2.40 USD by MERCHANT with common fee 3.3% for exchange
            and with personal fee 2.1% for exchange. """
        admin.set_wallet_amount(balance=bl(70), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(0.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.3), in_currency='UAH', out_currency='USD')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2.1))
        user1.merchant1.convert_create(in_amount=None, out_amount='2.40', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '69.11'
        assert user1.merchant1.resp_convert_create['out_amount'] == '2.4'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['28.7921', '1']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0.89'
        assert user1.merchant1.balance(curr='USD') == '2.9'
        '''


    def test_exchange_21(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange UAH to RUB: selling 10 UAH by OWNER with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=0, currency='RUB', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB')
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'create',
                               'externalid': user1.ex_id(), 'in_curr': 'UAH', 'out_curr': 'RUB',
                               'in_amount': '10', 'out_amount': None})
        assert user1.resp_delegate['in_amount'] == '10'
        assert user1.resp_delegate['in_curr'] == 'UAH'
        assert user1.resp_delegate['out_amount'] == '26.13'
        assert user1.resp_delegate['out_curr'] == 'RUB'
        assert user1.resp_delegate['rate'] == ['1', '2.61326']
        '''
        assert user1.merchant1.balance(curr='UAH') == '0'
        assert user1.merchant1.balance(curr='RUB') == '26.13'
        '''

    def test_exchange_22(self, _custom_fee, _disable_personal_exchange_fee):
        """ Exchange BTC to USD: baying 4.4 USD by MERCHANT with common fee 3% for exchange
            and with personal fee 2% for exchange. """
        admin.set_wallet_amount(balance=bl(0.005), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_wallet_amount(balance=bl(1.5), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(3), in_currency='BTC', out_currency='USD', tech_min=bl(0.0002),
                                tech_max=bl(3000))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(2))
        user1.merchant1.convert_create(in_amount=None, out_amount='4.4', in_curr='BTC', out_curr='USD')
        assert user1.merchant1.resp_convert_create['in_amount'] == '0.00125391'
        assert user1.merchant1.resp_convert_create['out_amount'] == '4.4'
        assert user1.merchant1.resp_convert_create['in_curr'] == 'BTC'
        assert user1.merchant1.resp_convert_create['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_create['rate'] == ['1', '3509.04101']
        '''
        assert user1.merchant1.balance(curr='BTC') == '0.04874609'
        assert user1.merchant1.balance(curr='USD') == '5.9'
        '''


class TestWrongExchange:
    """ Wrong exchanging. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_exchange_1(self, _merchant_activate):
        """ Exchange with inactive merchant. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='50', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32010, 'message': 'InvalidMerchant',
                                                       'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_exchange_2(self):
        """ Request with int's and float's in in_curr and out_curr. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=50, out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data': {'reason': "Key 'in_amount' must not be of 'int' type"}}
        user1.merchant1.convert_create(in_amount=None, out_amount=1.5, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070, 'message': 'InvalidParam',
                                                       'data': {'reason': "Key 'out_amount' must not be of 'float' type"}}

    def test_wrong_exchange_3(self):
        """ Exchange with in_amount wrong format. """
        admin.set_wallet_amount(balance=bl(1), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='1.122', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat', 'data': ['1.122', 'UAH']}
        user1.merchant1.convert_create(in_amount='String', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat', 'data': ['String', 'UAH']}

    def test_wrong_exchange_4(self):
        """ Exchange with out_amount wrong format. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.015', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat', 'data': ['0.015', 'USD']}
        user1.merchant1.convert_create(in_amount=None, out_amount='String', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32071, 'message': 'InvalidAmountFormat', 'data': ['String', 'USD']}

    def test_wrong_exchange_5(self):
        """ Exchange with equal pair of currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_convert_create == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_exchange_6(self):
        """ Exchange without pair of currencies. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr=None, out_curr=None)
        assert user1.merchant1.resp_convert_create == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_exchange_7(self):
        """ Exchange without in_curr. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr=None, out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32000, 'message': 'Server error',
                                                       'data': {'type': 'KeyError', 'args': ['in_curr'], 'message': "'in_curr'"}}

    def test_wrong_exchange_8(self):
        """ Exchange without out_curr. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr=None)
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency', 'data': 'out_curr'}

    def test_wrong_exchange_9(self):
        """ Exchange in to not real currency. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UAH', out_curr='UDS')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_exchange_10(self):
        """ Exchange from not real currency. """
        user1.merchant1.convert_create(in_amount=None, out_amount='0.2', in_curr='UHA', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_exchange_11(self):
        """ Exchange in to not active currency."""
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='10', out_amount=None, in_curr='UAH', out_curr='ETH')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not inactive currency')
    def test_wrong_exchange_12(self):
        """ Exchange from not active currency. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='UAH')
        assert user1.merchant1.resp_convert_create == {'code': -32076, 'message': 'InvalidCurrency'}

    @pytest.mark.skip(reason='Not disabled exchange pair')
    def test_wrong_exchange_13(self):
        """ Exchange with not active exchange pair. """
        admin.set_wallet_amount(balance=bl(0.5), currency='ETH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='0.1', out_amount=None, in_curr='ETH', out_curr='LTC')
        assert user1.merchant1.resp_convert_create == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_exchange_14(self):
        """ Exchange WITH in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount='1', out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070,
                                                       'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                                "'out_amount'."}, 'message': 'InvalidParam'}

    def test_wrong_exchange_15(self):
        """ Exchange WITHOUT in_amount and out_amount. """
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.merchant1.lid)
        user1.merchant1.convert_create(in_amount=None, out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32070,
                                                       'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                                "'out_amount'."}, 'message': 'InvalidParam'}

    def test_wrong_exchange_16(self):
        """ Exchange UAH to USD: baying 1 USD, in_amount with fee less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(31.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32072, 'message': 'InsufficientFunds'}

    def test_wrong_exchange_17(self):
        """ Exchange UAH to USD: selling 50.01 UAH, in_amount less than user has in his balance. """
        admin.set_wallet_amount(balance=bl(50), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='50.01', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32072, 'message': 'InsufficientFunds'}

    def test_wrong_exchange_18(self):
        """ Exchange UAH to USD: selling 31.02 UAH with in_amount less than admin_min in exchange table
            Exchange UAH to USD: selling 93.06 UAH with in_amount more than admin_max in exchange table.
            Exchange UAH to USD: baying 1 USD with in_amount less than admin_min in exchange table.
            Exchange UAH to USD: baying 3 USD with in_amount more than admin_max in exchange table. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(10), tech_min=bl(31.03), tech_max=bl(93.05),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_create(in_amount='31.02', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32075, 'message': 'AmountTooSmall'}
        user1.merchant1.convert_create(in_amount='93.06', out_amount=None, in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32074, 'message': 'AmountTooBig'}
        user1.merchant1.convert_create(in_amount=None, out_amount='1', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32075, 'message': 'AmountTooSmall'}
        user1.merchant1.convert_create(in_amount=None, out_amount='3', in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_create == {'code': -32074, 'message': 'AmountTooBig'}

    def test_wrong_exchange_19(self):
        """ Exchange with wrong sign. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '10', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': 'WRONG SIGN',
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {'code': -32002,
                                          'message': 'InvalidSign', 'data': {'reason': 'Not correct signature'}}


    def test_wrong_exchange_20(self):
        """ Exchange without sign = None. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_exchange_21(self):
        """ Exchange without SIGN in headers. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-utc-now-ms': user1.merchant1.time_sent()}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_exchange_22(self):
        """ Exchange with wrong merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': '105',
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32010, 'message': 'InvalidMerchant', 'data': {'reason': 'Merchant Is Not Active'}}

    def test_wrong_exchange_23(self):
        """ Exchange with None merchant id. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': 1, 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': None,
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_exchange_24(self):
        """ Exchange without merchant id in headers. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None,
                           'externalid': '123'},
                'jsonrpc': 2.0, 'id': '123456'}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-merchant to headers'}}

    def test_wrong_exchange_25(self):
        """ Exchange without IN_CURR parameter. """
        data = {'method': 'convert.create',
                'params': {'out_curr': 'USD', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.create' missing 1 argument: 'in_curr'"}}

    def test_wrong_exchange_26(self):
        """ Exchange without OUT_CURR parameter. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'in_amount': '1', 'out_amount': None, 'externalid': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {"reason": "method 'convert.create' missing 1 argument: 'out_curr'"}}

    def test_wrong_exchange_27(self):
        """ Exchange without IN_AMOUNT and OUT_AMOUNT. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'externalid': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32070,
                                          'data': {'reason': "Must be provided one amount: 'in_amount' or "
                                                             "'out_amount'."}, 'message': 'InvalidParam'}

    def test_wrong_exchange_28(self):
        """ Exchange without EXTERNAL_ID. """
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '1', 'out_amount': None},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        time_sent = user1.merchant1.time_sent()
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, "data": {'reason': "method 'convert.create' missing 1 argument: 'externalid'"},
                                          'message': 'InvalidInputParams'}

    def test_wrong_exchange_29(self):
        """ Exchange with equal EXTERNAL_ID. """
        admin.set_wallet_amount(balance=bl(100), currency='UAH', merch_lid=user1.merchant1.lid)
        ex_id = user1.merchant1._id()
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None, 'externalid': ex_id},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        requests.post(url=user1.merchant1.japi_url, json=data,
                      headers={'x-merchant': str(user1.merchant1.lid),
                               'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                               'x-utc-now-ms': time_sent}, verify=False)
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32033, 'data': {'reason': 'Duplicated key for externalid'}, 'message': 'Unique'}

    def test_wrong_exchange_30(self):
        """ Exchange with excess parameter in params field. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.create',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'in_amount': '50', 'out_amount': None,
                           'externalid': user1.merchant1._id(), 'par': '123'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.create' received a redundant argument 'par'"}}


@pytest.mark.usefixtures('_personal_exchange_fee')
class TestExchangeParams:
    """ Testing convert params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_params_1(self):
        """ Getting params for UAH -> USD by MERCHANT. """
        admin.set_wallet_amount(balance=bl(1.01), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, tech_min=bl(0.01), tech_max=bl(3000),
                                in_currency='UAH', out_currency='USD')
        user1.merchant1.convert_params(in_curr='UAH', out_curr='USD')
        assert user1.merchant1.resp_convert_params['is_convert'] is True
        assert user1.merchant1.resp_convert_params['in_curr_balance'] == '1.01'
        assert user1.merchant1.resp_convert_params['in_min'] == '0.01'
        assert user1.merchant1.resp_convert_params['in_max'] == '3000'
        assert user1.merchant1.resp_convert_params['in_curr'] == 'UAH'
        assert user1.merchant1.resp_convert_params['out_curr'] == 'USD'
        assert user1.merchant1.resp_convert_params['rate'] == ['28.1999', '1']

    def test_params_2(self):
        """ Getting params for RUB -> UAH by OWNER. """
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(10),
                                tech_max=bl(100))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.resp_delegate['out_min'] == '3.76'
        assert user1.resp_delegate['out_max'] == '37.5'
        assert user1.resp_delegate['rate'] == ['2.6666', '1']
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_3(self):
        """ Getting params for BTC -> USD by OWNER. """
        admin.set_wallet_amount(balance=bl(0.02), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.001),
                                tech_max=bl(1.3))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.resp_delegate['in_min'] == '0.001'
        assert user1.resp_delegate['in_max'] == '1.3'
        assert user1.resp_delegate['out_min'] == '3.59'
        assert user1.resp_delegate['out_max'] == '4654.85'
        assert user1.resp_delegate['in_curr'] == 'BTC'
        assert user1.resp_delegate['out_curr'] == 'USD'
        assert user1.resp_delegate['rate'] == ['1', '3580.6541']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.00000001),
                                tech_max=bl(3))

    def test_params_4(self):
        """ Getting params for USD -> UAH by OWNER with 3.8 percent common fee. """
        admin.set_wallet_amount(balance=bl(5.11), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(28.1999), fee=pers(3.8), in_currency='USD', out_currency='UAH', tech_min=bl(0.5),
                                tech_max=bl(3000))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'USD', 'out_curr': 'UAH'})
        assert user1.resp_delegate['in_curr_balance'] == '5.11'
        assert user1.resp_delegate['in_min'] == '0.5'
        assert user1.resp_delegate['in_max'] == '3000'
        assert user1.resp_delegate['out_min'] == '13.57'
        assert user1.resp_delegate['out_max'] == '81384.9'
        assert user1.resp_delegate['in_curr'] == 'USD'
        assert user1.resp_delegate['out_curr'] == 'UAH'
        assert user1.resp_delegate['rate'] == ['1', '27.1283']
        admin.set_rate_exchange(rate=bl(28.1999), fee=0, in_currency='USD', out_currency='UAH', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_5(self):
        """ Getting params for USD -> BTC by MERCHANT with 5 percent common fee. """
        admin.set_wallet_amount(balance=bl(15), currency='USD', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(5), in_currency='USD', out_currency='BTC', tech_min=bl(3),
                                tech_max=bl(3000))
        user1.merchant1.convert_params(in_curr='USD', out_curr='BTC')
        assert user1.merchant1.resp_convert_params['in_curr_balance'] == '15'
        assert user1.merchant1.resp_convert_params['in_min'] == '3'
        assert user1.merchant1.resp_convert_params['in_max'] == '3000'
        assert user1.merchant1.resp_convert_params['out_min'] == '0.00079794'
        assert user1.merchant1.resp_convert_params['out_max'] == '0.7979388'
        assert user1.merchant1.resp_convert_params['rate'] == ['3759.68681', '1']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='USD', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_6(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for UAH -> RUB by MERCHANT with 5% common fee and 3% personal fee. """
        admin.set_wallet_amount(balance=bl(15), currency='UAH', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(5), in_currency='UAH', out_currency='RUB', tech_min=bl(17),
                                tech_max=bl(950))
        admin.set_personal_exchange_fee(in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3))
        user1.merchant1.convert_params(in_curr='UAH', out_curr='RUB')
        assert user1.merchant1.resp_convert_params['in_min'] == '17'
        assert user1.merchant1.resp_convert_params['in_max'] == '950'
        assert user1.merchant1.resp_convert_params['out_min'] == '43.98'
        assert user1.merchant1.resp_convert_params['out_max'] == '2457.27'
        assert user1.merchant1.resp_convert_params['rate'] == ['1', '2.5866']
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='USD', out_currency='BTC', tech_min=bl(0.01),
                                tech_max=bl(3000))

    def test_params_7(self, _custom_fee, _disable_personal_exchange_fee):
        """ Getting params for BTC -> USD by OWNER with 5% common fee and 3% personal fee. """
        admin.set_wallet_amount(balance=bl(1), currency='BTC', merch_lid=user1.merchant1.lid)
        admin.set_rate_exchange(rate=bl(3580.6541), fee=pers(5), in_currency='BTC', out_currency='USD', tech_min=bl(0.1),
                                tech_max=bl(3))
        admin.set_personal_exchange_fee(in_curr=admin.currency['BTC'], out_curr=admin.currency['USD'],
                                        is_active=True, merchant_id=user1.merchant1.id, fee=pers(3))
        user1.delegate(params={'m_lid': user1.merchant1.lid, 'merch_model': 'convert', 'merch_method': 'params',
                               'in_curr': 'BTC', 'out_curr': 'USD'})
        assert user1.resp_delegate['out_min'] == '347.33'
        assert user1.resp_delegate['out_max'] == '10419.7'
        assert user1.resp_delegate['rate'] == ['1', '3473.23447']
        admin.set_rate_exchange(rate=bl(3580.6541), fee=0, in_currency='BTC', out_currency='USD', tech_min=bl(0.00000001),
                                tech_max=bl(3))


class TestWrongParams:
    """ Testing wrong requests for exchange params method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_wrong_params_1(self):
        """ Getting params for equal currency. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr='UAH')
        assert user1.merchant1.resp_convert_params == {'code': -32065, 'message': 'UnavailExchange'}

    def test_wrong_params_2(self):
        """ Getting params from not real currency. """
        user1.merchant1.convert_params(in_curr='UHA', out_curr='USD')
        assert user1.merchant1.resp_convert_params == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_params_3(self):
        """ Getting params to not real currency. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr='UDS')
        assert user1.merchant1.resp_convert_params == {'code': -32076, 'message': 'InvalidCurrency'}

    def test_wrong_params_4(self):
        """ Getting params with NONE in_curr. """
        user1.merchant1.convert_params(in_curr=None, out_curr='USD')
        assert user1.merchant1.resp_convert_params['message'] == 'InvalidCurrency'

    def test_wrong_params_5(self):
        """ Getting params with NONE out_curr. """
        user1.merchant1.convert_params(in_curr='UAH', out_curr=None)
        assert user1.merchant1.resp_convert_params['message'] == 'InvalidCurrency'

    def test_wrong_params_6(self):
        """ Getting params without in_curr parameter. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'out_curr': 'USD'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.params' missing 1 argument: 'in_curr'"}}

    def test_wrong_params_7(self):
        """ Getting params without out_curr parameter. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'USD'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.params' missing 1 argument: 'out_curr'"}}

    def test_wrong_params_8(self):
        """ Getting params with excess parameter in params field. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD', 'par': 'boom'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': create_sign(user1.merchant1.akey, data['params'], time_sent),
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                                          'data': {'reason': "method 'convert.params' received a redundant argument 'par'"}}

    def test_wrong_params_9(self):
        """ Getting params with NONE signature. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': None,
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32003, 'message': 'InvalidHeaders', 'data': {'reason': 'Add x-signature to headers'}}

    def test_wrong_params_10(self):
        """ Getting params with wrong signature. """
        time_sent = user1.merchant1.time_sent()
        data = {'method': 'convert.params',
                'params': {'in_curr': 'UAH', 'out_curr': 'USD'},
                'jsonrpc': 2.0, 'id': user1.merchant1._id()}
        r = requests.post(url=user1.merchant1.japi_url, json=data,
                          headers={'x-merchant': str(user1.merchant1.lid),
                                   'x-signature': 'WRONG SIGNATURE',
                                   'x-utc-now-ms': time_sent}, verify=False)
        print(r.text)
        assert loads(r.text)['error'] == {'code': -32002, 'message': 'InvalidSign', 'data': {'reason': 'Not correct signature'}}
