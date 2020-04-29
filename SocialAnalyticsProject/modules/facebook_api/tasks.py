from celery import shared_task
from modules.utils.urls import *
from modules.utils.constants import *

from allauth.socialaccount.models import SocialToken
from reporting.models import *
from landing.models import *


@shared_task
def page_engagement_task(page_pk,start_date,end_date):
    
    facebook_page = FacebookPage.objects.get(pk=page_pk)

    daily_impressions = get_page_insights(facebook_page.page_id, [METRIC_PAGE_IMPRESSIONS],facebook_page.access_token,start_date,end_date)

    facebook_report = FacebookPageReport.objects.get(date=start_date)
    facebook_report.impressions = daily_impressions
    facebook_report.save()

    return daily_impressions