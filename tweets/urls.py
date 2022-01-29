from django.urls import path, include
from . import views


urlpatterns = [
    path('tweets/', views.get_tweets, name="tweets"),
    # path('tweets/<int:pk>/', views.tweet_detail, name="detail"),
]
