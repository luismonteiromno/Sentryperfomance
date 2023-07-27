from rest_framework import serializers
from .models import Books, Companys


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Books
        fields = '__all__'


class CompanysSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Companys
        fields = '__all__'
