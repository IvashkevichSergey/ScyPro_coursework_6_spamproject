import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_job

import datetime
import smtplib

from django.core.mail import send_mail

from config import settings
from spam.models import Spam, Message


def send_spam(email_params: Spam):
    try:
        clients_emails = [client.email for client in list(email_params.clients.all())]
        send_mail(
            subject=email_params.message.subject,
            message=email_params.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_emails,
            fail_silently=False
        )
    except smtplib.SMTPException as e:
        print(e)
    else:
        print('all messages sent')


def send_hello():
    time = datetime.datetime.now()
    print('hello world:[{}]'.format(time))


def task_schedular():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_hello, trigger=CronTrigger(second='00'))
    scheduler.start()

