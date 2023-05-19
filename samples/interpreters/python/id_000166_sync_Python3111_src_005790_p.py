

















"""Tests for authentication functions.

"""

import ipaddress
import unittest
from datetime import timedelta
from unittest.mock import patch


from cmstestsuite.unit_tests.databasemixin import DatabaseMixin

from cms import config
from cms.server.contest.authentication import validate_login, \
    authenticate_request


from cmscommon.crypto import build_password, hash_password
from cmscommon.datetime import make_datetime


class TestValidateLogin(DatabaseMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.timestamp = make_datetime()
        self.add_contest()
        self.contest = self.add_contest(allow_password_authentication=True)
        self.add_user(username="otheruser")
        self.user = self.add_user(
            username="myuser", password=build_password("mypass"))
        self.participation = self.add_participation(
            contest=self.contest, user=self.user)

    def assertSuccess(self, username, password, ip_address):
        
        
        
        
        self.session.flush()
        self.session.expire(self.user)
        self.session.expire(self.contest)

        authenticated_participation, cookie = validate_login(
            self.session, self.contest, self.timestamp,
            username, password, ipaddress.ip_address(ip_address))

        self.assertIsNotNone(authenticated_participation)
        self.assertIsNotNone(cookie)
        self.assertIs(authenticated_participation, self.participation)
        self.assertIs(authenticated_participation.user, self.user)
        self.assertIs(authenticated_participation.contest, self.contest)

    def assertFailure(self, username, password, ip_address):
        authenticated_participation, cookie = validate_login(
            self.session, self.contest, self.timestamp,
            username, password, ipaddress.ip_address(ip_address))

        self.assertIsNone(authenticated_participation)
        self.assertIsNone(cookie)

    def test_successful_login(self):
        self.assertSuccess("myuser", "mypass", "127.0.0.1")

    def test_no_user(self):
        self.assertFailure("myotheruser", "mypass", "127.0.0.1")

    def test_no_participation_for_user_in_contest(self):
        other_contest = self.add_contest(allow_password_authentication=True)
        other_user = self.add_user(
            username="myotheruser", password=build_password("mypass"))
        self.add_participation(contest=other_contest, user=other_user)

        self.assertFailure("myotheruser", "mypass", "127.0.0.1")

    def test_participation_specific_password(self):
        self.participation.password = build_password("myotherpass")

        self.assertFailure("myuser", "mypass", "127.0.0.1")
        self.assertSuccess("myuser", "myotherpass", "127.0.0.1")

    def test_unallowed_password_authentication(self):
        self.contest.allow_password_authentication = False

        self.assertFailure("myuser", "mypass", "127.0.0.1")

    def test_unallowed_hidden_participation(self):
        self.contest.block_hidden_participations = True
        self.participation.hidden = True

        self.assertFailure("myuser", "mypass", "127.0.0.1")

    def test_invalid_password_stored_in_user(self):
        
        self.user.password = "mypass"

        
        self.assertFailure("myuser", "mypass", "127.0.0.1")

    def test_invalid_password_stored_in_participation(self):
        
        self.participation.password = "myotherpass"

        
        self.assertFailure("myuser", "myotherpass", "127.0.0.1")

    def test_ip_lock(self):
        self.contest.ip_restriction = True
        self.participation.ip = [ipaddress.ip_network("10.0.0.0/24")]

        self.assertSuccess("myuser", "mypass", "10.0.0.1")
        self.assertFailure("myuser", "wrongpass", "10.0.0.1")
        self.assertFailure("myuser", "mypass", "10.0.1.1")

        self.participation.ip = [ipaddress.ip_network("10.9.0.0/24"),
                                 ipaddress.ip_network("127.0.0.1/32")]

        self.assertSuccess("myuser", "mypass", "127.0.0.1")
        self.assertFailure("myuser", "mypass", "127.0.0.0")
        self.assertSuccess("myuser", "mypass", "10.9.0.7")

        
        self.participation.ip = []
        self.assertFailure("myuser", "mypass", "10.0.0.1")

        self.participation.ip = None
        self.assertSuccess("myuser", "mypass", "10.0.0.1")

    def test_deactivated_ip_lock(self):
        self.contest.ip_restriction = False
        self.participation.ip = [ipaddress.ip_network("10.0.0.0/24")]

        self.assertSuccess("myuser", "mypass", "10.0.1.1")


class TestAuthenticateRequest(DatabaseMixin, unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.timestamp = make_datetime()
        self.add_contest()
        self.contest = self.add_contest()
        self.add_user(username="otheruser")
        self.user = self.add_user(
            username="myuser", password=build_password("mypass"))
        self.participation = self.add_participation(
            contest=self.contest, user=self.user)
        _, self.cookie = validate_login(
            self.session, self.contest, self.timestamp, self.user.username,
            "mypass", ipaddress.ip_address("10.0.0.1"))

    def attempt_authentication(self, **kwargs):
        
        
        
        return authenticate_request(
            self.session, self.contest,
            kwargs.get("timestamp", self.timestamp),
            kwargs.get("cookie", self.cookie),
            ipaddress.ip_address(kwargs.get("ip_address", "10.0.0.1")))

    def assertSuccess(self, **kwargs):
        
        
        
        

        
        
        
        
        self.session.flush()
        self.session.expire(self.user)
        self.session.expire(self.contest)

        authenticated_participation, cookie = \
            self.attempt_authentication(**kwargs)

        self.assertIsNotNone(authenticated_participation)
        self.assertIs(authenticated_participation, self.participation)
        self.assertIs(authenticated_participation.user, self.user)
        self.assertIs(authenticated_participation.contest, self.contest)

        return cookie

    def assertSuccessAndCookieRefreshed(self, **kwargs):
        
        
        
        
        cookie = self.assertSuccess(**kwargs)
        self.assertIsNotNone(cookie)
        return cookie

    def assertSuccessAndCookieCleared(self, **kwargs):
        
        
        
        
        
        cookie = self.assertSuccess(**kwargs)
        self.assertIsNone(cookie)

    def assertFailure(self, **kwargs):
        
        
        authenticated_participation, cookie = \
            self.attempt_authentication(**kwargs)
        self.assertIsNone(authenticated_participation)
        self.assertIsNone(cookie)

    @patch.object(config, "cookie_duration", 10)
    def test_cookie_contains_timestamp(self):
        self.contest.ip_autologin = False
        self.contest.allow_password_authentication = True

        
        self.assertSuccessAndCookieRefreshed()

        
        new_cookie = self.assertSuccessAndCookieRefreshed(
            timestamp=self.timestamp + timedelta(seconds=8))

        
        self.assertFailure(timestamp=self.timestamp + timedelta(seconds=14))

        
        self.assertSuccessAndCookieRefreshed(
            timestamp=self.timestamp + timedelta(seconds=14),
            cookie=new_cookie)

    def test_cookie_contains_password(self):
        self.contest.ip_autologin = False

        
        self.contest.allow_password_authentication = False
        self.assertFailure()
        self.contest.allow_password_authentication = True

        
        self.user.password = build_password("newpass")
        self.assertFailure()

        
        self.participation.password = build_password("mypass")
        self.assertSuccessAndCookieRefreshed()

        
        self.user.password = build_password("mypass")
        self.participation.password = build_password("newpass")
        self.assertFailure()

    def test_ip_autologin(self):
        self.contest.ip_autologin = True
        self.contest.allow_password_authentication = False

        self.participation.ip = [ipaddress.ip_network("10.0.0.1/32")]
        self.assertSuccessAndCookieCleared()

        self.assertFailure(ip_address="10.1.0.1")

        self.participation.ip = [ipaddress.ip_network("10.0.0.0/24")]
        self.assertFailure()

    def test_ip_autologin_with_ambiguous_addresses(self):
        
        self.contest.ip_autologin = True
        self.contest.allow_password_authentication = False
        self.participation.ip = [ipaddress.ip_network("10.0.0.1/32")]
        other_user = self.add_user()
        other_participation = self.add_participation(
            contest=self.contest, user=other_user,
            ip=[ipaddress.ip_network("10.0.0.1/32")])
        self.assertFailure()

        
        self.contest.allow_password_authentication = True
        self.assertFailure()

        
        
        self.contest.ip_autologin = False
        self.assertSuccessAndCookieRefreshed()

        
        
        self.contest.ip_autologin = True
        self.contest.block_hidden_participations = True
        other_participation.hidden = True
        self.assertSuccessAndCookieCleared()

        
        self.contest.block_hidden_participations = False
        self.assertFailure()

    def test_invalid_password_in_database(self):
        self.contest.ip_autologin = False
        self.contest.allow_password_authentication = True
        self.user.password = "not a valid password"
        self.assertFailure()

        self.user.password = build_password("mypass")
        self.participation.password = "not a valid password"
        self.assertFailure()

    def test_invalid_cookie(self):
        self.contest.ip_autologin = False
        self.contest.allow_password_authentication = True
        self.assertFailure(cookie=None)
        self.assertFailure(cookie="not a valid cookie")

    def test_no_user(self):
        self.session.delete(self.user)
        self.assertFailure()

    def test_no_participation_for_user_in_contest(self):
        self.session.delete(self.participation)
        self.assertFailure()

    def test_hidden_user(self):
        self.contest.ip_autologin = True
        self.contest.allow_password_authentication = True
        self.contest.block_hidden_participations = True
        self.participation.hidden = True
        self.assertFailure()

    def test_ip_lock(self):
        self.contest.ip_autologin = True
        self.contest.allow_password_authentication = True
        self.contest.ip_restriction = True
        self.participation.ip = [ipaddress.ip_network("10.0.0.0/24"),
                                 ipaddress.ip_network("127.0.0.1/32")]

        self.assertSuccessAndCookieCleared(ip_address="127.0.0.1")
        self.assertSuccessAndCookieRefreshed(ip_address="10.0.0.1")
        self.assertFailure(ip_address="10.1.0.1")

        self.contest.ip_restriction = False
        self.assertSuccessAndCookieRefreshed()

        
        self.contest.ip_restriction = True
        self.participation.ip = []
        self.assertFailure()

        self.participation.ip = None
        self.assertSuccessAndCookieRefreshed()


if __name__ == "__main__":
    unittest.main()
