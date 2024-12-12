from django.db import models
from .book import Book

class PhysicalCopy(models.Model):
    book = models.ForeignKey(Book, related_name='physical_copies', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} (ID: {self.id})"