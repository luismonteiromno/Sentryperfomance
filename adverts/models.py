from django.db import models
from library.models import Librarys


class Adverts(models.Model):
    announcement = models.ImageField('Anúncio')
    library = models.ForeignKey(Librarys, verbose_name='Biblioteca anunciante', related_name='library_adverts', on_delete=models.CASCADE)
    create_at = models.DateTimeField('Data de início')
    expiration = models.DateTimeField('Data de expiração')

    def __str__(self):
        return str(f'{self.announcement} - {self.library}')

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
