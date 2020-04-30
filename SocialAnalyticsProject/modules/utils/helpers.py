import datetime


def get_page_post_helper(data,facebook_page):
    from reporting.models import FacebookPost
    for post in data['data']:
        try:
            facebook_post = FacebookPost.objects.create(content=post['message'],post_id=post['id'],page=facebook_page,created_time=datetime.datetime.now())
            facebook_post.save()
        except:
            pass