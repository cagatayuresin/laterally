from django.db import models
from .publisher import Publisher
from .author import Author


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_year = models.IntegerField()
    language = models.CharField(max_length=50)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    synopsis = models.TextField()
    short_description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title