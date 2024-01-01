from django.db import models
from django.contrib.auth.models import AbstractUser

TYPE_USER = (
    ('client', 'Cliente'),
    ('employee', 'Funcionário'),
    ('owner', 'Dono'),
    ('admin', 'Admin')
)


class Users(AbstractUser):
    username = models.CharField('username', max_length=40)
    type_user = models.CharField('Tipo do usuário', choices=TYPE_USER, default='client', max_length=100)
    full_name = models.CharField('Nome completo', max_length=100, default='')
    email = models.EmailField('email', unique=True)
    phone = models.CharField('Telefone', max_length=20, unique=True, blank=True, null=True)
    address = models.CharField('Endereço', max_length=50, blank=True, null=True)
    favorite_books = models.ManyToManyField('adminUsibras.Books', verbose_name='Livros Favoritos', blank=True, related_name='user_favorite_books')
    favorite_libraries = models.ManyToManyField('library.librarys', verbose_name='Bibliotecas Favoritas', blank=True, related_name='user_favorite_libraries')
    company_owner = models.BooleanField('Dono de alguma companhia?', default=False)
    library_owner = models.BooleanField('Dono de alguma biblioteca?', default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Usuários'
        verbose_name_plural = 'Usuários'
