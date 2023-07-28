from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

import sentry_sdk

from .models import BooksPurchases
from .serializers import BooksPurchasesSerializers


class BooksPurchasesViewSet(ModelViewSet):
    queryset = BooksPurchases.objects.all()
    serializer_class = BooksPurchasesSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def books_purchase_by_user(self, request):
        user = request.user
        try:
            books = BooksPurchases.objects.filter(user=user)
            serializer = BooksPurchasesSerializers(books, many=True)
            return Response({'message': 'Sucesso', 'books': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)