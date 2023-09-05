# Generated by Django 4.2.3 on 2023-08-17 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
        migrations.CreateModel(
            name='Spam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Название')),
                ('spam_time', models.TimeField(verbose_name='время рассылки')),
                ('periodicity', models.SmallIntegerField(default=7, verbose_name='периодичность рассылки (дней)')),
                ('status', models.CharField(default='создана', max_length=25, verbose_name='статус')),
                ('clients', models.ManyToManyField(to='spam.client', verbose_name='кому отправить')),
                ('messages', models.ManyToManyField(to='spam.message', verbose_name='сообщения к рассылке')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_send', models.DateTimeField(verbose_name='дата и время последней рассылки')),
                ('status', models.CharField(verbose_name='статус последней рассылки')),
                ('post_answer', models.CharField(verbose_name='ответ почтового сервера')),
                ('spam', models.ForeignKey(on_delete=models.SET('--рассылка удалена--'), to='spam.spam', verbose_name='номер рассылки')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
    ]
