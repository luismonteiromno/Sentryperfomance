from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Users
from .serializers import UsersSerializers


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializers
    permission_classes = AllowAny

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def create_user(self, request):
        data = request.data
        try:
            user = Users.objects.create(
                username=data['username'],
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                company_owner=data['company_owner'],
                library_owner=data['library_owner']
            )
            user.set_password(data['password'])
            Token.objects.create(user=user)
            return Response({'message': 'Usuário cadastrado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao criar usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        data = request.data
        try:
            user = Users.objects.filter(pk=user.id).update(
                username=data['username'],
                full_name=data['full_name'],
                email=data['email'],
                phone=data['phone'],
                address=data['address'],
                company_owner=data['company_owner'],
                library_owner=data['library_owner']
            )
            # if user.password != data['password']:
            #     user.set_password(data['password'])
            return Response({'message': 'Usuário atualizado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        user = request.user
        try:
            user = Users.objects.get(id=user.id)
            user.delete()
            return Response({'message': 'Usuário deletado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao deletar usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_user(self, request):
        user = request.user
        try:
            user = Users.objects.get(id=user.id)
            serializer = UsersSerializers(user)
            return Response({'message': 'Perfil do usuário', 'user': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao exibir perfil do usuário!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def update_user_library_owner(self, request):
        user = request.user
        data = request.data
        try:
            user = Users.objects.get(id=user.id)
            user.library_owner = data['library_owner']
            user.save()
            return Response({'message': 'Campo atualizado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar campo!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PUT'], permission_classes=[IsAuthenticated])
    def update_user_company_owner(self, request):
        user = request.user
        data = request.data
        try:
            user = Users.objects.get(id=user.id)
            user.company_owner = data['company_owner']
            user.save()
            return Response({'message': 'Campo atualizado com sucesso'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar campo!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
