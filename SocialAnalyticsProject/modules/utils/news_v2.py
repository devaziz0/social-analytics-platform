# d05ac5fb39264b84a4fb046c25467800

import requests 
  
# Endpoint Top Headlines
url_top_headlines = 'https://gnews.io/api/v3/top-news'

# Endpoint Search
url_search = 'https://gnews.io/api/v3/search'
  
# Params 
token = 'e2c2678a567af772e770481dd5be741a'
lang = 'en'
country = 'us'
# defining a params dict for the parameters to be sent to the API 
  
# Method to get top headlines per category
# Possible options: business entertainment general health science sports technology . 
# Default: all categories. 
def top_headlines_category_v2(category):
    return ''

# Method to get top headlines per keyword
# Not all keywords get results, some will get none
def top_headlines_keyword_v2(keyword):
    PARAMS = {
        'lang': lang,
        'q': keyword,
        'token': token,
        }

    r = requests.get(url = url_search, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()
    return data