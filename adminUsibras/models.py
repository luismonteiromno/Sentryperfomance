from django.db import models
from users.models import Users


BOOK_STATE = (
    ('new', 'Novo'),
    ('semi-new', 'Semi-novo'),
    ('used', 'Usado')
)

BOOK_GENRE = (
    ('mistery', 'Mistério'),
    ('comedy', 'Comédia'),
    ('romance', 'Romance'),
    ('terror', 'Terror'),
)


class Companys(models.Model):
    owner = models.ManyToManyField(Users, verbose_name='Dono(s)')
    name = models.CharField('Nome da empresa', max_length=150, default='')
    cnpj = models.CharField('CNPJ', max_length=14)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Books(models.Model):
    title = models.CharField('Titulo', max_length=255)
    author = models.ManyToManyField(Users, verbose_name='Autor', default='')
    release_year = models.IntegerField('Ano de lançamento')
    state = models.CharField('Estado', max_length=50, choices=BOOK_STATE, default='new')
    pages = models.IntegerField('Quantidade de páginas')
    book_genre = models.CharField('Genero do livro', choices=BOOK_GENRE, max_length=50, default='')
    publishing_company = models.ForeignKey(Companys, verbose_name='Publicado pela empresa', default='', on_delete=models.CASCADE)
    create_at = models.DateField('Data de criação', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Livro"
        verbose_name_plural = "Livros"



