# Generated by Django 4.2.3 on 2023-08-20 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0004_alter_spam_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spam',
            name='messages',
        ),
        migrations.AddField(
            model_name='spam',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='spam.message', verbose_name='сообщение к рассылке'),
        ),
    ]