# d05ac5fb39264b84a4fb046c25467800

import requests 
  
# Endpoint Top Headlines
url_top_headlines = 'http://newsapi.org/v2/top-headlines'
  
# Params 
apiKey = 'd05ac5fb39264b84a4fb046c25467800'
# defining a params dict for the parameters to be sent to the API 
  
# Method to get top headlines per category
# Possible options: business entertainment general health science sports technology . 
# Default: all categories. 
def top_headlines_category(category):
    PARAMS = {
        'category': category,
        'apiKey': apiKey
        }

    r = requests.get(url = url_top_headlines, params = PARAMS) 
    
    # extracting data in json format 
    data = r.json()
    return data

print(top_headlines_category('health'))