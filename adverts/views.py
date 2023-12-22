from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from .models import Adverts
from .serializers import AdvertsSerializers
from library.models import Librarys
from datetime import datetime



class AdvertsViewSet(ModelViewSet):
    queryset = Adverts.objects.all()
    serializer_class = AdvertsSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_announcement(self, request):
        user = request.user
        data = request.data
        try:
            library = Librarys.objects.get(id=data['library_id'])
            if user in library.owner_library.all():
                create_at = datetime.strptime(data['create_at'], '%d/%m/%Y %H:%M')
                expiration = datetime.strptime(data['expiration'], '%d/%m/%Y %H:%M')
                Adverts.objects.create(
                    announcement=data['announcement'],
                    library_id=library.id,
                    create_at=create_at,
                    expiration=expiration
                )
                return Response({'message': 'Anúncio criado com sucesso!'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Somente o(s) usuário(s) dono(s) desta biblioteca pode(m) criar anúncios!'},
                                status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response({'message': 'Biblioteca anunciante não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao criar anúncio!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
