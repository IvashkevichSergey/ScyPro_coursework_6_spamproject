# Generated by Django 4.2.4 on 2023-09-06 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0006_remove_logs_post_answer_logs_client_logs_errors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spam',
            name='title',
            field=models.CharField(default='Рассылка_<django.db.models.fields.BigAutoField>', max_length=50, verbose_name='Название'),
        ),
    ]
