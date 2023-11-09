from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import AboutUs, TermsOfUse, PrivacyPolice
from .serializers import AboutUsSerializer, TermsOfUseSerializer, PrivacyPoliceSerializers


class AboutUsViewSet(ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
    permission_classes = AllowAny

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def about_us(self, request):
        try:
            about_us = AboutUs.objects.last()
            if about_us != None:
                serializer = AboutUsSerializer(about_us)
                return Response({'message': 'Sobre Nós', 'about_us': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Informação não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar sobre nós!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TermsOfUseViewSet(ModelViewSet):
    queryset = TermsOfUse.objects.all()
    serializer_class = TermsOfUseSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def terms_of_use(self, request):
        try:
            terms_of_use = TermsOfUse.objects.last()
            if terms_of_use != None:
                serializer = TermsOfUseSerializer(terms_of_use)
                return Response({'message': 'Termos de Uso', 'about_us': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Informação não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar Termos de Uso!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrivacyPoliceViewSet(ModelViewSet):
    queryset = PrivacyPolice.objects.all()
    serializer_class = PrivacyPoliceSerializers
    permission_classes = [AllowAny]

    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def privacy_police(self, request):
        try:
            privacy_police = PrivacyPolice.objects.last()
            if privacy_police != None:
                serializer = PrivacyPoliceSerializers(privacy_police)
                return Response({'message': 'Políticas de Privacidade', 'privacy_police': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Informação não encontrada!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao exibir políticas de privacidade'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
