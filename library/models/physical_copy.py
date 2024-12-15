# models.py

from django.db import models
from django.contrib.auth.models import User
from .book import Book

class PhysicalCopy(models.Model):
    book = models.ForeignKey(Book, related_name='physical_copies', on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    borrowed_by = models.ForeignKey(User, related_name='borrowed_copies', null=True, blank=True, on_delete=models.SET_NULL)
    due_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)  # Yeni alan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} (ID: {self.id})"
