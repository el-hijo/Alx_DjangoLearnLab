from rest_framework import serializers
from .models import Author, Book
from datetime import date


"""
    Serializer for the Book model.
    Serializes all fields and adds custom validation
    to ensure publication_year is not in the future.
    """
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = "__all__"
    
    """
        Field-level validation for publication_year.
        Ensures the year is not in the future.
        """
    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year",
                                              "cannot be in the future.")    
 
        return value
    
"""
    Serializer for the Author model.
    Includes the author's name and a nested list of books.
    """    
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ["id","name","books"]
    
    
