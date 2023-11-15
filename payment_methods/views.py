from django.shortcuts import render
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import PaymentMethods
from .serializers import PaymentMethodsSerializers


class PaymentMethodsViewSet(ModelViewSet):
    queryset = PaymentMethods.objects.all()
    serializer_class = PaymentMethodsSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def create_payment_method(self, request):
        data = request.data
        try:
            PaymentMethods.objects.create(
                method=data['new_method']
            )
            return Response({'message': 'Novo método criado'}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao criar novo método de pagamento!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['PATCH'], permission_classes=[IsAuthenticated])
    def update_payment_method(self, request):
        data = request.data
        try:
            payment_method = PaymentMethods.objects.get(id=data['payment_method_id'])
            payment_method.method = data['payment_method']
            payment_method.save()
            return Response({'message': 'Método atualizado com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Método de pagamento não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao atualizar o método de pagamento!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def payment_method_by_id(self, request):
        params = request.query_params
        try:
            payment_method = PaymentMethods.objects.get(id=params['payment_method_id'])
            serializer = PaymentMethodsSerializers(payment_method)
            return Response({'message': 'Método encontrado com sucesso', 'payment_method': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar método de pagamento!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_payment_method(self, request):
        data = request.data
        try:
            payment_method = PaymentMethods.objects.get(id=data['payment_method_id'])
            payment_method.delete()
            return Response({'message': 'Método deletado com sucesso'}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Método de pagamento não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar método de pagamento!'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def list_payments_methods(self, request):
        try:
            payment_method = PaymentMethods.objects.all()
            serializer = PaymentMethodsSerializers(payment_method, many=True)
            return Response({'message': 'Métodos de pagamentos encontrados', 'payment_methods': serializer.data}, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'message': 'Erro ao listar tipos de pagamento!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
