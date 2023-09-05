from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_job

import datetime
import smtplib

from django.core.mail import send_mail

from config import settings
from spam.models import Spam, Message, Logs


def send_emails():
    # Ищем рассылки со статусом running
    mailings = Spam.objects.filter(status='running')
    # Проходим по всем рассылкам со статусом running
    for spam_email in mailings:
        # Проверяем, отправлялась ли данная рассылка ранее
        suitable_logs = Logs.objects.filter(spam=spam_email)
        if suitable_logs:
            print()
            # Получаем из логов информацию по последней отправленной рассылке
            # last_spam = suitable_logs.order_by('-last_send').first()
            # # Получаем дату отправки последней отправленной рассылки
            # last_send = last_spam.last_send
            # print(f'Рассылка последний раз отправлялась: {last_send}')
            #
            # # Получаем текущую дату
            # current_time = timezone.now()
            # print(f'Текущее время: {current_time}')
            #
            # print((current_time - last_send).days)
            #
            # spam_periodicity = spam_email.periodicity
            # print(f'Периодичность рассылки: {spam_periodicity} дней')
            #
            # # Проверяем сколько дней прошло с момента отправки последней рассылки,
            # # сравниваем с периодичностью рассылки
            # if (current_time - last_send).days >= spam_periodicity:
            #     print('Запускается скрипт рассылки спама')
        else:
            print('\nУ рассылки', spam_email, 'ещё нет логов')

            current_time = timezone.now()
            print(f'Текущее время: {current_time}')

            # Получаем запланированное время отправки рассылки
            spam_time = spam_email.spam_time
            print(f'Время рассылки: {spam_time}')

            # Вычисляем оставшееся время до запланированной отправки
            t1 = timezone.timedelta(hours=current_time.hour, minutes=current_time.minute)
            t2 = timezone.timedelta(hours=spam_time.hour, minutes=spam_time.minute)
            time_to_send_spam = (t2 - t1).seconds / 60
            print(time_to_send_spam)

            if 0 <= time_to_send_spam < 5:
                print('Запускается рассылка СПАМа в первый раз')



def send_spam(email_params: Spam):
    try:
        clients_emails = [client.email for client in list(email_params.clients.all())]
        # send_mail(
        #     subject=email_params.message.subject,
        #     message=email_params.message.body,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=clients_emails,
        #     fail_silently=False
        # )
    except smtplib.SMTPException as e:
        print(e)
    else:
        print('all messages sent')


def send_hello():
    time = datetime.datetime.now()
    sp = Spam.objects.all()[0]
    print('Периодичность рассылки -> ', sp.periodicity)
    print('hello world:[{}]'.format(time))
    l = Logs.objects.all()[2]
    print(datetime.datetime.now())
    # print(datetime.time.hour)
    # offset = timezone.timezone(timezone.timedelta(hours=3))
    # cur_time = timezone.datetime.utcoffset(tz=offset)
    # print(cur_time)
    # now(tz=offset)
    # print(cur_time.hour, cur_time.minute)
    # sp_time = sp.spam_time
    # print(sp_time.hour, sp_time.minute)
    # t1 = timezone.timedelta(hours=cur_time.hour, minutes=cur_time.minute)
    # t2 = timezone.timedelta(hours=sp_time.hour, minutes=sp_time.minute)
    # print(t1 - t2)
    # a = (t1 - t2).seconds / 60
    # print(a)
    # print(0 <= a <= 5)

    # print(cur_time, ' --- ', l.last_send)
    # print(timezone.timedelta(cur_time, sp.spam_time))
    # # print(timezone.now().strptime())
    # print(datetime.timedelta(cur_time, sp.spam_time))


def task_schedular():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_emails, trigger=CronTrigger(second='*/5'))
    scheduler.start()
