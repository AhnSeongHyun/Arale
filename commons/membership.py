# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

from arale_base import app
from arale_base import request
from arale_base import make_response
from arale_base import redirect
from arale_base import logger

import json
from flask_login import LoginManager
from flask_login import current_user as current_member
from flask_login import login_required
from flask_login import logout_user
from flask_login import UserMixin

_login_manager = LoginManager()
_sso = None

def init_membership(flask_app, url, decrypt, cookie, callback):
    if not(flask_app or url or decrypt or cookie or callback):
        raise Exception('need params for membership ')
    global _login_manager, _sso
    _login_manager.init_app(flask_app)
    _sso = SSO(login_url=url, callback=callback, cookie=cookie, decrypt=decrypt)


def _decrypt_token(cookie_value):
    try:
        if not cookie_value:
            raise Exception('need params for membership ')

        raw = None
        if _sso.decrypt_crypto.upper() == "AES":
            from commons.aes256 import AESCipher
            aes = AESCipher(_sso.decrypt_key)
            decrypt_cookie_value = aes.decrypt(cookie_value)
            raw = decrypt_cookie_value
        else:
            raise Exception('another decryption is not implement')

        if raw:
            return json.loads(raw)

    except Exception as e:
        logger.exception(e)
        raise e


@_login_manager.request_loader
def load_user_from_cookie(request):
    try:
        cookie_value = request.cookies.get(_sso.cookie_field)
        if cookie_value:
            auth_info = _decrypt_token(cookie_value)
            print auth_info
            if auth_info:
                return Member(auth_info)
            else:
                return None
        else:
            return None
    except Exception as e:
        logger.exception(e)
        return None


@_login_manager.unauthorized_handler
def unauthorized():
    return redirect(_sso.login_url)

def logout_member():
    try:
        logout_user()
        response = make_response(redirect(_sso.login_url))
        for logout_cookie_filed in _sso.logout_cookie_fields:
            response.set_cookie(key=unicode(logout_cookie_filed['field_name']), value=u'', path='/')

        return response
    except Exception as e:
        logger.exception(e)
        raise e


class SSO(object):
    _login_url = None
    _cookie = None
    _callback = None
    _decrypt = None

    def __init__(self, login_url, cookie, decrypt, callback):
        self._login_url = login_url
        self._callback = callback
        self._cookie = cookie
        self._decrypt = decrypt

    @property
    def logout_cookie_fields(self):
        return self._cookie['logout_field']

    @property
    def cookie_field(self):
        return self._cookie['field']

    @property
    def decrypt_key(self):
        return self._decrypt['key']

    @property
    def decrypt_crypto(self):
        return self._decrypt['crypto']


    @property
    def login_url(self):
        if self._callback['field']:
            import urllib
            try:
                import urlparse
            except ImportError:
                from urllib import parse as urlparse

            url_parts = list(urlparse.urlparse(self._login_url))
            query = dict(urlparse.parse_qsl(url_parts[4]))

            if self._callback['url']:
                query.update({self._callback['field']: self._callback['url']})
            else:
                query.update({self._callback['field']: request.url})

            if 'etc' in self._callback:
                for etc in self._callback['etc']:
                    query.update(etc)

            url_parts[4] = urllib.urlencode(query)
            full_url = urlparse.urlunparse(url_parts)
            return full_url
        else:
            return self._login_url


class Member(UserMixin):

    id = None
    user = None
    name = None

    def __init__(self, auth_info):
        self.id = auth_info['id']
        self.user = auth_info['user']
        self.name = auth_info['name']

    def get_id(self):
        return unicode(self.id)

    def __str__(self):
        return "is_active:" + str(self.is_active()) +"\n" + "is_authenticated : "+str(self.is_authenticated())