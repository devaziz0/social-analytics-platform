from .constants import *
import requests

def add_access_token(url, access_token):

    PARAMS = {"access_token": access_token}
    r = requests.get(url = url, params = PARAMS) 

    return r


def get_page_insights(object_id,metrics,access_token):

    url = URL_BASE_FACEBOOK+ object_id + URL_PAGE_INSIGHTS + '?metric='
    for metric in metrics:
        url += '{' + metric + '},'
    
    data = access_token(url,access_token)

    return data.json()


def get_pages_list(access_token):
    
    url = URL_BASE_FACEBOOK+ URL_PAGE_LIST

    data = add_access_token(url,access_token)

    return data.json()