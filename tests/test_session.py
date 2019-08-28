import pytest
from users.tools import *
import requests
from users.sign import create_sign
from json import loads
import time
from users.user import User
from users import merchant
import pprint
from users.admin import Admin


@pytest.mark.usefixtures('allow_many_session')
class TestGet:
    """ Testing session get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)

    def test_1(self):
        """ Success requests without sess_id. """
        r = user1.session_get()
        assert r.get('user_id') == user1.id, r

    def test_2(self):
        """ Success requests with sess_id. """
        session_id = admin.get_session(key={'owner_id': user1.id})[0]['id']
        r = user1.session_get(sess_id=str(session_id))
        assert r.get('user_id') == user1.id, r
        assert r.get('id') == session_id, r

    def test_3(self):
        """ Success requests with many sess_id. """
        sessions = admin.get_session(key={'owner_id': user1.id})
        session_id1 = sessions[0]['id']
        session_id2 = sessions[1]['id']
        r1 = user1.session_get(sess_id=str(session_id1))
        r2 = user1.session_get(sess_id=str(session_id2))
        assert r1.get('user_id') == r2.get('user_id') == user1.id
        assert r1.get('id') == session_id1, r1
        assert r2.get('id') == session_id2, r2

    def test_4(self):
        """ Request with wrong sess_id. """
        session_id = admin.get_session(key={'owner_id': user2.id})[0]['id']
        r = user1.session_get(sess_id=str(session_id))
        assert r['error'] == {'code': -32090, 'message': 'NotFound'}, r

    def test_5(self):
        """ Request with invalid value. """
        r = user1.session_get(sess_id='test')
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'Invalid value for session_id: test'}}, r

    def test_6(self):
        """ Request with wrong param."""
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.get',
                                      'params': {'unknown': 'test'},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                headers=user1.headers, verify=False).text)
        assert r['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                              'data': {'reason': "method 'session.get' received a redundant argument 'unknown'"}}, r

    def test_7(self):
        """ Request without headers. """
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.get',
                                      'params': {},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                verify=False).text)
        assert r['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                              'data': {'reason': "Add x-token to headers"}}, r


@pytest.mark.usefixtures('allow_many_session')
class TestList:
    """ Testing session get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)

    def test_1(self):
        """ Success request without filters. """
        r = user1.session_list()
        assert r['data'][0].get('user_id') == user1.id, r

    def test_2(self):
        """ Success request with many sessions. """
        r = user1.session_list()['data']
        assert r[0].get('user_id') == user1.id, r
        assert r[1].get('user_id') == user1.id, r
        assert r[2].get('user_id') == user1.id, r
        assert r[0]['create_time'] > r[1]['create_time']
        assert r[1]['create_time'] > r[2]['create_time']

    def test_3(self):
        """ Count filter test. """
        count = 3
        r = user1.session_list(count=str(count))['data']
        len = r.__len__()
        assert len == count or len == r['total']

    def test_4(self):
        """ Count filter test. """
        count = 0
        r = user1.session_list(count=str(count))
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'count - has to be more than zero'}}

    def test_5(self):
        """ Count filter test. """
        r = user1.session_list(count=10)
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': "Key 'count' must not be of 'int' type"}}

    def test_6(self):
        """ First filter test. """
        r = user1.session_list()['data'][1]
        test_r = user1.session_list(first='1')['data'][0]
        assert r == test_r

    def test_7(self):
        """ First filter test. """
        r = user1.session_list(first=1)
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': "Key 'first' must not be of 'int' type"}}

    def test_8(self):
        """ First filter test. """
        r = user1.session_list(first='one')
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'first - has to be an Integer'}}

    def test_9(self):
        """ First filter test. """
        r = user1.session_list(first='9999999')['data']
        assert not r


@pytest.mark.usefixtures('allow_many_session')
class TestDelete:
    """ Testing session get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)

    def test_1(self):
        """ Success request with sess_id. """
        session_id = admin.get_session(key={'owner_id': user1.id})[1]['id']
        r = user1.session_delete(sess_id=str(session_id))
        print(r)
        assert r.get('user_id') == user1.id, r
        assert r.get('id') == session_id, r

    def test_2(self):
        """ Wrong request with active sess_id. """
        session_id = admin.get_session(key={'owner_id': user1.id})[0]['id']
        r = user1.session_delete(sess_id=str(session_id))
        assert r['error'] == {'code': -32034, 'message': 'Forbidden',
                              'data': {'reason': 'Active session cannot be deleted'}}, r

    def test_3(self):
        """ Wrong requests without sess_id. """
        r = user1.session_delete()
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'Invalid value for session_id: None'}}, r

    def test_4(self):
        """ Request with wrong sess_id. """
        session_id = admin.get_session(key={'owner_id': user2.id})[0]['id']
        r = user1.session_delete(sess_id=str(session_id))
        assert r['error'] == {'code': -32090, 'message': 'NotFound',
                              'data': {'reason': 'no session found with id: ' + str(session_id)}}, r

    def test_5(self):
        """ Request with invalid value. """
        r = user1.session_delete(sess_id='test')
        assert r['error'] == {'code': -32070, 'message': 'InvalidParam',
                              'data': {'reason': 'Invalid value for session_id: test'}}, r

    def test_6(self):
        """ Request with wrong param."""
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.delete',
                                      'params': {'unknown': 'test'},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                headers=user1.headers, verify=False).text)
        assert r['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                              'data': {'reason': "method 'session.delete' received a redundant argument 'unknown'"}}, r

    def test_7(self):
        """ Request without headers. """
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.delete',
                                      'params': {},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                verify=False).text)
        assert r['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                              'data': {'reason': "Add x-token to headers"}}, r


@pytest.mark.usefixtures('allow_many_session')
class TestDeleteAll:
    """ Testing session get method. """

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1, user2 = start_session
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)
        user1.authorization_by_email(email=user1.email, pwd=user1.pwd)

    def test_1(self):
        """ Success request. """
        session_id = admin.get_session(key={'owner_id': user1.id})[0]['id']
        r = user1.session_delete_all()
        assert r.__len__() == 2, r
        assert r[0].get('id') != session_id, r
        assert r[1].get('id') != session_id, r

    def test_2(self):
        """ Wrong request by one active session. """
        r = user1.session_delete_all()
        assert r['error'] == {'code': -32090, 'message': 'NotFound',
                              'data': {'reason': 'no sessions found except active one'}}, r

    def test_3(self):
        """ Request with wrong param."""
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.delete_all',
                                      'params': {'unknown': 'test'},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                headers=user1.headers, verify=False).text)
        assert r['error'] == {'code': -32602, 'message': 'InvalidInputParams',
                              'data': {'reason': "method 'session.delete_all' received a redundant argument 'unknown'"}}, r

    def test_4(self):
        """ Request without headers. """
        r = loads(requests.post(url=user1.wapi_url,
                                json={'method': 'session.delete_all',
                                      'params': {},
                                      'jsonrpc': 2.0, 'id': user1.ex_id()},
                                verify=False).text)
        assert r['error'] == {'code': -32003, 'message': 'InvalidHeaders',
                              'data': {'reason': "Add x-token to headers"}}, r