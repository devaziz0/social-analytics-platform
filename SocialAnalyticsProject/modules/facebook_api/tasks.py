from celery import shared_task
from modules.utils.urls import *
from modules.utils.constants import *

from allauth.socialaccount.models import SocialToken
from reporting.models import *
from landing.models import *


@shared_task
def page_engagement_task(page_pk):
    
    facebook_page = FacebookPage.objects.get(pk=page_pk)

    data = get_page_insights(facebook_page.page_id, [METRIC_ENGAGED_USERS,METRIC_POST_ENGAGEMENTS],facebook_page.access_token)

    