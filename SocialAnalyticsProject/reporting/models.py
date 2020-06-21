from django.db import models
from landing.models import *
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class FacebookPage(models.Model):
    page_id = models.CharField(max_length=2048,unique=True)
    account = models.ForeignKey(SocialAccount,on_delete=models.CASCADE)
    access_token = models.CharField(max_length=2048)
    name =  models.CharField(max_length=248)

    def __str__(self):
        return self.name
    

class FacebookPost(models.Model):
    
    created_time= models.DateTimeField()
    content = models.CharField(max_length=2048)
    week_day = models.IntegerField(null=True)
    hour = models.IntegerField(null=True)
    post_type = models.IntegerField(null=True)
    post_id = models.CharField(max_length=2048, unique=True)
    page = models.ForeignKey(FacebookPage,on_delete=models.CASCADE)

class FacebookComment(models.Model):
    
    created_time= models.DateTimeField()
    content = models.CharField(max_length=2048)
    comment_id = models.CharField(max_length=2048, unique=True)
    post = models.ForeignKey(FacebookPost,on_delete=models.CASCADE)


class InstagramPost(models.Model):
    content = models.CharField(max_length=2048)
    date = models.DateField()

class InstagramReport(models.Model):
    impressions = models.IntegerField()
    engagement = models.IntegerField()
    date = models.DateField()
    post = models.ForeignKey(InstagramPost,on_delete=models.CASCADE)


class FacebookPostReport(models.Model):
    reactions = models.IntegerField(default=0)
    reach = models.IntegerField(default=0)
    impressions = models.IntegerField()
    engagement = models.IntegerField()
    sentiment = JSONField(null=True)
    date = models.DateField()
    post = models.OneToOneField(FacebookPost,on_delete=models.CASCADE)

class FacebookPageReport(models.Model):
    impressions = models.IntegerField()
    engagement = models.IntegerField()
    date = models.DateField()
    page = models.ForeignKey(FacebookPage,on_delete=models.CASCADE)


class UserPreferences(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    business_category = models.CharField(max_length=128)
    fav_page = models.ForeignKey(FacebookPage,on_delete=models.CASCADE)

