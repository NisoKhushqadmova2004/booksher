from django.urls import path
from .views import *
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view()),
    path('cities/', CityListCreateView.as_view()),
    path('books/', BookListCreateView.as_view()),
    path('books/<int:pk>/', BookDetailView.as_view()),
    path('trades/', TradeListCreateView.as_view()),
    path('trades/<int:pk>/', TradeDetailView.as_view()),
]
