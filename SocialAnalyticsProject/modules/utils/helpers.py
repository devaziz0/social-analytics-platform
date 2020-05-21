import datetime

def get_page_post_helper(data,facebook_page):
    from .facebook_urls import get_comments

    from reporting.models import FacebookPost,FacebookComment
    for post in data['data']:
        try:
            facebook_post = FacebookPost.objects.create(content=post['message'],post_id=post['id'],page=facebook_page,created_time=datetime.datetime.now())
            facebook_post.save()
            data_comments = get_comments(post['id'],facebook_page.access_token)

            for comment in data_comments['data']:
                facebook_comment = FacebookComment.objects.create(content=comment['message'],comment_id=comment['id'],post=facebook_post,created_time=datetime.datetime.now())
                facebook_comment.save()
        except:
            pass