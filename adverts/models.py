from django.db import models
from library.models import Librarys
from users.models import Users


class Adverts(models.Model):
    announcement = models.ImageField('Anúncio')
    description = models.TextField('Descrição do anúncio', max_length=320, default='')
    library = models.ForeignKey(Librarys, verbose_name='Biblioteca anunciante', related_name='library_adverts', on_delete=models.CASCADE)
    create_at = models.DateTimeField('Data de início')
    expiration = models.DateTimeField('Data de expiração')

    def __str__(self):
        return str(f'{self.announcement} - {self.library}')

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'


class AdvertsViewed(models.Model):
    user_viewed = models.ForeignKey(Users, verbose_name='Visto pelo usuário', related_name='user_viewed_advert', on_delete=models.CASCADE)
    announcement = models.ForeignKey(Adverts, verbose_name='Anúncio visto', related_name='announcement_viewed', on_delete=models.CASCADE)
    date = models.DateTimeField('Data de visualização', auto_now_add=True)

    def __str__(self):
        return str(f'{self.announcement} - {self.user_viewed}')

    class Meta:
        verbose_name = 'Anúncio visualizado'
        verbose_name_plural = 'Anúncios visualizados'
