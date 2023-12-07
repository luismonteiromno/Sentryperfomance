from django.db import models
from users.models import Users

BOOK_STATE = (
    ('new', 'Novo'),
    ('semi-new', 'Semi-novo'),
    ('used', 'Usado')
)


class Companys(models.Model):
    owner = models.ManyToManyField(Users, verbose_name='Dono(s)')
    name = models.CharField('Nome da empresa', max_length=150, default='')
    phone = models.CharField('Telefone')
    email = models.EmailField('Email', unique=True)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    cep = models.CharField('CEP', max_length=14)
    street = models.CharField('Rua')
    state = models.CharField('Estado')
    complement = models.CharField('Complemento', blank=True, null=True)
    reference_point = models.CharField('Ponto de referência')
    number = models.CharField('Número')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class BookGenres(models.Model):
    book_genre = models.CharField('Gênero')

    def __str__(self):
        return f"{self.book_genre}"

    class Meta:
        verbose_name = 'Gênero do Livro'
        verbose_name_plural = 'Gênero dos Livros'


class Books(models.Model):
    title = models.CharField('Titulo', max_length=255)
    book_cover = models.ImageField('Capa do livro')
    synopsis = models.TextField('Sinopse', default='')
    price = models.FloatField('Preço')
    author = models.ManyToManyField(Users, verbose_name='Autor', default='')
    release_year = models.IntegerField('Ano de lançamento')
    state = models.CharField('Estado', max_length=50, choices=BOOK_STATE, default='new')
    pages = models.IntegerField('Quantidade de páginas')
    book_genre = models.ManyToManyField(BookGenres, verbose_name='Gênero do livro', related_name='books_genre')
    in_stock = models.BooleanField('Em estoque', default=True)
    publishing_company = models.ForeignKey(Companys, verbose_name='Publicado pela empresa', default='', on_delete=models.CASCADE)
    available_in_libraries = models.ForeignKey('library.Librarys', verbose_name='Disponível na biblioteca', related_name='book_available_libraries', on_delete=models.CASCADE)
    create_at = models.DateField('Data de criação', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"



