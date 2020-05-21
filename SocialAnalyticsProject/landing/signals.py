from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from modules.utils.facebook_urls import get_pages_list,get_page_posts
from modules.utils.helpers import get_page_post_helper

# Signal launched after a user is signed up and before the login occue
@receiver(user_signed_up)
def social_login_handler(sender, **kwargs):
    from .models import FacebookPage  # or...
    from reporting.models import FacebookPost
    
	# Retrieve the social account object
    social_account = kwargs['sociallogin'].account
    
	# Retrieve pages that the account has
    pages_list = get_pages_list(kwargs['sociallogin'].token.token)
    
    for page in pages_list['data']:

        # Save each page in the database.   
        facebook_page = FacebookPage.objects.create(
                    account=social_account, page_id=page['id'], access_token=page['access_token'], name=page['name'])
        facebook_page.save()

        # Retrive page posts and save them in the database
        data = get_page_posts(facebook_page.page_id,facebook_page.access_token)
        get_page_post_helper(data,facebook_page)
