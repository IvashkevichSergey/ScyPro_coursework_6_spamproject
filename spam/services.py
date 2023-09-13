from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import smtplib

from django.core.mail import send_mail

from config import settings
from spam.models import Spam, Logs, Client


def send_emails():
    """
    Функция сравнивает текущие дату/время с датой и временем, на которые запланированы
    рассылки. С заданной периодичностью запускает функцию отправки сообщений конкретным клиентам
    """
    # Ищем рассылки со статусом running
    mailings = Spam.objects.filter(status='started')
    # Проходим по всем рассылкам со статусом running
    for spam_email in mailings:
        # Проходим по всем клиентам из рассылки
        for client in spam_email.clients.all():
            # Получаем текущую дату
            current_time = timezone.now()
            # Проверяем, отправлялась ли данная рассылка конкретному клиенту ранее
            suitable_logs = Logs.objects.filter(spam=spam_email, client=client)
            if suitable_logs:
                # Получаем из логов информацию по последней отправленной рассылке
                last_spam = suitable_logs.order_by('-last_send').first()
                # Получаем дату отправки последней отправленной рассылки
                last_send = last_spam.last_send
                # Получаем периодичность рассылки
                spam_periodicity = spam_email.periodicity

                # Проверяем сколько дней прошло с момента отправки последней рассылки,
                # сравниваем с периодичностью рассылки
                if (current_time - last_send).days >= spam_periodicity:
                    print('Запускается скрипт рассылки СПАМа')
                    send_spam(spam_email, client)
            else:
                # Получаем запланированное время отправки рассылки
                spam_time = spam_email.spam_time

                # Вычисляем оставшееся время в минутах до запланированной отправки
                t1 = timezone.timedelta(hours=current_time.hour, minutes=current_time.minute)
                t2 = timezone.timedelta(hours=spam_time.hour, minutes=spam_time.minute)
                time_to_send_spam = (t2 - t1).seconds / 60
                # print("Оставшееся время до запуска рассылки:", time_to_send_spam, "минут")

                # Запускаем рассылку в 1ый раз с точностью до 5мин до запланированного времени
                if 0 <= time_to_send_spam < 5:
                    print('Запускается рассылка СПАМа в первый раз')
                    send_spam(spam_email, client)


def create_logs(email_params: Spam, client: Client, status: str, errors: str):
    """Функция для записи в базу данных логов отправки писем"""
    log = Logs.objects.create(
        spam=email_params,
        last_send=timezone.now(),
        status=status,
        client=f'{client}',
        errors=errors
    )
    log.save()


def send_spam(email_params: Spam, client: Client):
    """
    Запускает функцию отправки писем конкретным адресатам,
    обрабатывает возможные ошибки, вызывает функция записи логов отправки
    """
    try:
        email = send_mail(
            subject=email_params.message.subject,
            message=email_params.message.body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email],
            fail_silently=False
        )
    except smtplib.SMTPDataError as err:
        print(err)
        create_logs(email_params, client, 'failed', 'SMTPDataError')
    except smtplib.SMTPException as err:
        print(err)
        create_logs(email_params, client, 'failed', 'SMTPException')
    else:
        if email:
            print('message sent')
            create_logs(email_params, client, 'ок', 'Без ошибок')
        else:
            print('something went wrong')
            create_logs(email_params, client, 'failed', 'Ошибка доставки письма')


def task_schedular():
    """Запускает крон для периодической проверки активных рассылок"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_emails, trigger=CronTrigger(minute='*/5'))
    scheduler.start()
