from django.urls import path
from . import views

urlpatterns = [
    path('publishers/', views.PublisherListView.as_view(), name='publisher-list'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('borrow/', views.BorrowBookView.as_view(), name='borrow-book'),
    path('return/<int:pk>/', views.ReturnBookView.as_view(), name='return-book'),
]
