# -*- coding: utf-8 -*-

"""
Initialize Flask app

"""
from flask import Flask

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__, static_url_path='')
import views
