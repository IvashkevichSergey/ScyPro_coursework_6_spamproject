# Generated by Django 4.2.4 on 2023-09-22 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_user_verification_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(verbose_name='39544'),
        ),
    ]
