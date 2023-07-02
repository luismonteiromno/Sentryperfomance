from django.db import models
from adminUsibras.models import Companys
from users.models import Users


class Librarys(models.Model):
    owner_library = models.ForeignKey(Users, verbose_name='Dono', related_name='owner_library', on_delete=models.CASCADE, null=True)
    name = models.CharField('Nome da livraria', max_length=100)
    address = models.CharField('Endereço', max_length=50)
    partner_companies = models.ManyToManyField(Companys, verbose_name='Companhias parceiras', related_name='library_partner_companies')

    def __str__(self):
        return f"{self.name} - {self.address}"

    class Meta:
        verbose_name = 'Biblioteca'
        verbose_name_plural = 'Bibliotecas'
