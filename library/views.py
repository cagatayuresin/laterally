from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models.physical_copy import PhysicalCopy
from .models.book import Book
from .models.publisher import Publisher
from .models.borrow import Borrow
from .models.author import Author
from rest_framework import generics
from .serializers import BookSerializer, PublisherSerializer, BorrowSerializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth import get_user_model


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

def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = "Kullanıcı adı veya şifre hatalı."
    return render(request, 'pages/login.html', {'error_message': error_message})

def change_password(request):
    return render(request, 'pages/change-password.html')

def logout_user(request):
    logout(request)
    return redirect('dashboard')


def signup(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        if not username or not email or not password or not password2:
            error_message = "Lütfen tüm alanları doldurun."
        elif password != password2:
            error_message = "Şifreler eşleşmiyor."
        elif User.objects.filter(username=username).exists():
            error_message = "Bu kullanıcı adı zaten kayıtlı."
        elif User.objects.filter(email=email).exists():
            error_message = "Bu e-posta adresi zaten kullanılıyor."
        else:
            # Kullanıcıyı aktif etmeden oluştur
            user = User.objects.create_user(username=username, email=email, password=password, is_active=False)

            # Aktivasyon maili için token üret
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Aktivasyon linkini oluştur
            # Aşağıdaki linki kendi domaininize göre düzenleyin.
            # Örneğin: http://localhost:8000/activate/<uid>/<token>/
            activation_link = f"http://127.0.0.1:8000/activate/{uid}/{token}/"

            subject = "Hesap Aktivasyonunuz"
            message = f"Merhaba {user.username},\n\nHesabınızı aktif etmek için aşağıdaki linke tıklayın:\n{activation_link}\n\nTeşekkürler!"

            # E-posta gönderimi
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            # Kullanıcıyı direkt giriş yaptırmak yerine aktifleşmesini bekliyoruz.
            return render(request, 'pages/signup-confirm.html', {'email': email})

    return render(request, 'pages/signup.html', {'error_message': error_message})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Kullanıcıyı aktif hale getir
        user.is_active = True
        user.save()
        # Kullanıcıyı login yapabilirsiniz
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'pages/activation-invalid.html')


def forgot_password(request):
    success_message = None
    error_message = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            error_message = "Lütfen bir e-posta adresi girin."
        else:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                error_message = "Bu e-posta adresine ait bir kullanıcı bulunamadı."
            else:
                # Kullanıcı bulundu, token üret ve mail gönder
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Bu linki kendi domaininize göre ayarlayın
                reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

                subject = "Şifre Sıfırlama İsteği"
                message = (
                    f"Merhaba {user.username},\n\n"
                    f"Aşağıdaki linke tıklayarak şifrenizi sıfırlayabilirsiniz:\n{reset_link}\n\n"
                    f"Teşekkürler!"
                )

                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

                success_message = "Şifre sıfırlama bağlantısı e-posta adresinize gönderildi. Lütfen e-postanızı kontrol edin."

    return render(request, 'pages/forgot-password.html', {
        'success_message': success_message,
        'error_message': error_message
    })


def reset_password_view(request, uidb64, token):
    error_message = None
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Token kontrolü
    if user is None or not default_token_generator.check_token(user, token):
        # Token geçersizse veya kullanıcı yoksa hata döndür
        return render(request, 'pages/activation-invalid.html', {
            'error_message': 'Geçersiz ya da süresi geçmiş bir bağlantı kullanıyorsunuz.'
        })

    # GET isteğinde formu göster
    if request.method == 'GET':
        return render(request, 'pages/reset-password.html', {
            'error_message': error_message
        })

    # POST isteğinde yeni şifreleri al
    if request.method == 'POST':
        new_password = request.POST.get('new_password', '').strip()
        new_password2 = request.POST.get('new_password2', '').strip()

        if not new_password or not new_password2:
            error_message = "Lütfen tüm alanları doldurun."
        elif new_password != new_password2:
            error_message = "Şifreler eşleşmiyor."
        else:
            # Şifreyi güncelle
            user.set_password(new_password)
            user.save()
            # Kullanıcıyı giriş yaptırmak isterseniz:
            login(request, user)
            return redirect('home')  # Yeni şifre ayarlandıktan sonra yönlendirme

        return render(request, 'pages/reset-password.html', {
            'error_message': error_message
        })

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
    publishers = Publisher.objects.order_by('?')[:20]
    return render(request, 'pages/publishers.html', {'publishers': publishers})

def publisher_detail(request, pk):
    publisher = get_object_or_404(Publisher, id=pk)
    publisher_books = Book.objects.filter(publisher=publisher)
    return render(request, 'pages/publisher-detail.html', {
        'publisher': publisher,
        'publisher_books': publisher_books
    })

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

