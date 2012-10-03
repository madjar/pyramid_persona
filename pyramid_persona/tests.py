import unittest
from pyramid.interfaces import IAuthorizationPolicy, IAuthenticationPolicy
from pyramid.testing import DummySecurityPolicy
from pyramid.httpexceptions import HTTPBadRequest
import requests

from pyramid import testing


class SecurityPolicy(DummySecurityPolicy):
    remembered = None
    forgotten = None
    def remember(self, request, principal, **kw):
        self.remembered = principal
        return []

    def forget(self, request):
        self.forgotten = True
        return []


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(autocommit=False)
        self.config.add_settings({'persona.audiences': 'http://someaudience'})
        self.config.include('pyramid_persona')
        self.security_policy = SecurityPolicy()
        self.config.set_authorization_policy(self.security_policy)
        self.config.set_authentication_policy(self.security_policy)
        self.config.commit()

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        from .views import login
        data = requests.get('http://personatestuser.org/email_with_assertion/http%3A%2F%2Fsomeaudience').json
        email = data['email']
        assertion = data['assertion']

        request = testing.DummyRequest()
        request.params['assertion'] = assertion
        request.params['csrf_token'] = request.session.get_csrf_token()
        response = login(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.security_policy.remembered, email)

    def test_login_fails_with_bad_audience(self):
        from .views import login
        data = requests.get('http://personatestuser.org/email_with_assertion/http%3A%2F%2Fbadaudience').json
        email = data['email']
        assertion = data['assertion']

        request = testing.DummyRequest()
        request.params['assertion'] = assertion
        request.params['csrf_token'] = request.session.get_csrf_token()

        self.assertRaises(HTTPBadRequest, login, request)
        self.assertEqual(self.security_policy.remembered, None)

    def test_logout(self):
        from .views import logout
        request = testing.DummyRequest()
        request.params['csrf_token'] = request.session.get_csrf_token()
        response = logout(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.security_policy.forgotten)
