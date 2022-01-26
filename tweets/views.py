from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TweetSerializer
from rest_framework import generics
from .util import *


from .models import Tweet


class TweetList(generics.ListCreateAPIView):
    '''
    Get a set of tweets, or create new tweets
    '''
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def get(self, request, format=None):
        url = "https://api.twitter.com/2/tweets?ids=1278747501642657792,1255542774432063488&tweet.fields=lang,author_id"
        response = execute_twitter_api_call(url)
        print('RESPONSE: ', response)
        print('first id: ', response['data'][0].get('id'))
        print('first text: ', response['data'][0].get('text'))

        return Response(response)
