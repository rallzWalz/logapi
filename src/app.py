#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 12:17:03 2022

sources consulted:
https://github.com/iliasmansouri/flask-swagger-template
https://github.com/iliasmansouri/flask-swagger-template/blob/main/back_end/run.py
https://flask.palletsprojects.com/en/2.2.x/logging/
https://gist.github.com/kapb14/87255efffa173bb76cf5c1ed9db1d047
stackoverflow

@author: rall Walsh
Copyright Rall Walsh 2022
"""

from flask import Flask, request
import logging
import os
from logging.config import dictConfig
import json


root = os.path.dirname(os.path.abspath(__file__))
print('root=, ', root)
logdir = os.path.join(root, 'logs')
if not os.path.exists(logdir):
    os.mkdir(logdir)
log_file = os.path.join(logdir, 'logs.txt')


logging.basicConfig(filename=log_file,
                level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


app = Flask(__name__)


@app.before_first_request
def before_first_request():
    log_level = logging.INFO

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)

    root = os.path.dirname(os.path.abspath(__file__))
    # print('root=, ', root)
    logdir = os.path.join(root, 'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    log_file = os.path.join(logdir, 'logs.txt')
    # print('log_file=', log_file)
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    app.logger.addHandler(handler)

    app.logger.setLevel(log_level)



@app.route('/api/log', methods=['POST', 'GET'])
def log_msg():
    if request.method == 'POST':
        body = request.get_json()
        msgs = dict(body).get('logEntries', [])
        for amsg in msgs:  # loop over messages
            app.logger.info(amsg)
        return '200 success'
    else:  # assume get if not post
        print('was a get')
        respdata = ''
        numlines = int(request.args.get('num_lines', 10))
        with open(log_file, 'r') as file:
            # loop to read iterate
            # last n lines and print it
            # https://www.geeksforgeeks.org/python-reading-last-n-lines-of-a-file/
            for line in (file.readlines() [-numlines:]):
                respdata += line
        resp = {"Status": 200,
                "Data": respdata}
    return json.dumps(resp)




if __name__ == '__main__':
    logging.info("Starting API...")
    app.run(
        host="0.0.0.0",
        port=os.environ.get("PORT", 8080),
        debug=False,
        use_reloader=True,
    )
