from django.shortcuts import render
from .models.physical_copy import PhysicalCopy
from .models.book import Book
from .models.publisher import Publisher
from .models.borrow import Borrow
from rest_framework import generics
from .serializers import BookSerializer, PublisherSerializer, BorrowSerializer


# Yayıncıların ve kitapların listelenmesi için Görünümler
class PublisherListView(generics.ListCreateAPIView):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Kitap ödünç alma ve iade işlemleri
class BorrowBookView(generics.CreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

class ReturnBookView(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.return_book()

def dashboard(request):
    return render(request, 'components/base.html')

def login(request):
    return render(request, 'pages/login.html')

def change_password(request):
    return render(request, 'pages/change-password.html')

def logout(request):
    return render(request, 'pages/logout.html')

def signup(request):
    return render(request, 'pages/signup.html')

def profile(request):
    return render(request, 'pages/profile.html')

def update_profile(request):
    return render(request, 'pages/update-profile.html')

def books(request):
    return render(request, 'pages/books.html')

def book_detail(request):
    return render(request, 'pages/book-detail.html')

def borrow(request):
    return render(request, 'pages/borrow.html')

def return_book(request):
    return render(request, 'pages/return-book.html')

def publishers(request):
    return render(request, 'pages/publishers.html')

def publisher_detail(request):
    return render(request, 'pages/publisher-detail.html')

def authors(request):
    return render(request, 'pages/authors.html')

def author_detail(request):
    return render(request, 'pages/author-detail.html')

def genres(request):
    return render(request, 'pages/genres.html')

def genre_detail(request):
    return render(request, 'pages/genre-detail.html')

def search(request):
    return render(request, 'pages/search.html')

def contact(request):
    return render(request, 'pages/contact.html')

def about(request):
    return render(request, 'pages/about.html')

