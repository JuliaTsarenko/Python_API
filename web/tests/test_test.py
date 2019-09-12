import pytest
from web.users import *


class TestFirst:
    """Order_get"""

    def test_0(self, start_session):
        """ Warm. """
        global admin, user1, user2
        admin, user1 = start_session

