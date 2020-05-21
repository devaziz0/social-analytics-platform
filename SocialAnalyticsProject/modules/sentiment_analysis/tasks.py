from celery import shared_task
from reporting.models import FacebookComment, FacebookPost
from .sentiment_urls import predict_multiple_comments

# Evaluate post comments through sentiment analysis app
@shared_task
def evaluate_facebook_post(post_pk):

    data = {}

    facebook_comment_list = list(FacebookComment.objects.filter(
        post__pk=post_pk).values_list('content', flat=True))

    if facebook_comment_list != []:
        data = predict_multiple_comments(facebook_comment_list)

    return data
