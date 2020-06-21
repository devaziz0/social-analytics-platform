from pytrends.request import TrendReq

# Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

# Create payload and capture API tokens. Only needed for interest_over_time(), interest_by_region() & related_queries()

def get_related_trending_topics(topic):
    pytrend.build_payload(kw_list=[topic])

    # Related Topics, returns a dictionary of dataframes
    related_topic_dict = pytrend.related_topics()
    print(related_topic_dict)

    return related_topic_dict