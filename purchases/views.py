from datetime import datetime
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

import sentry_sdk

from adminUsibras.models import Books
from payment_methods.models import PaymentMethods
from .models import BooksPurchases
from .serializers import BooksPurchasesSerializers


class BooksPurchasesViewSet(ModelViewSet):
    queryset = BooksPurchases.objects.all()
    serializer_class = BooksPurchasesSerializers
    permission_classes = IsAuthenticated

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_purchase(self, request):
        user = request.user
        data = request.data
        try:
            now = datetime.now()
            book_ids = [int(book_id) for book_id in data['books_id'].split(',')]

            if Books.objects.filter(id__in=book_ids, in_stock=False).exists():
                return Response({'message': 'Alguns livros não estão em estoque. A compra não pode ser concluída.'},
                                status=status.HTTP_400_BAD_REQUEST)

            type_payment = PaymentMethods.objects.get(id=data['type_payment'])

            books_purchase = BooksPurchases.objects.create(
                user_id=user.id,
                type_payment=type_payment,
                date=now
            )

            for purchase in book_ids:
                books_purchase.books.add(purchase)

            return Response({'message': 'Compra feita com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Tipo de pagamento não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro efetuar compra'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def books_purchase_by_user(self, request):
        user = request.user
        try:
            books = BooksPurchases.objects.filter(user_id=user.id).order_by('date')
            serializer = BooksPurchasesSerializers(books, many=True)
            return Response({'message': 'Sucesso', 'books': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_all_purchases(self, request):
        try:
            books = BooksPurchases.objects.all().order_by('date')
            serializer = BooksPurchasesSerializers(books, many=True)
            return Response({'message': 'Sucesso', 'purchases': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_purchases_by_type_payment(self, request):
        params = request.query_params
        try:
            books = BooksPurchases.objects.filter(type_payment_id=params['type_payment'])
            serializer = BooksPurchasesSerializers(books, many=True)
            return Response({'message': 'Sucesso', 'purchases': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def purchase_by_id(self, request):
        params = request.query_params
        try:
            purchase = BooksPurchases.objects.get(pk=params['purchase_id'])
            serializer = BooksPurchasesSerializers(purchase)
            return Response({'message': 'Sucesso', 'books': serializer.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": 'Compra não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def books_purchase_by_user_id(self, request):
        params = request.query_params
        try:
            books = BooksPurchases.objects.filter(user_id=params['user_id']).order_by('date')
            serializer = BooksPurchasesSerializers(books, many=True)
            return Response({'message': 'Sucesso', 'books': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao listar todos o livros comprados pelo usuário'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def search_purchase_book(self, request):
        params = request.query_params
        try:
            book = BooksPurchases.objects.filter(books__title__iexact=params['book_title'])
            serializer = BooksPurchasesSerializers(book, many=True)
            return Response({'message': 'Livro encontrado', 'book': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            sentry_sdk.capture_exception(error)
            return Response({'message': 'Erro ao procurar compra!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
