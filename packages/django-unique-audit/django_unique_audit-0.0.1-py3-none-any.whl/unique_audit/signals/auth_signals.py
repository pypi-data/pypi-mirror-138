from django.contrib.auth import signals, get_user_model
from django.db import transaction
from django.utils.module_loading import import_string

from unique_audit.middleware.unique_audit import get_current_request
from unique_audit.models import LoginEvent
from unique_audit.settings import REMOTE_ADDR_HEADER, WATCH_AUTH_EVENTS, LOGGING_BACKEND

audit_logger = import_string(LOGGING_BACKEND)()


def user_logged_in(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            login_event = audit_logger.login({
                'login_type': LoginEvent.LOGIN,
                'user_pk_as_string': str(getattr(user, 'id')),
                'remote_ip': request.META[REMOTE_ADDR_HEADER]
            })
    except:
        pass


def user_logged_out(sender, request, user, **kwargs):
    try:
        with transaction.atomic():
            login_event = audit_logger.login({
                'login_type': LoginEvent.LOGOUT,
                'user_pk_as_string': str(getattr(user, 'id')),
                'remote_ip': request.META[REMOTE_ADDR_HEADER]
            })
    except:
        pass


def user_login_failed(sender, credentials, **kwargs):
    try:
        with transaction.atomic():
            request = get_current_request()  # request argument not available in django < 1.11
            login_event = audit_logger.login({
                'login_type': LoginEvent.FAILED,
                'remote_ip': request.META[REMOTE_ADDR_HEADER]
            })
    except:
        pass


if WATCH_AUTH_EVENTS:
    signals.user_logged_in.connect(user_logged_in, dispatch_uid='unique_audit_signals_logged_in')
    signals.user_logged_out.connect(user_logged_out, dispatch_uid='unique_audit_signals_logged_out')
    signals.user_login_failed.connect(user_login_failed, dispatch_uid='unique_audit_signals_login_failed')
