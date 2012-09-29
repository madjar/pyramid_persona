from pyramid.authentication import SessionAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import ConfigurationError
from pyramid.interfaces import ISessionFactory
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid_persona.utils import button, js
from pyramid_persona.views import login, logout, forbidden


def includeme(config):
    """Include persona settings into a pyramid config.

    This function does the following:

        * Setup default authentication and authorization policies, and a default session factory.
          Keep in mind that the sessions are not encrypted, if you need to store secret information in it, please
          override the session factory.
        * Add two request attributes :
            * persona_js, the javascript code to inclue on a page to make persona work.
            * persona_button, the html for a default login/logout button.
        * Set login and logout views for use with persona.
        * Set a forbidden view with a loggin button
    """
    settings = config.get_settings()

    if not 'persona.audience' in settings:
        raise ConfigurationError('Missing persona.audience settings. This is needed for security reasons. '
                                 'See https://developer.mozilla.org/en-US/docs/Persona/Security_Considerations for details.')

    # Default authentication and authorization policies. Those are needed to remember the userid.
    authn_policy = SessionAuthenticationPolicy()
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    # A default session factory, needed for the csrf check.

    secret = settings.get('persona.secret', None)
    session_factory = UnencryptedCookieSessionFactoryConfig(secret)
    config.set_session_factory(session_factory)

    # Either a secret must be provided or the session factory must be overriden.
    def check():
        if config.registry.queryUtility(ISessionFactory) == session_factory and not secret:
            raise ConfigurationError('If you do not override the session factory, you have to provide a persona.secret settings.')
    config.action(None, check)


    # Login and logout views.
    login_route = settings.get('persona.login_route', 'login')
    login_path = settings.get('persona.login_path', '/login')
    config.add_route(login_route, login_path)
    config.add_view(login, route_name=login_route, check_csrf=True)

    logout_route = settings.get('persona.logout_route', 'logout')
    logout_path = settings.get('persona.logout_path', '/logout')
    config.add_route(logout_route, logout_path)
    config.add_view(logout, route_name=logout_route, check_csrf=True)

    # A simple 403 view, with a login button.
    config.add_forbidden_view(forbidden)

    # A quick access to the login button
    config.add_request_method(button, 'persona_button', reify=True)

    # The javascript needed by persona
    config.add_request_method(js, 'persona_js', reify=True)