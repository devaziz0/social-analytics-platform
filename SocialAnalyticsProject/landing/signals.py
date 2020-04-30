from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from modules.utils.urls import get_pages_list,get_page_posts
from modules.utils.helpers import get_page_post_helper


@receiver(pre_social_login)
def social_login_handler(sender, **kwargs):
    from .models import FacebookPage  # or...
    from reporting.models import FacebookPost
    

    social_account = kwargs['sociallogin'].account
    pages_list = get_pages_list(kwargs['sociallogin'].token.token)
    

    facebook_page_list = FacebookPage.objects.filter(account=social_account)
    
    for page in pages_list['data']:
        
            facebook_page = FacebookPage.objects.create(
                    account=social_account, page_id=page['id'], access_token=page['access_token'], name=page['name'])
            facebook_page.save()

            data = get_page_posts(facebook_page.page_id,facebook_page.access_token)

            get_page_post_helper(data,facebook_page)
