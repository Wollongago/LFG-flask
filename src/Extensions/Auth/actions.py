from pprint import pprint

from flask import _request_ctx_stack, request, session

from . import models as auth_models
from .session import get_identifiers


def login(user, device=None, secure=True, auth_type='cookie'):
    """

    :param user: User model
    :param device: Device model, can be None
    :param secure: is this session secure ?
    :param auth_type: How we will send JWT token, by cookie, or by header
    :return:
    """

    # Determine the leading model, basicaly which model contains JWT token
    # TODO:not implemented yet
    # master = user if device is None else device

    # if master.anonymous:
    #     return False

    session['secure'] = secure  # After login, session bacome secure for some time, or until IP or user agent changes.
    # TODO: not implemented yet
    # session['jwt_identity'] = master.jwt_identity
    session['login_ua'], session['login_ip'] = get_identifiers(request)
    session['auth_type'] = auth_type

    # Updating request context
    ctx = _request_ctx_stack.top
    ctx.device = device
    ctx.user = user

    return True

def logout(model, anon_device=None, anon_user=None):

    if not model.anonymous:
        model.logout()

        # Update ctx stack with anonymous models
        ctx = _request_ctx_stack.top
        if anon_device is None:
            ctx.device = auth_models.Device()
        else:
            ctx.device = anon_device

        if anon_user is None:
            ctx.user = auth_models.User()
        else:
            ctx.user = anon_user

    if 'jwt_identity' in session:
        del session['jwt_identity']

    return True