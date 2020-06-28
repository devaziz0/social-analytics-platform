from django.shortcuts import render, redirect, reverse
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
from modules.utils.facebook_urls import *


from .models import *

def get_user_pages(request):
    user_pages = FacebookPage.objects.filter(account__user=request.user)
    return user_pages

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

    return JsonResponse(data=data, safe=False)


def news_suggestions(request):
    context = {
        'title': 'News Suggestion',
        'user_pages': get_user_pages(request),
    }
    return render(request, 'news.html', context)


def news_suggestions_keyword(request):
    context = {
        'title': 'News Suggestion Keyword',
        'user_pages': get_user_pages(request),
    }
    return render(request, 'keyword_news.html', context)

def growth_choose_page(request):
    context = {
        'title': 'Growth - Choose a page',
        'user_pages': get_user_pages(request),
    }
    return render(request, 'growth_choose.html', context)
    
def growth_page(request, page_pk):
    context = {
        'title': 'Growth',
        'page_pk': page_pk,
        'user_pages': get_user_pages(request),
    }
    return render(request, 'growth.html', context)
        
def predict_page(request):
    context = {
        'title': 'Post Prediction',
        'user_pages': get_user_pages(request),
    }
    return render(request, 'predict.html', context)

def sentiments_page(request,post_id):
    post = FacebookPost.objects.get(pk=post_id,page__account__user=request.user)

    post_report = FacebookPostReport.objects.get(post=post)

    if post_report.sentiment == None:

        facebook_comment_list = list(FacebookComment.objects.filter(
            post=post).values_list('content', flat=True))

        data = predict_multiple_comments(facebook_comment_list)

        post_report.sentiment = data
        post_report.save()

    else:
        data = post_report.sentiment

    context = {
        'title': 'Sentiment Analysis',
        "data": data,
        'user_pages': get_user_pages(request),
    }
    return render(request, 'sentiment.html', context)

def collect_comments_page(request):
    try:
        user_prefs = UserPreferences.objects.get(user=request.user)
    except:
        # We take the first page in case there is no user prefs
        page = FacebookPage.objects.filter(account__user=request.user).first()
        user_prefs = UserPreferences(
            user=request.user,
            fav_page=page,
            business_category='',
            )
        user_prefs.save()
    page = user_prefs.fav_page
    posts = FacebookPost.objects.filter(page=page).order_by('-pk')
    context = {
        'title': 'Comments Collect',
        'page': page,
        'posts': posts,
        'user_pages': get_user_pages(request),
    }
    return render(request, 'posts_collect_comments.html', context)

def sync_comments(request,post_id):
    post = FacebookPost.objects.get(pk=post_id,page__account__user=request.user)
    
    if not post.comments_synced:
        
        data_comments = get_comments(post.post_id,post.page.access_token)

        for comment in data_comments['data']:
            facebook_comment = FacebookComment.objects.create(content=comment['message'],comment_id=comment['id'],post=post,created_time=datetime.datetime.now())
            facebook_comment.save()

        post.nb_comments = len(data_comments['data'])
        post.comments_synced = True

        post.save()

    return redirect(reverse('reporting:collect_comments_page'))

def growth_default_page(request):
    try:
        user_prefs = UserPreferences.objects.get(user=request.user)
    except:
        # We take the first page in case there is no user prefs
        page = FacebookPage.objects.filter(account__user=request.user).first()
        user_prefs = UserPreferences(
            user=request.user,
            fav_page=page,
            business_category='',
            )
        user_prefs.save()
    page = user_prefs.fav_page
    context = {
        'title': 'Growth',
        'page_pk': page.pk,
        'user_pages': get_user_pages(request),
    }
    return render(request, 'growth.html', context)

def change_fav_page(request):
    new_pk = POST['pk']
    new_page = FacebookPage.objects.get(pk=new_pk)
    user_prefs = UserPreferences.objects.get(user=request.user)
    user_prefs.page = new_page
    user_prefs.save()
    return JsonResponse(data={"message": "success"}, safe=False)
