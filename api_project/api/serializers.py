from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = "__all__"