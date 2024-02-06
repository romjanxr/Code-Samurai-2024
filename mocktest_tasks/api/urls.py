from django.urls import path
from .views import create_read_search_book, fetch_or_update_book

urlpatterns = [
    path('books', create_read_search_book, name='create_book'),
    path('books/<int:pk>', fetch_or_update_book, name='fetch_or_update_by_id'),
]
