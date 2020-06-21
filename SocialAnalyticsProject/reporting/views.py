from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
import requests
from modules.schedules.tasks import *
from modules.facebook_api.tasks import engagement_growth_task, page_engagement_task
from django.http import JsonResponse
from modules.utils.constants import *
from modules.utils.news import *
from modules.utils.news_v2 import *
from modules.utils.trends import *
from modules.sentiment_analysis.sentiment_urls import predict_multiple_comments
from modules.sentiment_analysis.sentiment_urls import predict_multiple_comments

from .models import *


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
    page_engagement_task.delay(request.user.pk)


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
    growth = this_month_value - last_month_value
    if growth>0:
        growth_str = "+" + str(growth)
        ratio = "+" + str(((this_month_value/last_month_value) * 100) - 100)
    else:
        growth_str = str(growth)
        ratio = "-" + str(((last_month_value/this_month_value) * 100) - 100)

    result = {
        "growth": growth_str,
        "current": this_month_value,
        "last": last_month_value,
        "ratio": ratio,
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
    growth = this_month_value - last_month_value
    if growth>0:
        growth_str = "+" + str(growth)
        ratio = "+" + str(((this_month_value/last_month_value) * 100) - 100)
    else:
        growth_str = str(growth)
        ratio = "-" + str(((last_month_value/this_month_value) * 100) - 100)

    result = {
        "growth": growth_str,
        "current": this_month_value,
        "last": last_month_value,
        "ratio": ratio,
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
    growth = this_month_value - last_month_value
    if growth>0:
        growth_str = "+" + str(growth)
        ratio = "+" + str(((this_month_value/last_month_value) * 100) - 100)
    else:
        growth_str = str(growth)
        ratio = "-" + str(((last_month_value/this_month_value) * 100) - 100)

    result = {
        "growth": growth_str,
        "current": this_month_value,
        "last": last_month_value,
        "ratio": ratio,
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
    growth = today_value - yesterday_value
    if growth>0:
        growth_str = "+" + str(growth)
        ratio = "+" + str(((today_value/yesterday_value) * 100) - 100)
    else:
        growth_str = str(growth)
        ratio = "-" + str(((yesterday_value/today_value) * 100) - 100)

    result = {
        "growth": growth_str,
        "current": today_value,
        "last": yesterday_value,
        "ratio": ratio,
    }
    return JsonResponse(data=result, safe=False)

def get_top_headlines_category(request, category):
    data = top_headlines_category(category)
    result = data['articles']
    return JsonResponse(data=result, safe=False)

def get_top_headlines_keyword(request, keyword):
    data = top_headlines_keyword_v2(keyword)
    result = data['articles']
    return JsonResponse(data=result, safe=False)

def get_related_topics(request, topic):
    data = get_related_trending_topics(topic)
    # result = data[topic]['rising']['topic_title']
    result = data[topic]['top']['topic_title'].to_dict()
    return JsonResponse(data=result, safe=False)

def get_post_sentiment(request, post_id):
    facebook_comment_list = list(FacebookComment.objects.filter(
        post__pk=post_id).values_list('content', flat=True))

    data = predict_multiple_comments(facebook_comment_list)

    return JsonResponse(data=data, safe=False)


def news_suggestions(request):
    context = {
        'title': 'News Suggestion',
    }
    return render(request, 'news.html', context)


def news_suggestions_keyword(request):
    context = {
        'title': 'News Suggestion Keyword',
    }
    return render(request, 'keyword_news.html', context)

def growth_choose_page(request):
    context = {
        'title': 'Growth - Choose a page',
    }
    return render(request, 'growth_choose.html', context)
    
def growth_page(request, page_pk):
    context = {
        'title': 'Growth',
        'page_pk': page_pk,
    }
    return render(request, 'growth.html', context)
        
def predict_page(request):
    context = {
        'title': 'Post Prediction',
    }
    return render(request, 'predict.html', context)

def sentiments_page(request):
    context = {
        'title': 'Sentiment Analysis',
    }
    return render(request, 'sentiment.html', context)

def collect_comments_page(request):
    #user_prefs = UserPreferences.objects.get(user=request.user)
    page = FacebookPage.objects.filter(account__user=request.user).first()
    posts = FacebookPost.objects.filter(page=page)
    context = {
        'title': 'Comments Collect',
        'page': page,
        'posts': posts,
    }
    return render(request, 'posts_collect_comments.html', context)

def sync_comments(request,post_id):
    post = FacebookPost.objects.get(pk=post_id,page__account__user=request.user)
    data_comments = get_comments(post['id'],post.page.access_token)

    for comment in data_comments['data']:
        facebook_comment = FacebookComment.objects.create(content=comment['message'],comment_id=comment['id'],post=facebook_post,created_time=datetime.datetime.now())
        facebook_comment.save()
    
    return JsonResponse(data={"message": "success"})

def growth_default_page(request):
    return None
