from rest_framework import serializers
from .models import Adverts, AdvertsViewed, AdvertsBooks


class AdvertsSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Adverts
        fields = '__all__'


class AdvertsViewedSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = AdvertsViewed
        fields = '__all__'


class AdvertsBooksSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdvertsBooks
        fields = '__all__'
