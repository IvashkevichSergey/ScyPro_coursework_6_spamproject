# Generated by Django 4.2.4 on 2023-09-06 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spam', '0009_alter_spam_id_alter_spam_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spam',
            name='title',
            field=models.CharField(default="Рассылка_(<class 'django.db.models.fields.NOT_PROVIDED'>, None, None, True)", max_length=150, verbose_name='Название'),
        ),
    ]