from rest_framework import serializers
from .models.physical_copy import PhysicalCopy
from .models.book import Book
from .models.publisher import Publisher
from .models.borrow import Borrow

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'created_at', 'updated_at']

class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    physical_copies = serializers.StringRelatedField(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_year', 'language', 'isbn', 'genre', 'publisher', 'synopsis', 'short_description', 'cover_image', 'created_at', 'updated_at', 'physical_copies']

class PhysicalCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalCopy
        fields = ['id', 'book', 'available', 'created_at', 'updated_at']

class BorrowSerializer(serializers.ModelSerializer):
    copy = PhysicalCopySerializer()

    class Meta:
        model = Borrow
        fields = ['id', 'user', 'copy', 'borrow_date', 'return_date']
