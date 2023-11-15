from django.db import models


class PaymentMethods(models.Model):
    method = models.CharField('Método')

    def __str__(self):
        return str(f"{self.method}")

    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'
