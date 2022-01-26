from .models import Tweet
from rest_framework import viewsets, permissions
from .serializers import TweetSerializer


# Tweet Viewset - for CRUD operations
class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
