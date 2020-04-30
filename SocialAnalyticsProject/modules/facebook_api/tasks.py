from celery import shared_task
from modules.utils.urls import *
from modules.utils.constants import *
from modules.utils.helpers import *


from allauth.socialaccount.models import SocialToken
from reporting.models import *
from landing.models import *



@shared_task
def page_impressions_task(page_pk,start_date,end_date):
    
    facebook_page = FacebookPage.objects.get(pk=page_pk)

    daily_impressions = get_page_insights(facebook_page.page_id, [METRIC_PAGE_IMPRESSIONS],facebook_page.access_token,start_date,end_date)

    facebook_report = FacebookPageReport.objects.get(date=start_date)
    facebook_report.impressions = daily_impressions
    facebook_report.save()

    return daily_impressions

@shared_task
def page_engagement_task(page_pk,start_date,end_date):
    
    facebook_page = FacebookPage.objects.get(pk=page_pk)

    engagement = get_page_insights(facebook_page.page_id, [METRIC_ENGAGED_USERS],facebook_page.access_token,start_date,end_date)

    facebook_report = FacebookPageReport.objects.get(date=start_date)
    facebook_report.engagement = engagement
    facebook_report.save()

    return engagement

@shared_task
def page_posts_task(page_pk):
    
    facebook_page = FacebookPage.objects.get(pk=page_pk)

    data = get_page_posts(facebook_page.page_id, facebook_page.access_token)

    get_page_post_helper(data,facebook_page)

    return data