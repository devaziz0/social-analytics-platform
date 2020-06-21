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
    path('growth/page/<int:page_pk>', views.growth_page, name='growth_page'),
    path('news/category/<str:category>', views.get_top_headlines_category, name='get_top_headlines_category'),
    path('news/q/<str:keyword>', views.get_top_headlines_keyword, name='get_top_headlines_keyword'),
    path('news/', views.news_suggestions, name='news_suggestions'),
    path('news/keyword', views.news_suggestions_keyword, name='news_suggestions_keyword'),
    path('post/<int:post_id>/predict/',views.get_post_sentiment, name= 'get_post_sentiment'),
    path('prediction/', views.predict_page, name='predict_page'),
    path('sentiments/', views.sentiments_page, name='sentiments_page'),
    path('related-topics/<str:topic>',views.get_related_topics, name= 'get_related_topics'),
    path('collect-comments/',views.collect_comments_page, name= 'collect_comments_page'),
]