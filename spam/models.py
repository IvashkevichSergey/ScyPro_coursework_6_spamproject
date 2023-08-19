from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(**NULLABLE, verbose_name='электронная почта')

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=50, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    def __str__(self):
        return f'Сообщение "{self.subject}"'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Spam(models.Model):
    STATUS_CHOICES = [
        ('created', 'создана'),
        ('running', 'запущена'),
        ('completed', 'завершена')
    ]

    title = models.CharField(max_length=50, verbose_name='Название')
    spam_time = models.TimeField(verbose_name='время рассылки')
    periodicity = models.SmallIntegerField(default=7, verbose_name='периодичность рассылки (дней)')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус')
    clients = models.ManyToManyField(Client, verbose_name='кому отправить')
    messages = models.ManyToManyField(Message, verbose_name='сообщения к рассылке')

    def __str__(self):
        return f'Рассылка {self.title} {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Logs(models.Model):
    spam = models.ForeignKey(Spam, **NULLABLE, on_delete=models.SET_NULL, verbose_name='номер рассылки')
    last_send = models.DateTimeField(verbose_name='дата и время последней рассылки')
    status = models.CharField(verbose_name='статус последней рассылки')
    post_answer = models.CharField(verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'Рассылка: {self.spam}\n' \
               f'Последняя отправка: {self.last_send}\n' \
               f'Статус: {self.status}\n' \
               f'Ответ от сервера {self.post_answer}\n'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
