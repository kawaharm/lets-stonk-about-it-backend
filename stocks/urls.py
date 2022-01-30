from django.urls import path, include
# from rest_framework import routers
# from .api import TweetViewSet
from . import views


urlpatterns = [
    path('', views.get_stocks),
]
