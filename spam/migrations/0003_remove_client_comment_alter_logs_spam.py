# Generated by Django 4.2.3 on 2023-08-17 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0002_message_spam_logs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='comment',
        ),
        migrations.AlterField(
            model_name='logs',
            name='spam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='spam.spam', verbose_name='номер рассылки'),
        ),
    ]
