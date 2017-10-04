import requests
import os
import sys
import json
from elasticsearch import Elasticsearch

def conn():

	es_host=os.environ.get('ES_HOST', 'localhost')
	es_http_port=os.environ.get('ES_HTTP_PORT', '9200')

	print("ES Host: ", es_host)
	print("ES Port: ", es_http_port)

	es_conn_string = 'http://' + es_host + ":" + es_http_port
	print("ES Connnection string: ", es_conn_string)


	try:
		res = requests.get(es_conn_string) #' + es_host + ':' + es_http_port)
	except Exception as e:
		print("ES cannot be reached. Please check env vars ES_HOST and ES_HOST_PORT")
		print(e)
		sys.exit(1)

	es = Elasticsearch([{'host': es_host, 'port': int(es_http_port)}])
	return es

