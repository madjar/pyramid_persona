import logging
import pkg_resources
from pyramid.httpexceptions import HTTPBadRequest, HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget
import browserid.errors


logger = logging.getLogger(__name__)


def verify_login(request):
    """Verifies the assertion and the csrf token in the given request.

    Returns the email of the user if everything is valid, otherwise raises
    a HTTPBadRequest"""
    verifier = request.registry['persona.verifier']
    try:
        data = verifier.verify(request.POST['assertion'])
    except (ValueError, browserid.errors.TrustError) as e:
        logger.info('Failed persona login: %s (%s)', e, type(e).__name__)
        raise HTTPBadRequest('Invalid assertion')
    return data['email']


def login(request):
    """View to check the persona assertion and remember the user"""
    email = verify_login(request)
    headers = remember(request, email)
    return HTTPFound(request.POST['came_from'], headers=headers)


def logout(request):
    """View to forget the user"""
    headers = forget(request)
    return HTTPFound(request.POST['came_from'], headers=headers)


def forbidden(request):
    """A basic 403 view, with a login button"""
    template = pkg_resources.resource_string('pyramid_persona', 'templates/forbidden.html').decode()
    html = template % {'js': request.persona_js, 'button': request.persona_button}
    return Response(html, status='403 Forbidden')
