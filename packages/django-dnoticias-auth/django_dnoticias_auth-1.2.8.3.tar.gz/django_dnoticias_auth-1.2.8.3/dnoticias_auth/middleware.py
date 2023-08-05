import logging
from re import Pattern
from requests.exceptions import HTTPError

from dnoticias_auth.redis import KeycloakSessionStorage
from django.utils.module_loading import import_string
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import BACKEND_SESSION_KEY
from django.utils.functional import cached_property
from django.conf import settings
from django.contrib import auth

from mozilla_django_oidc.middleware import SessionRefresh as SessionRefreshOIDC
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.utils import absolutify

from .utils import generate_oidc_cookies, get_cookie_equivalency
from .backends import ExtraClaimsOIDCAuthenticationBackend

logger = logging.getLogger(__name__)


class BaseAuthMiddleware:
    @cached_property
    def exempt_url_patterns(self):
        exempt_patterns = set()

        for url_pattern in settings.AUTH_EXEMPT_URLS:
            if isinstance(url_pattern, Pattern):
                exempt_patterns.add(url_pattern)

        return exempt_patterns

    def _is_processable(self, request):
        pass


class SessionRefresh(SessionRefreshOIDC):
    def is_refreshable_url(self, request):
        """Takes a request and returns whether it triggers a refresh examination

        :arg HttpRequest request:

        :returns: boolean

        """
        # Do not attempt to refresh the session if the OIDC backend is not used
        backend_session = request.session.get(BACKEND_SESSION_KEY)
        is_oidc_enabled = True
        if backend_session:
            auth_backend = import_string(backend_session)
            is_oidc_enabled = issubclass(auth_backend, OIDCAuthenticationBackend)

        return (
            request.method == 'GET' and
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            request.user.is_authenticated and
            is_oidc_enabled and
            request.path not in self.exempt_urls
        )


class LoginMiddleware(BaseAuthMiddleware, MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def _login_user(self, access_token, id_token, payload, request):
        """
        Ge get or create the user and then proceed to log in
        """
        UserModel = ExtraClaimsOIDCAuthenticationBackend()
        user = None

        try:
            user = UserModel.get_or_create_user(access_token, id_token, payload)
        except HTTPError as e:
            logger.debug("An HTTP error ocurred: {}".format(e))
        except:
            logger.exception("An exception has been ocurred on _login_user")

        if user:
            user.backend = "dnoticias_auth.backends.ExtraClaimsOIDCAuthenticationBackend"
            auth.login(request, user)

            if session_id := request.COOKIES.get(get_cookie_equivalency("keycloak_session_id")):
                keycloak_session = KeycloakSessionStorage(session_id, request.session.session_key)
                keycloak_session.create_or_update()

    def _is_processable(self, request):
        return (
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            not request.user.is_authenticated
        )

    def process_request(self, request):
        if not self._is_processable(request):
            logger.debug("The request is not processable, skipping...")
            return

        cookies = request.COOKIES
        session = request.session

        if not cookies.get(get_cookie_equivalency('oidc_access_token'), None):
            logger.debug("Access token not found in cookie, skipping...")
            return
    
        # Setting the session items from cookies
        session['oidc_id_token_expiration'] = \
            float(cookies.get(get_cookie_equivalency('oidc_id_token_expiration'), 0))
        session['oidc_access_token'] = \
            cookies.get(get_cookie_equivalency('oidc_access_token'), None)
        session['oidc_id_token'] = \
            cookies.get(get_cookie_equivalency('oidc_id_token'), None)
        session['oidc_login_next'] = \
            cookies.get(get_cookie_equivalency('oidc_login_next'), None)

        # This condition avoids the exception 'OIDC callback'
        if not session.get('oidc_states'):
            session['oidc_states'] = \
                cookies.get(get_cookie_equivalency('oidc_states'), {})

        if not all([
            session['oidc_id_token_expiration'],
            session['oidc_access_token'],
            session['oidc_id_token']
        ]):
            return

        # Token payload that is used in OIDC to get (or refresh) an user token
        token_payload = {
            'client_id': settings.OIDC_RP_CLIENT_ID,
            'client_secret': settings.OIDC_RP_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': None,
            'redirect_uri': absolutify(
                request,
                ''
            ),
        }

        self._login_user(
            session['oidc_access_token'],
            session['oidc_id_token'],
            token_payload,
            request
        )

        return


class TokenMiddleware(BaseAuthMiddleware, MiddlewareMixin):
    """
    Just generates the cookie if the user is logged in
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def _is_processable(self, request):
        return (
            not any(pat.match(request.path) for pat in self.exempt_url_patterns) and
            request.user.is_authenticated
        )

    def process_response(self, request, response):
        # If the user is logged in then we set the cookies, else we delete it
        if self._is_processable(request):
            response = generate_oidc_cookies(request.session, response)

        return response
