# Generated by Django 4.2.4 on 2023-09-16 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spam_messages', '0001_initial'),
        ('spam', '0017_rename_owner_message_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spam',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='spam_messages.message', verbose_name='сообщение к рассылке'),
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
