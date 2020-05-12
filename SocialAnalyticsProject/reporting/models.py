from django.db import models
from landing.models import *
# Create your models here.

class FacebookPost(models.Model):
    
    created_time= models.DateTimeField()
    content = models.CharField(max_length=2048)
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
    impressions = models.IntegerField()
    engagement = models.IntegerField()
    date = models.DateField()
    post = models.ForeignKey(FacebookPost,on_delete=models.CASCADE)

class FacebookPageReport(models.Model):
    impressions = models.IntegerField()
    engagement = models.IntegerField()
    date = models.DateField()
    page = models.ForeignKey(FacebookPage,on_delete=models.CASCADE)
