from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from modules.utils.urls import get_pages_list

@receiver(pre_social_login)
def social_login_handler(sender, **kwargs):
    from .models import FacebookPage  # or...

    social_account = kwargs['sociallogin'].account
    pages_list = get_pages_list(kwargs['sociallogin'].token.token)
    

    facebook_page_list = FacebookPage.objects.filter(account=social_account)
    
    for page in pages_list['data']:

        facebook_page = FacebookPage.objects.create(
            account=social_account, page_id=page['id'], access_token=page['access_token'], name=page['name'])
        facebook_page.save()
