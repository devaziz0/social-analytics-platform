from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(FacebookPageReport)
admin.site.register(FacebookPostReport)
admin.site.register(FacebookPage)
admin.site.register(FacebookPost)
admin.site.register(FacebookComment)