from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
# Create your models here.

class FacebookPage(models.Model):
    page_id = models.CharField(max_length=2048,unique=True)
    account = models.ForeignKey(SocialAccount,on_delete=models.CASCADE)
    access_token = models.CharField(max_length=2048)
    name =  models.CharField(max_length=248)