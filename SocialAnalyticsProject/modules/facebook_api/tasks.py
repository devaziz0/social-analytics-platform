from celery import shared_task
from modules.utils.urls import *
from allauth.socialaccount.models import SocialToken
from reporting.models import *

@shared_task
def page_engagement_task(user_pk):

    get_page_insights()