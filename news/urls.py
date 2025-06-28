from django.urls import path
from .views import NewsListAPIView

urlpatterns = [
    path('president-news/', NewsListAPIView.as_view(), name='presidentuz-news-list'),
]
