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
            library = Librarys.objects.create(
                owner_library_id=user.id,
                name=data['name'],
                address=data['address'],
                street=data['street'],
                number=data['number'],
                cep=data['cep']
            )
            companies = data['partner_companies'].split(',')
            if companies == None or '' or ' ':
                return Response({'message': 'Preencha o campo de empresas parceiras!'}, status=status.HTTP_400_BAD_REQUEST)

            for company in companies:
                library.partner_companies.add(int(company))
            return Response({'message': 'Biblioteca registrada com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao registrar biblioteca'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def list_librarys(self, request):
        try:
            librarys = self.queryset
            serializer = LibrarysSerializers(librarys, many=True)
            return Response({'message': 'Bibliotecas encontradas', 'librarys': serializer.data}, status=status.HTTP_200_OK)
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
            return Response({'message': 'Biblioteca encontrada', 'librarys': serializer.data},status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_librarys(self, request):
        data = request.data
        try:
            librarys = Librarys.objects.get(pk=data['library_id'])
            librarys.delete()
            return Response({'message': 'Biblioteca deletada com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar bibliotecas'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
