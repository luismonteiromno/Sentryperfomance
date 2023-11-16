from django.db import models
from adminUsibras.models import Books
from users.models import Users
from payment_methods.models import PaymentMethods


class BooksPurchases(models.Model):
    user = models.ForeignKey(Users, verbose_name='Usuário', related_name='user_book_purchase', on_delete=models.CASCADE)
    books = models.ManyToManyField(Books, verbose_name='Livros comprados')
    type_payment = models.ForeignKey(PaymentMethods, verbose_name='Tipo de pagamento', on_delete=models.CASCADE)
    date = models.DateTimeField('Data da compra', auto_created=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
