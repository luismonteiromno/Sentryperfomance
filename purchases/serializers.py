from rest_framework import serializers
from .models import BooksPurchases


class BooksPurchasesSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 3
        model = BooksPurchases
        fields = '__all__'
