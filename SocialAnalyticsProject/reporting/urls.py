from django.urls import path
from django.conf.urls import url

from . import views
app_name = "reporting"

urlpatterns = [
    path('report/',views.get_insight,name='report'),
    path('pages/<int:page_pk>/engagement/<str:date_preset>',views.get_engagement,name='engagement'),
    path('pages/<int:page_pk>/growth/1day_monthly',views.get_1day_monthly_growth,name='this_month_vas_last_month_growth'),
    path('pages/<int:page_pk>/growth/1week_monthly',views.get_1week_monthly_growth,name='this_month_vas_last_month_growth'),
    path('pages/<int:page_pk>/growth/28days_monthly',views.get_28days_monthly_growth,name='this_month_vas_last_month_growth'),
    path('pages/<int:page_pk>/growth/1day_daily',views.get_1day_daily_growth,name='today_vs_yesterday_growth'),
    path('post/<int:post_id>/predict/',views.get_post_sentiment, name= 'get_post_sentiment')
]