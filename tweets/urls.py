from django.urls import path, include
from . import views


urlpatterns = [
    path('tweets/', views.get_tweets, name="tweets"),
    path('threads/', views.get_threads, name="threads")
]
