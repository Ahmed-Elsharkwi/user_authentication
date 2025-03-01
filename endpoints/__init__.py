#!/usr/bin/python3
""" blue print api """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/app')

from endpoints.user import *
from endpoints.file import *
from endpoints.conversation import *

