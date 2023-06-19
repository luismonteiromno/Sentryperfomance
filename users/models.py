from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    username = models.CharField('username', max_length=40)
    full_name = models.CharField('Nome completo', max_length=100, default='')
    email = models.EmailField('email', unique=True)
    phone = models.CharField('Telefone', max_length=20, unique=True, blank=True)
    address = models.CharField('Endereço', max_length=50, blank=True, null=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Usuários'
        verbose_name_plural = 'Usuários'