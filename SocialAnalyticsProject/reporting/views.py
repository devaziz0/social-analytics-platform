from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
import requests
from modules.schedules.tasks import *
from modules.facebook_api.tasks import engagement_growth_task, page_engagement_task
from django.http import JsonResponse
from modules.utils.constants import *
from modules.utils.news import *
from modules.sentiment_analysis.sentiment_urls import predict_multiple_comments

# Create your views here.

def get_insight(request):
    #user = request.user
    #
    #token = SocialToken.objects.get(account__user = user)
    #
    #url = "https://graph.facebook.com/v6.0/me/accounts"
    #
    #PARAMS = {'access_token':token}
    # r = requests.get(url = url, params = PARAMS)
    # extracting data in json format
    # data = r.json()
    # page_engagement_task.delay(request.user.pk)


def get_engagement(request, page_pk, date_preset):
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, date_preset)
    result = t.wait(timeout=None, interval=0.5)
    return JsonResponse(data=result, safe=False)

# Compares the engagement of the past 28 days with the engagement on the same period last month


def get_28days_monthly_growth(request, page_pk):
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'this_month')
    this_month = t.wait(timeout=None, interval=0.5)
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'last_month')
    last_month = t.wait(timeout=None, interval=0.5)
    this_month_value = this_month['data'][2]['values'][0]['value']
    last_month_value = last_month['data'][2]['values'][0]['value']
    result = {
        "growth": this_month_value - last_month_value
    }
    return JsonResponse(data=result, safe=False)

# Compares the engagement of this week with the engagement on the same week last month


def get_1week_monthly_growth(request, page_pk):
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'this_month')
    this_month = t.wait(timeout=None, interval=0.5)
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'last_month')
    last_month = t.wait(timeout=None, interval=0.5)
    this_month_value = this_month['data'][1]['values'][0]['value']
    last_month_value = last_month['data'][1]['values'][0]['value']
    result = {
        "growth": this_month_value - last_month_value
    }
    return JsonResponse(data=result, safe=False)

# Compares the engagement of today with the engagement on the same day last month


def get_1day_monthly_growth(request, page_pk):
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'this_month')
    this_month = t.wait(timeout=None, interval=0.5)
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'last_month')
    last_month = t.wait(timeout=None, interval=0.5)
    this_month_value = this_month['data'][0]['values'][0]['value']
    last_month_value = last_month['data'][0]['values'][0]['value']
    result = {
        "growth": this_month_value - last_month_value
    }
    return JsonResponse(data=result, safe=False)

# Compares the engagement of today with the engagement of yesterday


def get_1day_daily_growth(request, page_pk):
    t = engagement_growth_task.delay(page_pk, METRIC_POST_ENGAGEMENTS, 'today')
    today = t.wait(timeout=None, interval=0.5)
    t = engagement_growth_task.delay(
        page_pk, METRIC_POST_ENGAGEMENTS, 'yesterday')
    yesterday = t.wait(timeout=None, interval=0.5)
    today_value = today['data'][0]['values'][0]['value']
    yesterday_value = yesterday['data'][0]['values'][0]['value']
    result = {
        "growth": today_value - yesterday_value
    }
    return JsonResponse(data=result, safe=False)


# Compares the engagement of today with the engagement of yesterday
def get_top_headlines_category(request, category):
    data = top_headlines_category(category)
    result = {
        "source": data['articles'][0]['source']['name']
    }
    return JsonResponse(data=result, safe=False)


def get_post_sentiment(request, post_id):
    facebook_comment_list = list(FacebookComment.objects.filter(
        post__pk=post_id).values_list('content', flat=True))

    data = predict_multiple_comments(facebook_comment_list)

    return JsonResponse(data=data, safe=False)
