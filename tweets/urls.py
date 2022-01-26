from django.urls import path, include
# from rest_framework import routers
# from .api import TweetViewSet
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('tweets/', views.TweetList.as_view()),
]
