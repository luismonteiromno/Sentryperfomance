from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import PaymentMethods
from .serializers import PaymentMethodsSerializers


class PaymentMethodsViewSet(ModelViewSet):
    queryset = PaymentMethods.objects.all()
    serializer_class = PaymentMethodsSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_payments_methods(self, request):
        try:
            payment_method = PaymentMethods.objects.all()
            serializer = PaymentMethodsSerializers(payment_method, many=True)
            return Response({'message': 'Métodos de pagamentos encontrados', 'payment_methods': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar tipos de pagamento!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
