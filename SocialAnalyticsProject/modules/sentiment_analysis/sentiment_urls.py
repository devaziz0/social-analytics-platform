from .constants import *
import requests


def predict_multiple_comments(comments_list):

    url = BASE_SENTIMENT_URL + URL_PREDICT_MULTIPLE
    r = requests.post(url, json=comments_list)

    data = r.json()

    return data
