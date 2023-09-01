from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    username = models.CharField('username', max_length=40)
    full_name = models.CharField('Nome completo', max_length=100, default='')
    email = models.EmailField('email', unique=True)
    phone = models.CharField('Telefone', max_length=20, unique=True, blank=True, null=True)
    address = models.CharField('Endereço', max_length=50, blank=True, null=True)
    company_owner = models.BooleanField('Dono de alguma companhia?', default=False)
    library_owner = models.BooleanField('Dono de alguma biblioteca?', default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Usuários'
        verbose_name_plural = 'Usuários'