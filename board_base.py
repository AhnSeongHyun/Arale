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


app = Flask(__name__, static_url_path = "", static_folder="bower_components")

#HTTP_METHOD
GET     = 'GET'
POST    = 'POST'
PUT     = 'PUT'
DELETE  = 'DELETE'
HEAD    = 'HEAD'
