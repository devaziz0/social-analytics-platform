from django.db import models
from landing.models import *
# Create your models here.
class FacebookPost(models.Model):
    content = models.CharField(max_length=2048)
    date = models.DateField()

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
