"""This is a demo app. It is basically the app that was presented
in http://compiletoi.net/quick-authentication-on-pyramid-with-persona.html.

To run it, you'll need pyramid, pyramid_persona and waitress.

The button integration example is a /.
The forbidden view example is at /restricted.
"""

from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.security import authenticated_userid
from pyramid.exceptions import Forbidden

def restricted(request):
    userid = authenticated_userid(request)
    if userid is None:
        raise Forbidden()
    return Response('Hello %s!' % (userid,))

def template(request):
    userid = authenticated_userid(request)
    return {'user': userid}


if __name__ == '__main__':
    settings = {
        'persona.secret': 'some secret',
        'persona.audiences': 'http://localhost:8080',
        'mako.directories': '.',
        'persona.siteName': 'Super demo app',
        'persona.privacyPolicy': '/nonExistentPrivacy.html',
        'persona.termsOfService': '/nonExistentTos.html',
    }
    config = Configurator(settings=settings)
    config.include('pyramid_persona')
    config.add_route('restricted', '/restricted')
    config.add_view(restricted, route_name='restricted')
    config.add_route('template', '/')
    config.add_view(template, route_name='template', renderer='hello.mako')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
