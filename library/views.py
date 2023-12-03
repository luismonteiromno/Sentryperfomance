from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import render
# from .signals import create_book
import sentry_sdk
from sentry_sdk import add_breadcrumb, configure_scope
from .models import Librarys
from .serializers import LibrarysSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from datetime import datetime


class LibraryViewSet(ModelViewSet):
    queryset = Librarys.objects.all()
    serializer_class = LibrarysSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_library(self, request):
        user = request.user
        data = request.data
        try:
            with sentry_sdk.start_transaction(op="Endpoint", name=f"Criar livro") as transaction:
                companies = data['partner_companies'].split(',')
                books_sale = data['books_for_sale'].split(',')
                if not companies or all(company.strip() == '' for company in companies):
                    return Response({'message': 'Preencha o campo de empresas parceiras!'},
                                    status=status.HTTP_400_BAD_REQUEST)
                if not books_sale or all(book_sale.strip() == '' for book_sale in books_sale):
                    return Response({'message': 'Preencha o campo de livros à venda!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if data['delivery'] == True and data.get('minimum_delivery') == None and data.get('maximum_delivery') == None:
                    return Response({'message': 'Preencha os campos de tempo de entrega!'}, status=status.HTTP_400_BAD_REQUEST)

                if data['delivery'] == False and data.get('minimum_delivery') != None and data.get('maximum_delivery') != None:
                    return Response({'message': 'Preencha o campo de entrega!'}, status=status.HTTP_400_BAD_REQUEST)

                if data.get('minimum_delivery') != None and data.get('maximum_delivery') != None and data.get('minimum_delivery') >= data.get('maximum_delivery'):
                    return Response({'message': 'O tempo minimo de entrega não pode ser menor/igual ao tempo máximo!'}, status=status.HTTP_400_BAD_REQUEST)

                library = Librarys.objects.create(
                    name=data['name'],
                    address=data['address'],
                    street=data['street'],
                    number=data['number'],
                    cep=data['cep'],
                    opening_time=data['opening_time'],
                    closing_time=data['closing_time'],
                    delivery=data['delivery'],
                    minimum_delivery=data.get('minimum_delivery'),
                    maximum_delivery=data.get('maximum_delivery')
                )
                library.owner_library.add(user)

                for company in companies:
                    library.partner_companies.add(int(company))

                for book in books_sale:
                    library.books_for_sale.add(int(book))

            transaction.finish()
            return Response({'message': 'Biblioteca registrada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar biblioteca'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_library(self, request):
        user = request.user
        data = request.data
        try:
            library = Librarys.objects.get(id=data['library_id'])
            if user not in library.owner_library.all():
                return Response({'message': 'Apenas o dono pode atualizar à biblioteca!'}, status=status.HTTP_401_UNAUTHORIZED)
            library.name = data['name']
            library.address = data['address']
            library.street = data['street']
            library.number = data['number']
            library.cep = data['cep']
            library.opening_time = data['opening_time']
            library.closing_time = data['closing_time']
            library.delivery = data['delivery']
            library.minimum_delivery = data['minimum_delivery']
            library.maximum_delivery = data['maximum_delivery']
            partner_companies = data['partner_companies'].split(',')
            books_for_sale = data['books_for_sale'].split(',')

            if library.partner_companies != partner_companies:
                if not partner_companies:
                    return Response({'message': 'Preencha o campo de empresas parceiras!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                library.partner_companies.clear()
                for company in partner_companies:
                    library.partner_companies.add(int(company))

            if library.books_for_sale != books_for_sale:
                if not books_for_sale:
                    return Response({'message': 'Preencha o campo de livros à venda!'},
                                    status=status.HTTP_400_BAD_REQUEST)

                library.books_for_sale.clear()
                for book in books_for_sale:
                    library.books_for_sale.add(int(book))

            library.save()
            return Response({'message': 'Biblioteca atualizada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar biblioteca!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_librarys(self, request):
        try:
            libraries = self.queryset
            serializer = LibrarysSerializers(libraries, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'librarys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_libraries_deliver(self, request):
        try:
            libraries = Librarys.objects.filter(delivery=True)
            serializer = LibrarysSerializers(libraries, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'libraries': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_librarys_by_user(self, request):
        user = request.user
        try:
            librarys = Librarys.objects.filter(owner_library=user)
            serializer = LibrarysSerializers(librarys, many=True)
            return Response({'message': 'Bibliotecas do usuário encontradas', 'librarys': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_librarys_by_id(self, request):
        params = request.query_params
        try:
            librarys = Librarys.objects.get(id=params['library_id'])
            serializer = LibrarysSerializers(librarys)
            return Response({'message': 'Biblioteca encontrada', 'librarys': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_librarys(self, request):
        user = request.user
        data = request.data
        try:
            library = Librarys.objects.get(pk=data['library_id'])
            if user.id != library.owner_library:
                return Response({'message': 'Somente o dono da biblioteca pode exclui-lá!'}, status=status.HTTP_401_UNAUTHORIZED)

            library.delete()
            return Response({'message': 'Biblioteca deletada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def filter_time_delivery(self, request):
        params = request.query_params
        try:
            minimum_delivery = params['minimum_delivery']
            maximum_delivery = params['maximum_delivery']
            if minimum_delivery >= maximum_delivery:
                return Response({'message': 'O tempo minimo de entrega não pode ser maior/igual ao tempo máximo!'},
                                status=status.HTTP_400_BAD_REQUEST)
            libraries = Librarys.objects.filter(
                delivery=True, minimum_delivery__gte=minimum_delivery, maximum_delivery__lte=maximum_delivery
            )
            serializer = LibrarysSerializers(libraries, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'libraries': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar tempo de entrega'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def search_library_by_name(self, request):
        params = request.query_params
        try:
            library = Librarys.objects.filter(name__icontains=params['library_name'])
            serializer = LibrarysSerializers(library, many=True)
            return Response({'message': 'Biblioteca(s) encontrada(s)', 'librarys': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Biblioteca não encontrada!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def libraries_by_opening_hours(self, request):
        params = request.query_params
        try:
            if params['opening_time'] >= params['closing_time']:
                return Response({'message': 'O Horário de abertura não pode ser maior/igual ao horário de fechamento!'},
                                status=status.HTTP_400_BAD_REQUEST)

            libraries = Librarys.objects.filter(opening_time__lte=params['opening_time'], closing_time__gte=params['closing_time'])
            serializer = LibrarysSerializers(libraries, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'libraries': serializer.data},  status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def open_libraries_now(self, request):
        now = datetime.now().time()
        try:
            libraries = Librarys.objects.filter(opening_time__lte=now, closing_time__gte=now)
            serializer = LibrarysSerializers(libraries, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'libraries': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
