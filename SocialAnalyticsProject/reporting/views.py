from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
import requests
from modules.schedules.tasks import *
from modules.facebook_api.tasks import *

# Create your views here.


def get_insight(request):

    #user = request.user
#
    #token = SocialToken.objects.get(account__user = user)
    #
    #url = "https://graph.facebook.com/v6.0/me/accounts"
#
    #PARAMS = {'access_token':token} 

    #r = requests.get(url = url, params = PARAMS) 
    ##
    ### extracting data in json format 
    #data = r.json() 
    page_engagement_task.delay(request.user.pk)
