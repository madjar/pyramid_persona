import unittest
from pyramid.interfaces import IAuthorizationPolicy, IAuthenticationPolicy
from pyramid.testing import DummySecurityPolicy
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
        self.config = testing.setUp()
        self.config.add_settings({'persona.audience': 'http://someaudience'})
#        self.config.include('pyramid_persona')
        self.security_policy = SecurityPolicy()
        self.config.registry.registerUtility(self.security_policy, IAuthorizationPolicy)
        self.config.registry.registerUtility(self.security_policy, IAuthenticationPolicy)

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        from .views import login
        data = requests.get('http://personatestuser.org/email_with_assertion/http%3A%2F%2Fsomeaudience').json
        email = data['email']
        assertion = data['assertion']

        request = testing.DummyRequest({'assertion': assertion})
        response = login(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.security_policy.remembered, email)

    def test_logout(self):
        from .views import logout
        request = testing.DummyRequest()
        response = logout(request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.security_policy.forgotten)
