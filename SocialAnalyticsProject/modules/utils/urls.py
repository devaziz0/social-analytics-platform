from .constants import *
import requests
import datetime
import calendar

def extract_data(url, access_token):

    PARAMS = {"access_token": access_token}
    r = requests.get(url = url, params = PARAMS) 

    data = r.json()

    value = data['data'][0]['values'][0]['value']

    return value


def get_page_insights(object_id,metrics,access_token,start_date,end_date):

    url = URL_BASE_FACEBOOK+ object_id + URL_PAGE_INSIGHTS + '?metric='
    for metric in metrics:
        url +=  metric + ','
    
    start_timestamp = calendar.timegm(start_date.timetuple())
    end_timestamp = calendar.timegm(end_date.timetuple())

    url+='&since='+str(start_timestamp)
    url+='&until='+str(end_timestamp)



    data = extract_data(url,access_token)

    return data


def get_pages_list(access_token):
    
    url = URL_BASE_FACEBOOK+ URL_PAGE_LIST

    data = add_access_token(url,access_token)

    return data.json()