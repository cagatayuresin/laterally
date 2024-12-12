from django.shortcuts import render, get_object_or_404
from .models.physical_copy import PhysicalCopy
from .models.book import Book
from .models.publisher import Publisher
from .models.borrow import Borrow
from .models.author import Author
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
    books = Book.objects.order_by('?')[:20]
    return render(request, 'pages/books.html', {'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    return render(request, 'pages/book-detail.html' , {'book': book})

def borrow(request):
    return render(request, 'pages/borrow.html')

def return_book(request):
    return render(request, 'pages/return-book.html')

def publishers(request):
    return render(request, 'pages/publishers.html')

def publisher_detail(request, pk):
    return render(request, 'pages/publisher-detail.html')

def authors(request):
    authors = Author.objects.order_by('?')[:20]
    return render(request, 'pages/authors.html', {'authors': authors})

def author_detail(request, pk):
    author = get_object_or_404(Author, id=pk)
    author_books = Book.objects.filter(author=author)
    return render(request, 'pages/author-detail.html', {
        'author': author,
        'author_books': author_books
    })

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

