#!/usr/bin/env python3
# LD_LIBRARY_PATH=./nativec/build/lib.linux-x86_64-3.5 flask run --port 5000

from flask import Flask, render_template, request, jsonify
import datetime, logging
from logging import handlers
from elasticsearch import Elasticsearch

import hello

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
    message = "Contact established." 
    return message

@app.route("/v1/api/search", methods=['GET'])
def retrieve():
    
    app.logger.debug("Search info ...")

    queried_text = request.args.get("q")

    if queried_text == '':
        queried_text = '*'

    app.logger.debug('query is %s' % queried_text)

    lucene_query = queried_text

    serializeddata = []

    try:
        response = es.search(index='sw', doc_type='people', q=lucene_query, size=100)
        # response = es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}})
        # response = es.search(index="sw", body={"query": {"match": {'name':'Darth Vader'}}})
        for hit in response['hits']['hits']:
            serializeddata.append(hit["_source"])
        # print(response)
    except Exception as esex:
        app.logger.error(esex)
        return "Search failure see log"
    
    return jsonify(serializeddata)