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

            date_str = data['create_at']

            date_object = datetime.strptime(date_str, '%d/%m/%Y').date()

            books = Books.objects.create(
                title=data['title'],
                author_id=user.id,
                release_year=data['release_year'],
                state=data['state'],
                pages=data['pages'],
                publishing_company=data['publishing_company'],
                create_at=date_object,
            )
            print(books)
            return Response({'message': 'Livro registrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Não foi possivel registrar o seu livro'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_books(self, request):
        user = request.user
        try:

            list = Books.objects.filter(user=user).order_by('create_at')
            serializer = BooksSerializer(list, many=True)
            return Response({'message': 'Livros encontrados', 'books': serializer.data}, status=status.HTTP_200_OK)

        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar livros'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_books(self, request):
        data = request.query_params
        try:
            books = Books.objects.get(pk=data['book_id'])
            books.delete()
            return Response({'message': 'Cartão deletado com sucesso!'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Cartão não encontrado.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as error:
            print(error)
            return Response({'message': 'Nao Foi Possivel Deletar o Cartão, Entre em Contato com o Suporte.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)