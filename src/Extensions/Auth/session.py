import random
import string
from datetime import datetime, timedelta, timezone
from hashlib import sha512
from pprint import pformat

import jwt
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict


class JWTSession(CallbackDict, SessionMixin):
    """
    Baseclass for client-side sessions.

    """

    def __init__(self, payload=None):
        def on_update(self):
            self.modified = True

        if payload is None:
            payload = {}
        if 'sid' not in payload:
            payload['sid'] = ''.join(
                random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))

        CallbackDict.__init__(self, payload, on_update)
        self.modified = False

        # self.should_be_terminated = False
        # self.secure = False
        # self.auth_type = None
        # if payload and 'secure' in payload:
        #     self.secure = payload['secure']
        #     del payload['secure']
        # if payload and 'auth_type' in payload:
        #     self.auth_type = payload['auth_type']
        #     del payload['auth_type']

        # def terminate(self):
        #     self.should_be_terminated = True


class JWTSessionInterface(SessionInterface):
    """
    We Only needed that to pass context
    """

    # serializer = pickle
    session_class = JWTSession
    debug = False
    omit_session_saving = False

    def __init__(self, app):
        self.secret_key = app.config['SECRET_KEY']

        self.session_protection_mode = app.config['SESSION_PROTECTION']

        self.jwt_algorithm = app.config['JWT_ALGORITHM']
        self.jwt_expiration = app.config['JWT_EXPIRATION_DELTA']
        self.jwt_delta_secure = app.config['JWT_SECURE_DELTA']
        self.jwt_algorithm = app.config['JWT_ALGORITHM']
        self.jwt_issuer = app.config['JWT_ISSUER']
        self.jwt_audience = app.config['JWT_AUDIENCE']
        self.jwt_leeway = app.config['JWT_LEEWAY']
        self.jwt_cookie_name = app.config['JWT_COOKIE_NAME']

    def _print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def open_session(self, app, request):
        self._print('[SI] Open session')
        config = app.config
        cookie_name = config.get('JWT_COOKIE_NAME')
        header_name = config.get('JWT_HEADER_NAME')
        _payload = None
        if cookie_name in request.cookies:
            _payload = self._payload_from_jwt(request.cookies[cookie_name], request=request)
            if _payload:
                _payload['auth_type'] = 'cookie'
        elif header_name in request.headers:
            jwt_tag = config.get('JWT_HEADER_TAG') + ' '
            if jwt_tag in request.headers[header_name]:
                jwt_header = request.headers[header_name].split(jwt_tag)[1].strip()
                _payload = self._payload_from_jwt(jwt_header, request=request)
                if _payload:
                    _payload['auth_type'] = 'header'
        self._print('[SI] Payload:\n%s' % pformat(_payload))
        return self.session_class(payload=_payload)

    def _payload_from_jwt(self, jwt_encoded, request, verify_exp=True):
        """

        :param jwt_encoded:
        {
            jwt_identity: search by that string inside your DB.
            remember: true\false, allow to use expired tokens.
            _ip : User IP address, which was used for login.
            _ua : User User-Agent filed, which was used for login.
        }
        :return:
        """
        try:
            payload = jwt.decode(jwt_encoded,
                                 self.secret_key,
                                 algorithms=[self.jwt_algorithm],
                                 issuer=self.jwt_issuer,
                                 leeway=self.jwt_leeway,
                                 audience=self.jwt_audience,
                                 options={'verify_exp': verify_exp})
        except jwt.ExpiredSignatureError:
            self._print('[SI] Expired signature')
            payload = None
        except jwt.InvalidIssuerError:
            self._print('[SI] Invalid issuer')
            payload = None
        except jwt.InvalidAudienceError:
            self._print('[SI] Invalid Audience')
            payload = None
        except jwt.InvalidIssuedAtError:
            self._print('[SI] Invalid Issued At')
            payload = None
        except jwt.DecodeError:
            self._print('[SI] Decode error')
            payload = None

        # Session protection for authorized users.
        if payload is not None and 'jwt_identity' in payload:
            mode = self.session_protection_mode

            # Check time betwen last request and current one
            delta_secure = datetime.now(tz=timezone.utc) - datetime.fromtimestamp(payload['iat']).replace(
                tzinfo=timezone.utc)
            if delta_secure > self.jwt_delta_secure:
                self._print('[SI] Session isn\'t secure because we exceeded secure delta')
                payload['secure'] = False

            # Session protection mode
            # basic - check UA and IP, make session insecure.
            # strong - drop session on differ UA nad IP
            current_ua, current_ip = get_identifiers(request)
            if mode == 'basic':
                if current_ip != payload['login_ip'] or current_ua != payload['login_ua']:
                    # Invalid ip\ua, set as non secure
                    payload['secure'] = False
            elif mode == 'strong':
                current_ua, current_ip = get_identifiers(request)
                if current_ip != payload['login_ip'] or current_ua != payload['login_ua']:
                    # Invalid ip\ua, can't trust, drop payload.
                    payload = None

        return payload

    def save_session(self, app, session, response):
        """
        if All k, we will slide jwt session for another period.
        :param app: Flask instance
        :param session: JWTSession
        :param response: Flask response Object
        :return:
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)

        if self.omit_session_saving:
            self._print('[SI] Omit session commit')
            self.omit_session_saving = False
            if session['auth_type'] == 'cookie':
                self._print('[SI] Removing of cookie.')
                response.delete_cookie(self.jwt_cookie_name,
                                       domain=domain,
                                       path=path)
            return

        # Delete case.  If there is no session we bail early.
        # If the session was modified to be empty we remove the
        # whole cookie.
        self._print('[SI] Trying to save session: %s' % session)
        if not session:
            # No need to store empty session in browser i guess.
            self._print('[SI] No session %s' % session)
            self._print('[SI] Session modified %s' % session.modified)
            if session.modified:
                # If session is empty and modified, that means we should remove it from browser.
                self._print('[SI] Remove cookie')
                response.delete_cookie(self.jwt_cookie_name,
                                       domain=domain,
                                       path=path)
            return

        # Setup session
        session['exp'] = datetime.now(tz=timezone.utc) + self.jwt_expiration
        session['iat'] = datetime.now(tz=timezone.utc)
        session['iss'] = self.jwt_issuer
        session['aud'] = self.jwt_audience
        session['auth_type'] = 'cookie' if 'auth_type' not in session else session['auth_type']

        self._print('[SI] Encode new session: %s' % session)
        val = jwt.encode(session, self.secret_key, algorithm=self.jwt_algorithm)

        if session['auth_type'] == 'cookie':
            # Setup cookie configurations
            httponly = self.get_cookie_httponly(app)
            cookie_secure = self.get_cookie_secure(app)

            response.set_cookie(self.jwt_cookie_name, val,
                                expires=datetime.utcnow() + self.jwt_expiration,
                                httponly=httponly,
                                domain=domain,
                                path=path,
                                secure=cookie_secure,
                                samesite='Lax'
                                )
        elif session['auth_type'] == 'header':
            response.headers[app.config.get('JWT_HEADER_NAME')] = '%s %s' % (app.config.get('JWT_HEADER_TAG'),
                                                                             val.decode('utf-8'))

    def generate_jwt_from_session(self, session) -> str:
        """
        Will generate JWT token on demand.
        But it having consequences, you will NOT get token from header or cookie after that.
        So be sure to send it somehow.
        I guess you know what you are doing.
        :return:
        """
        self._print('[SI] Generate JWT token from existing session: {!r}'.format(session))
        # self._print('[SI]\n{!s}'.format(pformat(dir(session))))
        # Setup session
        session = dict(session)  # Copy Session object, because it was thread save proxied.
        session['exp'] = datetime.now(tz=timezone.utc) + self.jwt_expiration
        session['iat'] = datetime.now(tz=timezone.utc)
        session['iss'] = self.jwt_issuer
        session['aud'] = self.jwt_audience

        self._print('[SI] Encode session:\n{!s}'.format(pformat(session)))
        jwt_token = jwt.encode(dict(session), self.secret_key, algorithm=self.jwt_algorithm).decode('utf-8')

        self.omit_session_saving = True
        return jwt_token


def get_identifiers(request):
    user_agent = request.headers.get('User-Agent')
    if user_agent is not None:
        user_agent = user_agent.encode('utf-8')
    user_agent_base = '{0}'.format(user_agent)
    user_ip_base = '{0}'.format(_get_remote_addr(request))
    # h = sha512()
    # hex_ua = h.update(user_agent_base.encode('utf8')).hexdigest()
    # hex_ip = h.update(user_ip_base.encode('utf8')).hexdigest()
    return user_agent_base, user_ip_base


def _get_remote_addr(request):
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        # An 'X-Forwarded-For' header includes a comma separated list of the
        # addresses, the first address being the actual remote address.
        address = address.encode('utf-8').split(b',')[0].strip()
    return address
