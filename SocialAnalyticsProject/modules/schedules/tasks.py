from celery import shared_task
from time import sleep


@shared_task
def print_wait():
    print('k')
    sleep(4)