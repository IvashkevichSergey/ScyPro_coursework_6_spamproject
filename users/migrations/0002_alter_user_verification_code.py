# Generated by Django 4.2.4 on 2023-09-04 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verification_code',
            field=models.CharField(default='74148', max_length=5),
        ),
    ]
