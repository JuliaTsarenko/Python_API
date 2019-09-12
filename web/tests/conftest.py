import pytest
from web.users.user import User
from users.admin import Admin
from users.tools import *
import selenium


def pytest_addoption(parser):
    parser.addoption(
        '--ADMIN', action='store', default='', help=' Getting admin token '
    )
    parser.addoption(
        '--USER1', action='store', default='', help=' Getting user1 email and password '
    )
    parser.addoption(
        '--USER2', action='store', default='', help=' Getting user2 email and password '
    )


@pytest.fixture(scope='session', autouse=False)
def comline(request):
    print('In comline')
    return {'admin': request.config.getoption('--ADMIN'),
            'user1': request.config.getoption('--USER1'),
            'user2': request.config.getoption('--USER2'),
            }


@pytest.yield_fixture(scope='session', autouse=True)
def start_session(comline):
    print('\n Start session')
    global admin, user1  # , user2
    if comline['admin'] == '':
        admin = Admin(email='viktor.yahoda@gmail.com', pwd='*Anycash15')
    else:
        print(' Admin token...')
        admin = Admin(token=comline['admin'])
    user1 = User(user={'email': comline['user1'].split(':')[0], 'pwd': comline['user1'].split(':')[1]})
    # user2 = User(user(email=comline['user2'].split(':')[0]), pwd=comline['user2'].split(':')[1]))
    user1.authorization(user1.email, pwd=user1.pwd)
    # user2.authorization_by_email(user2.email, pwd=user2.pwd)
    yield admin, user1  # , user2
    user1.logout()
    user1.driver.quit()
