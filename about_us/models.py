from django.db import models


class AboutUs(models.Model):
    name = models.CharField('Nome', max_length=100, default='')
    developed_by = models.CharField('Desenvolvido por:', max_length=150)
    description = models.TextField('Descrição', max_length=255)
    email = models.EmailField('Email para contato:', unique=True)
    phone = models.CharField('Telefone para contato:', max_length=50)

    def __str__(self):
        return f"{self.name} - {self.developed_by}"

    class Meta:
        verbose_name = 'Sobre nós'
        verbose_name_plural = 'Sobre nós'


class TermsOfUse(models.Model):
    terms_of_use = models.FileField(upload_to='terms_of_use', verbose_name='Termos de Uso')

    def __str__(self):
        return str(self.terms_of_use)

    class Meta:
        verbose_name = 'Termo de Uso'
        verbose_name_plural = 'Termos de Uso'

