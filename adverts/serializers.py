from rest_framework import serializers
from .models import Adverts


class AdvertsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Adverts
        fields = '__all__'