# Generated by Django 4.2.4 on 2023-09-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(default='710587', max_length=5),
        ),
    ]
