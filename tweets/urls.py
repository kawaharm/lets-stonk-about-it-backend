from django.urls import path, include
from rest_framework import routers
from .api import TweetViewSet
from . import views


# Routes
router = routers.DefaultRouter()
router.register(r'api_tweets', TweetViewSet, 'api_tweets')


# Paths
urlpatterns = [
    path('api/tweets/', include(router.urls))
]
