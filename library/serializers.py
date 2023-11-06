from rest_framework import serializers
from .models import Librarys
from adminUsibras.serializers import BooksSerializer


class LibrarysSerializers(serializers.ModelSerializer):
    books_for_sale = serializers.SerializerMethodField()

    def get_books_for_sale(self, obj):
        in_stock_books = obj.books_for_sale.filter(in_stock=True)
        return BooksSerializer(in_stock_books, many=True).data

    class Meta:
        depth = 1
        model = Librarys
        fields = '__all__'
