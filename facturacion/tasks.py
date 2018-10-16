from __future__ import absolute_import
from celery import shared_task


@shared_task
def sumar(x,y):
    result = x+y
    print(result)
    return result