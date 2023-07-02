from rest_framework import serializers
from .models import Librarys


class LibrarysSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Librarys
        fields = '__all__'
