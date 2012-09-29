import markupsafe
import pkg_resources
from pyramid.security import authenticated_userid


SIGNIN_HTML = "<img src='https://login.persona.org/i/sign_in_blue.png' id='signin' alt='sign-in button'/>"
SIGNOUT_HTML = "<button id='signout'>logout</button>"


def button(request):
    """If the user is logged in, returns the logout button, otherwise returns the login button"""
    if not authenticated_userid(request):
        return markupsafe.Markup(SIGNIN_HTML)
    else:
        return markupsafe.Markup(SIGNOUT_HTML)


def js(request):
    """Returns the javascript needed to run persona"""
    userid = authenticated_userid(request)
    user = markupsafe.Markup("'%s'")%userid if userid else "null"
    data = {
        'user': user,
        'login': '/login',
        'logout': '/logout',
        'csrf_token': request.session.get_csrf_token()
    }
    template = markupsafe.Markup(pkg_resources.resource_string('pyramid_persona', 'templates/persona.js'))
    return template % data