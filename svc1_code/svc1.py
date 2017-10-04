#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import datetime, logging
from logging import handlers
from elasticsearch import Elasticsearch


from config_loader import load_config
from es_conn import *

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.debug = True

LOG_FILENAME = 'app_access_logs.log'

app.logger.setLevel(logging.DEBUG) # use the native logger of flask or INFO

handler = handlers.RotatingFileHandler(
    LOG_FILENAME,
    maxBytes=1024 * 1024 * 100,
    backupCount=20
    )

app.logger.addHandler(handler)

es = conn()


@app.route("/")
def hello():
    message = "Contact established"
    return message

@app.route("/v1/api/populate", methods=['POST'])
def populate():
    
    app.logger.debug("JSON received...")
    app.logger.debug(request.json)
    
    if request.json:
        mydata = request.json # will be 

        try:
            es.index(index='sw', doc_type='people', body=mydata)
        except Exception as esex:
            print("ES insert error: ", esex)
            return esex

        
        return "Thanks. Data uploaded"
    else:
        return "no json received"

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)

@app.before_request
def pre_request_logging():
    #Logging statement
    # if 'text/html' in request.headers['Accept']:
    app.logger.info('\t'.join([
        datetime.datetime.today().ctime(),
        request.remote_addr,
        request.method,
        request.url,
        # str(request.data,
        # ', '.join([': '.join(x) for x in request.headers])]
        ])
    )