# -*- coding: utf-8 -*-

from googletrans import Translator
import wikipediaapi
import json
import requests
# if you are using python 3, you should
import urllib.request


# import urllib2

class SolrConnection:
    def convert_query(self, query):
        translator = Translator()
        detect = translator.detect(query)
        if detect.lang == 'en':
            text_en = query
            text_en = text_en.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_en + ")%0A"
            text_es = translator.translate(query, dest='es')
            text_es = text_es.text
            text_es = text_es.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_es + ")%0A"
            text_hi = translator.translate(query, dest='hi')
            text_hi = text_hi.text
            text_hi = text_hi.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_hi + ")"
        elif detect.lang == 'es':
            text_es = query
            text_es = text_es.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_es + ")%0A"
            text_en = translator.translate(query, dest='en')
            text_en = text_en.text
            text_en = text_en.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_en + ")%0A"
            text_hi = translator.translate(query, dest='hi')
            text_hi = text_hi.text
            text_hi = text_hi.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_hi + ")"
        else:
            text_hi = query
            text_hi = text_hi.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_hi + ")%0A"
            text_en = translator.translate(query, dest='en')
            text_en = text_en.text
            text_en = text_en.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_en + ")%0A"
            text_es = translator.translate(query, dest='es')
            text_es = text_es.text
            text_es = text_es.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_es + ")"

        solr_query = "http://ec2-52-72-185-101.compute-1.amazonaws.com:8983/solr/BM25_Sentiment_Analysis_V1/select?q.op=OR&q=" + query_final + "-poi_name%3A%5B*%20TO%20*%5D&rows=50"
        data = requests.get(solr_query).json()
        return data['response']['docs']

    def convert_query_for_poi(self, query):
        translator = Translator()
        detect = translator.detect(query)
        if detect.lang == 'en':
            text_en = query
            text_en = text_en.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_en + ")%0A"
            text_es = translator.translate(query, dest='es')
            text_es = text_es.text
            text_es = text_es.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_es + ")%0A"
            text_hi = translator.translate(query, dest='hi')
            text_hi = text_hi.text
            text_hi = text_hi.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_hi + ")"
        elif detect.lang == 'es':
            text_es = query
            text_es = text_es.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_es + ")%0A"
            text_en = translator.translate(query, dest='en')
            text_en = text_en.text
            text_en = text_en.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_en + ")%0A"
            text_hi = translator.translate(query, dest='hi')
            text_hi = text_hi.text
            text_hi = text_hi.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_hi + ")"
        else:
            text_hi = query
            text_hi = text_hi.replace(" ", "%20")
            query_final = "tweet_text%3A(" + text_hi + ")%0A"
            text_en = translator.translate(query, dest='en')
            text_en = text_en.text
            text_en = text_en.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_en + ")%0A"
            text_es = translator.translate(query, dest='es')
            text_es = text_es.text
            text_es = text_es.replace(" ", "%20")
            query_final = query_final + "tweet_text%3A(" + text_es + ")"
        query_final = query_final + "AND poi_name: [* TO *]"
        solr_query = "http://ec2-52-72-185-101.compute-1.amazonaws.com:8983/solr/BM25_Sentiment_Analysis_V1/select?q.op=OR&q=" + query_final + "&rows=50"
        data = requests.get(solr_query).json()
        return data['response']['docs']

    def wiki(self, query):
        wiki = wikipediaapi.Wikipedia()
        query = query.replace(" ","_")
        page_py = wiki.page(query)
        if page_py.exists():

            text = page_py.summary[0:6000]
            url = page_py.fullurl
            return text,url
        else:
            return None
