import pytest
from users.tools import *


@pytest.mark.positive
@pytest.mark.usefixtures('_personal_pwexchange_fee')
class TestPwconvertCalc:

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session

    def test_pwconvert_calc_1(self):
        """ Calc exchange UAH to RUB: selling 33.15 UAH by MERCHANT: VISAMC. """
        admin.set_wallet_amount(balance=bl(90), currency='UAH', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='UAH', out_currency='RUB', tech_min=bl(1), tech_max=bl(1000))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=0)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['visamc'], tp=10)
        user1.pwmerchant_VISAMC.convert(method='calc', params={'in_amount': '33.15', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'RUB'})
        assert user1.pwmerchant_VISAMC.resp_convert['in_amount'] == '33.15'
        assert user1.pwmerchant_VISAMC.resp_convert['out_amount'] == '88.39'
        assert user1.pwmerchant_VISAMC.resp_convert['rate'] == ['1', '2.6666']

    def test_pwconvert_calc_2(self):
        """ Calc exchange RUB to UAH: baying 5.27 UAH by OWNER: VISAMC. """
        admin.set_wallet_amount(balance=bl(20), currency='RUB', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(100))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['visamc'], tp=0)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=10)
        user1.delegate(params={'m_lid': user1.pwmerchant_VISAMC.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_amount': None, 'out_amount': '5.27', 'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.resp_delegate['in_amount'] == '14.06'
        assert user1.resp_delegate['out_amount'] == '5.27'

    def test_pwconvert_calc_3(self):
        """ Calc exchange RUB to USD: baying 2 USD by OWNER: PAYEER. """
        admin.set_wallet_amount(balance=bl(130), currency='RUB', merch_lid=user1.pwmerchant_PAYEER.lid)
        admin.set_rate_exchange(rate=bl(63.8888), fee=pers(0.2), in_currency='RUB', out_currency='USD', tech_min=bl(1), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=0)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=10)
        user1.delegate(params={'m_lid': user1.pwmerchant_PAYEER.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_amount': None, 'out_amount': '2', 'in_curr': 'RUB', 'out_curr': 'USD'})
        assert user1.resp_delegate['in_amount'] == '128.04'
        assert user1.resp_delegate['out_amount'] == '2'
        assert user1.resp_delegate['rate'] == ['64.01658', '1']

    def test_pwconvert_calc_4(self):
        """ Calc exchange RUB to UAH: selling 55.3 RUB by MERCHANT: VISAMC. """
        admin.set_wallet_amount(balance=bl(60), currency='RUB', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(50), in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['visamc'], tp=0)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=10)
        user1.pwmerchant_VISAMC.convert(method='calc', params={'in_amount': '55.3', 'out_amount': None, 'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.pwmerchant_VISAMC.resp_convert['in_amount'] == '55.3'
        assert user1.pwmerchant_VISAMC.resp_convert['out_amount'] == '13.82'
        assert user1.pwmerchant_VISAMC.resp_convert['rate'] == ['3.9999', '1']

    def test_pwconvert_calc_5(self, _disable_custom_pwfee):
        """ Calc exchange UAH to RUB: selling 10 UAH with common fee 3% and personal fee 2% by MERCHANT: VISAMC. """
        admin.params['merch'] = {'lid': user1.pwmerchant_VISAMC.lid, 'id': user1.pwmerchant_VISAMC.id}
        admin.set_wallet_amount(balance=bl(10), currency='UAH', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB', tech_min=bl(1), tech_max=bl(200))
        admin.set_merchant(lid=user1.pwmerchant_VISAMC.lid, is_customfee=True)
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        merchant_id=user1.pwmerchant_VISAMC.id, is_active=True)
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=0)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['visamc'], tp=10)
        user1.pwmerchant_VISAMC.convert(method='calc', params={'in_amount': '10', 'out_amount': None, 'in_curr': 'UAH', 'out_curr': 'RUB'})
        assert user1.pwmerchant_VISAMC.resp_convert['in_amount'] == '10'
        assert user1.pwmerchant_VISAMC.resp_convert['out_amount'] == '26.13'
        assert user1.pwmerchant_VISAMC.resp_convert['rate'] == ['1', '2.61326']

    def test_pwconvert_calc_6(self):
        """ Calc exchange USD to RUB: selling 3.15 USD with absolute payin fee 0.3 USD and percent payin fee 1,5 %
            and with absolute payout fee 2 RUB and percent payout fee 2% by OWNER: PAYEER. """
        admin.set_wallet_amount(balance=bl(10), currency='USD', merch_lid=user1.pwmerchant_PAYEER.lid)
        admin.set_rate_exchange(rate=bl(63.8888), fee=0, in_currency='USD', out_currency='RUB', tech_min=bl(1), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=0, add=bl(0.3), mult=pers(1.5))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=10, add=bl(2), mult=pers(2))
        user1.delegate(params={'m_lid': user1.pwmerchant_PAYEER.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_amount': '3.15', 'out_amount': None, 'in_curr': 'USD', 'out_curr': 'RUB'})
        assert user1.resp_delegate['in_amount'] == '3.15'
        assert user1.resp_delegate['orig_amount'] == '3.15'
        assert user1.resp_delegate['out_amount'] == '173.3'
        assert user1.resp_delegate['rate'] == ['1', '63.8888']

    def test_pwconvert_calc_7(self):
        """ Calc exchange RUB to UAH: baying 15.64 UAH with absolute payin fee 1 RUB and percent payin fee 3 %
            and with absolute payout fee 2 UAH and percent payout fee 5.4% by MERCHANT: VISAMC. """
        admin.set_wallet_amount(balance=bl(55), currency='RUB', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=0, in_currency='RUB', out_currency='UAH', tech_min=bl(1), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['visamc'], tp=0, add=bl(1), mult=pers(3))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['visamc'], tp=10, add=bl(2), mult=pers(5.4))
        user1.pwmerchant_VISAMC.convert(method='calc', params={'in_amount': None, 'out_amount': '15.64', 'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.pwmerchant_VISAMC.resp_convert['in_amount'] == '52.31'
        assert user1.pwmerchant_VISAMC.resp_convert['orig_amount'] == '15.64'
        assert user1.pwmerchant_VISAMC.resp_convert['out_amount'] == '15.64'
        assert user1.pwmerchant_VISAMC.resp_convert['rate'] == ['2.6666', '1']

    def test_pwconvert_calc_8(self, _disable_custom_pwfee, _disable_personal_exchange_fee):
        """ Calc exchange USD to RUB: baying 95 RUB with 3 % common exchange fee and with 2% personal exchange fee by OWNER: PAYEER. """
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.pwmerchant_PAYEER.lid)
        admin.set_rate_exchange(rate=bl(63.8888), fee=pers(3), in_currency='USD', out_currency='RUB', tech_min=bl(1.92), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=0, add=bl(0.3), mult=pers(1.5),
                      _min=bl(0.32), _max=bl(0.34))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=10, add=bl(2), mult=pers(5.4),
                      _min=bl(3.97), _max=bl(3.99))
        admin.set_merchant(lid=user1.pwmerchant_PAYEER.lid, is_customfee=True)
        admin.params['merch'] = {'lid': user1.pwmerchant_PAYEER.lid, 'id': user1.pwmerchant_PAYEER.id}
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['USD'], out_curr=admin.currency['RUB'],
                                        merchant_id=user1.pwmerchant_PAYEER.id, is_active=True)
        user1.delegate(params={'m_lid': user1.pwmerchant_PAYEER.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_amount': None, 'out_amount': '95', 'in_curr': 'USD', 'out_curr': 'RUB'})
        assert user1.resp_delegate['in_amount'] == '52.31'
        assert user1.resp_delegate['out_amount'] == '15.64'
        assert user1.resp_delegate['rate'] == ['1', '62.61102']

    def test_pwconvert_calc_9(self, _disable_custom_pwfee, _disable_personal_exchange_fee):
        """ Calc exchange UAH to RUB: selling 25.9 UAH with 3 % common exchange fee and with 1.7% personal exchange fee by MERCHANT: VISAMC. """
        admin.set_wallet_amount(balance=bl(26), currency='UAH', merch_lid=user1.pwmerchant_VISAMC.lid)
        admin.set_rate_exchange(rate=bl(2.6666), fee=pers(3), in_currency='UAH', out_currency='RUB', tech_min=bl(1), tech_max=bl(200))
        admin.set_fee(currency_id=admin.currency['UAH'], payway_id=admin.payway_id['payeer'], tp=0, add=bl(2), mult=pers(3))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=10, add=bl(2.2), mult=pers(1))
        admin.set_merchant(lid=user1.pwmerchant_VISAMC.lid, is_customfee=True)
        admin.params['merch'] = {'lid': user1.pwmerchant_VISAMC.lid, 'id': user1.pwmerchant_VISAMC.id}
        admin.set_personal_exchange_fee(fee=pers(1.7), in_curr=admin.currency['UAH'], out_curr=admin.currency['RUB'],
                                        merchant_id=user1.pwmerchant_VISAMC.id, is_active=True)
        user1.pwmerchant_VISAMC.convert(method='calc', params={'in_amount': '25.9', 'out_amount': None, 'in_curr': 'RUB', 'out_curr': 'UAH'})
        assert user1.pwmerchant_VISAMC.resp_convert['in_amount'] == '52.31'
        assert user1.pwmerchant_VISAMC.resp_convert['out_amount'] == '15.64'
        assert user1.pwmerchant_VISAMC.resp_convert['rate'] == ['1', '2.62126']

    def test_pwconvert_calc_10(self, _disable_custom_pwfee, _disable_personal_exchange_fee):
        """ Calc exchange USD to RUB: baying 95 RUB with 3 % common exchange fee and with 2% personal exchange fee
            with common payin fee 1 USD and 2%, with personal payin fee 0.3 USD and 1.5%
            with common payout fee 3 RUB and 3% with personal payout fee 2 RUB and 2% by MERCHANT: PAYEER. """
        admin.params['merch'] = {'lid': user1.pwmerchant_PAYEER.lid, 'id': user1.pwmerchant_PAYEER.id}
        admin.set_wallet_amount(balance=bl(2), currency='USD', merch_lid=user1.pwmerchant_PAYEER.lid)
        admin.set_rate_exchange(rate=bl(63.8888), fee=pers(3), in_currency='USD', out_currency='RUB', tech_min=bl(1), tech_max=bl(1.92))
        admin.set_merchant(lid=user1.pwmerchant_PAYEER.lid, is_customfee=True)
        admin.set_personal_exchange_fee(fee=pers(2), in_curr=admin.currency['USD'], out_curr=admin.currency['RUB'],
                                        merchant_id=user1.pwmerchant_PAYEER.id, is_active=True)
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=0, add=bl(1), mult=pers(2))
        admin.set_fee(currency_id=admin.currency['USD'], payway_id=admin.payway_id['payeer'], tp=0, add=bl(0.3), mult=pers(1.5),
                      merchant_id=user1.pwmerchant_PAYEER.id, is_active=True)
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=10, add=bl(3), mult=pers(3))
        admin.set_fee(currency_id=admin.currency['RUB'], payway_id=admin.payway_id['payeer'], tp=10, add=bl(2), mult=pers(2),
                      merchant_id=user1.pwmerchant_PAYEER.id, is_active=True)
        user1.delegate(params={'m_lid': user1.pwmerchant_PAYEER.lid, 'merch_model': 'convert', 'merch_method': 'calc',
                               'in_amount': None, 'out_amount': '95', 'in_curr': 'USD', 'out_curr': 'RUB'})