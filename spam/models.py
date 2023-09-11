from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    email = models.EmailField(**NULLABLE, verbose_name='электронная почта')
    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE, verbose_name='владелец клиента')

    def __str__(self):
        return f'{self.full_name} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    subject = models.CharField(max_length=50, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')
    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE, verbose_name='владелец клиента')

    def __str__(self):
        return f'Сообщение на тему "{self.subject}"'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Spam(models.Model):
    STATUS_CHOICES = [
        ('created', 'создана'),
        ('started', 'запущена'),
        ('completed', 'завершена')
    ]

    title = models.CharField(default=f'Рассылка ', max_length=50, verbose_name='Название')
    spam_time = models.TimeField(verbose_name='время рассылки')
    periodicity = models.SmallIntegerField(default=1, verbose_name='периодичность рассылки (дней)')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name='статус')
    clients = models.ManyToManyField(Client, verbose_name='адресаты рассылки')
    message = models.ForeignKey(Message, default=None, on_delete=models.CASCADE, verbose_name='сообщение к рассылке')
    owner = models.ForeignKey(User, **NULLABLE, on_delete=models.CASCADE, verbose_name='автор рассылки')

    def __str__(self):
        return f'{self.title}, статус "{self.get_status_display()}"'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Logs(models.Model):
    STATUS_CHOICES = [
        ('ок', 'успешно'),
        ('failed', 'ошибка'),
    ]
    spam = models.ForeignKey(Spam, **NULLABLE, on_delete=models.SET_NULL, verbose_name='Рассылка')
    last_send = models.DateTimeField(verbose_name='дата и время последней рассылки')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name='статус последней рассылки')
    client = models.CharField(**NULLABLE, max_length=50, verbose_name='клиент')
    errors = models.CharField(max_length=100, verbose_name='ошибки отправки')

    def __str__(self):
        return f'Рассылка: {self.spam}\n' \
               f'Последняя отправка: {self.last_send}\n' \
               f'Статус: {self.status}\n' \
               f'Клиент: {self.client}\n'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
