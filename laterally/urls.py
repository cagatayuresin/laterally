from django.conf.urls.static import static
from django.contrib import admin
from laterally import settings
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from library import views

# API dokümantasyonu için schema view
schema_view = get_schema_view(
   openapi.Info(
      title="Laterally API",
      default_version='v1',
      description="API documentation for Laterally",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@laterally.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),  # Swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),  # ReDoc
    path('', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('password/', views.change_password, name='change-password'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset-password'),
    path('books/', views.books, name='books'),
    path('book/<int:pk>/', views.book_detail, name='book-detail'),
    path('borrow/<int:pk>/', views.borrow_copy, name='borrow-copy'),
    path('return/<int:pk>/', views.return_copy, name='return-copy'),
    path('publishers/', views.publishers, name='publishers'),
    path('publisher/<int:pk>/', views.publisher_detail, name='publisher-detail'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:pk>/', views.author_detail, name='author-detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
