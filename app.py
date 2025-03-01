#!/usr/bin/python3
""" main end point """

from flask import Flask, make_response, jsonify, request, render_template, make_response
from endpoints import app_views
from models.connection import obj
import re


app = Flask(__name__)
app.register_blueprint(app_views)



@app.errorhandler(404)
def not_found(error):
    """ handler for 404 errors """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
