from random import randint

from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    avatar = models.ImageField(**NULLABLE, upload_to='users/', verbose_name='аватар')
    is_active = models.BooleanField(default=False, verbose_name='статус верификации')
    verification_code = models.CharField(max_length=6, default=''.join(str(randint(0, 10)) for _ in range(5)))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
