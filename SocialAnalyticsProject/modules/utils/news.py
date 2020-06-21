# d05ac5fb39264b84a4fb046c25467800

import requests 
  
# Endpoint Top Headlines
url_top_headlines = 'http://newsapi.org/v2/top-headlines'
  
# Params 
apiKey = 'd05ac5fb39264b84a4fb046c25467800'
language = 'en'
country = 'us'
# defining a params dict for the parameters to be sent to the API 
  
# Method to get top headlines per category
# Possible options: business entertainment general health science sports technology . 
# Default: all categories. 
def top_headlines_category(category):
    PARAMS = {
        'category': category,
        'language': language,
        'country': country,
        'apiKey': apiKey,
        }

    r = requests.get(url = url_top_headlines, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()
    return data  

# Method to get top headlines per keyword
# Not all keywords get results, some will get none
def top_headlines_keyword(keyword):
    PARAMS = {
        'language': language,
        'country': country,
        'q': keyword,
        'apiKey': apiKey,
        }

    r = requests.get(url = url_top_headlines, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()
    return data
