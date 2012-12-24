import unittest
from pyramid.httpexceptions import HTTPBadRequest
import requests

from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(autocommit=False)
        self.config.add_settings({'persona.audiences': 'http://someaudience'})
        self.config.include('pyramid_persona')
        self.security_policy = self.config.testing_securitypolicy()
        self.config.set_authorization_policy(self.security_policy)
        self.config.set_authentication_policy(self.security_policy)
        self.config.commit()

    def tearDown(self):
        testing.tearDown()

    def test_login(self):
        from .views import login
        data = requests.get('http://personatestuser.org/email_with_assertion/http%3A%2F%2Fsomeaudience').json()
        email = data['email']
        assertion = data['assertion']

        request = testing.DummyRequest()
        request.params['assertion'] = assertion
        request.params['csrf_token'] = request.session.get_csrf_token()
        request.params['came_from'] = '/'
        response = login(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.security_policy.remembered, email)

    def test_login_fails_with_bad_audience(self):
        from .views import login
        data = requests.get('http://personatestuser.org/email_with_assertion/http%3A%2F%2Fbadaudience').json()
        email = data['email']
        assertion = data['assertion']

        request = testing.DummyRequest()
        request.params['assertion'] = assertion
        request.params['csrf_token'] = request.session.get_csrf_token()
        request.params['came_from'] = '/'

        self.assertRaises(HTTPBadRequest, login, request)
        self.assertFalse(hasattr(self.security_policy, 'remembered'))

    def test_logout(self):
        from .views import logout
        request = testing.DummyRequest()
        request.params['csrf_token'] = request.session.get_csrf_token()
        request.params['came_from'] = '/'
        response = logout(request)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.security_policy.forgotten)


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.config.add_settings({'persona.secret': 'testingsecret',
                                  'persona.audiences': 'http://someaudience',
                                  'persona.login_path': '/awesomeloginpath',
                                  'persona.logout_path': '/awesomelogoutpath'})
        self.config.include('pyramid_persona')

    def test_login_path(self):
        from pyramid_persona.utils import js
        request = testing.DummyRequest()
        javascript = js(request)
        assert '/awesomeloginpath' in javascript
        assert '/awesomelogoutpath' in javascript
