# -*- coding:utf-8 -*-
__author__ = 'sh84.ahn@gmail.com'

import traceback

from flask import Flask
from flask import redirect
from flask import url_for
from flask import session
from flask import request
from flask import make_response
from flask import jsonify
from flask import render_template

from commons.conf import Conf
_conf = Conf.create_conf("config.json")

app = Flask(__name__, static_url_path="", static_folder="bower_components")
app.config.update(
    DEBUG=True,
    SECRET_KEY=_conf.membership.key
)

#HTTP_METHOD
GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'
HEAD = 'HEAD'

import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
file_handler = TimedRotatingFileHandler(filename="./logs/arale.log", when="D", interval=1, encoding="utf-8")
file_handler.setFormatter(Formatter("[%(process)d:%(processName)s:%(thread)d:%(threadName)s] %(asctime)s : %(message)s [in %(filename)s:%(lineno)d]"))
logger = logging.getLogger('arale_logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

# Membership Setting
from commons.membership import *
init_membership(flask_app=app,
                url=_conf.membership.url,
                decrypt={'crypto':'AES',
                         'key':_conf.membership.key},
                cookie={'field':'AUTH',
                        'logout_field':[{'field_name': 'AUTH'}]
                },
                callback={
                    'url':_conf.membership.callback_url,
                    'field':'returnurl',
                    'etc':[]
                }
)