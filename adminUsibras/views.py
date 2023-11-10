from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import render
# from .signals import create_book
import sentry_sdk
from sentry_sdk import add_breadcrumb, configure_scope
from .models import Books, Companys
from .serializers import BooksSerializer, CompanysSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from datetime import datetime


class CompanysViewSet(ModelViewSet):
    serializer_class = CompanysSerializer
    queryset = Companys.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_company(self, request):
        data = request.data
        user = request.user

        try:

            with sentry_sdk.start_transaction(op="Endpoint de teste",
                                              name="Inicio do endpoint de criar companhias") as transaction:
                # Define a descrição do erro
                    with sentry_sdk.start_span(description=f"endpoint de criar companhias"):
                        # função q contém set_tags para personalizar a msg de erro no painel
                        with sentry_sdk.push_scope() as scope:
                            # set_tag cria um campo extra personalizado para exibir o erro

                            # set_tag q contem informações do erro, navegador, id do usuário e etc
                            # scope.set_tag('user', request.user.id)
                            companys = Companys.objects.create(
                                name=data['name'],
                                cnpj=data['cnpj']
                            )
                            companys.owner.add(user)
                            scope.set_extra("Nova companhia criada", companys)
                            add_breadcrumb(category='info', message=companys)

            transaction.finish()
            return Response({'message': 'Nova empresa registrada'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Error ao registrar empresa'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_companys(self, request):
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Listar companhias"):
                with sentry_sdk.start_span(description=f"Endpoint de listar companhias"):
                    # with sentry_sdk.push_scope() as scope:
                    companys = Companys.objects.all()
                    serializer = CompanysSerializer(companys, many=True)
                        # scope.set_extra("Companhias listadas", serializer.data)
                    add_breadcrumb(category='Companhias encontradas', message=serializer.data)

            return Response({'message': 'Empresas encontradas', 'companys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar empresas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companys_by_user(self, request):
        user = request.user
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Listar companhias do usuario"):
                # with sentry_sdk.start_span(description=f"Endpoint de listar companhias do usuario"):
                with sentry_sdk.push_scope() as scope:
                    companys = Companys.objects.filter(owner=user)
                    serializer = CompanysSerializer(companys, many=True)
                    scope.set_extra("Companhias listadas", serializer.data)
                    add_breadcrumb(category='Companhias encontradas', message=serializer.data)
            return Response({'message': 'Empresas encontradas', 'companys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar empresas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def companys_by_id(self, request):
        data = request.data
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Endpoint de listar companhia por id"):
                with sentry_sdk.start_span(description=f"Listar companhia por id"):
                    with sentry_sdk.push_scope() as scope:
                        companys = Companys.objects.get(pk=data['company_id'])
                        serializer = CompanysSerializer(companys)
                        scope.set_extra("Companhia encontrada", serializer.data)
                        add_breadcrumb(category='Companhia encontrada', message=serializer.data)
            return Response({'message': 'Empresa encontrada', 'company': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Empresa não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar empresas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_company(self, request):
        data = request.data
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Endpoint de deletar companhia por id"):
                with sentry_sdk.start_span(description=f"Deletar companhia por id"):
                    with sentry_sdk.push_scope() as scope:
                        companys = Companys.objects.get(pk=data['company_id'])
                        scope.set_extra("Companhia encontrada", companys)
                        add_breadcrumb(category='Companhia encontrada', message='companhia deletada')
                        companys.delete()
            return Response({'message': 'Empresa deletada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao deletar empresa'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BooksViewSet(ModelViewSet):
    serializer_class = BooksSerializer
    queryset = Books.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def register_book(self, request):
        user = request.user
        data = request.data
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Criar livro") as transaction:
                date_str = data['create_at']

                date_object = datetime.strptime(date_str, '%d/%m/%Y').date()

                Books.objects.create(
                    title=data['title'],
                    author_id=user.id,
                    price=data['price'],
                    release_year=data['release_year'],
                    state=data['state'],
                    pages=data['pages'],
                    publishing_company=data['publishing_company'],
                    create_at=date_object,
                )
            transaction.finish()
            return Response({'message': 'Livro registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Não foi possivel registrar o seu livro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_book(self, request):
        user = request.user
        data = request.data
        try:

            try:
                company = Companys.objects.get(id=data['publishing_company'])
            except Exception as error:
                print(error)
                return Response({'message': 'Empresa não encontrada!'}, status=status.HTTP_404_NOT_FOUND)

            book = Books.objects.get(id=data['book_id'])
            date_str = data['create_at']
            date_object = datetime.strptime(date_str, '%d/%m/%Y')
            if user in book.author.all():
                book.title = data['title']
                book.author.id = data.get('author_ids')
                book.price = data['price']
                book.release_year = data['release_year']
                book.state = data['state']
                book.pages = data['pages']
                book.publishing_company = company
                book.create_at = date_object
                book.save()
                return Response({'message': 'Livro atualizado com sucesso'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente os autores podem atualizar este livro!'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'message': 'Livro não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar livro!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methoEl menos bostero:ds=['GET'], permission_classes=[IsAuthenticated])
    def list_books(self, request):
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Listar livros") as transaction:
                books = Books.objects.all().order_by('price')
                serializer = BooksSerializer(books, many=True)
            transaction.finish()
            return Response({'message': 'Livros encontrados', 'books': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar livros'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_books(self, request):
        data = request.query_params
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Deletar livro") as transaction:
                books = Books.objects.get(pk=data['book_id'])
                books.delete()
            transaction.finish()
            return Response({'message': 'Livro deletado com sucesso!'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Livro não encontrado.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            print(error)
            return Response({'message': 'Nao Foi Possivel Deletar o Livro, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def search_book(self, request):
        data = request.query_params
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Buscar livro") as transaction:
                books = Books.objects.filter(title__iexact=data['title'])
                serializer = BooksSerializer(books, many=True)
            transaction.finish()
            return Response({'message': 'Livro encontrado', 'book': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Nẫo Foi Possivel encontrar o livro'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def book_by_id(self, request):
        params = request.query_params
        try:
            book = Books.objects.get(pk=params['book_id'])
            serializer = BooksSerializer(book)
            return Response({'message': 'Livro encontrado com sucesso', 'book': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Livro não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao buscar livro!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)