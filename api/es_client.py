from elasticsearch import Elasticsearch
from django.conf import settings

def get_es_client():
    es_args = {"hosts": [settings.ELASTICSEARCH_HOST]}
    if settings.ELASTICSEARCH_USER and settings.ELASTICSEARCH_PASSWORD:
        es_args["basic_auth"] = (settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD)
    return Elasticsearch(**es_args)
