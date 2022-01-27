import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TweetSerializer
from rest_framework import generics
from .util import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import statistics


from .models import Tweet


class TweetList(generics.ListCreateAPIView):
    '''
    Get a set of tweets, or create new tweets
    '''
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    # def get(self, request, format=None):
    #     url = "https://api.twitter.com/2/tweets?ids=1278747501642657792,1255542774432063488&tweet.fields=lang,author_id"
    #     response = execute_twitter_api_call(url)
    #     print('RESPONSE: ', response)
    #     print('first id: ', response['data'][0].get('id'))
    #     print('first text: ', response['data'][0].get('text'))

    #     return Response(response)

    def get(self, request):
        url = "https://api.twitter.com/2/tweets/search/recent?max_results=10&tweet.fields=created_at&place.fields=&query=gamestop%20or%20%23gme%20or%20%40gamestop%20-is%3Aretweet"
        response = execute_twitter_api_call(url)
        # Extract text only
        sentences = list(map(lambda s: s.get('text'), response['data']))
        datetime = list(map(lambda t: t.get('created_at'), response['data']))

        '''
        Sentiment Analysis using VADER lexicon.
        Each sentence comprise of a neg, neu, pos, and compound score.
        Compound score is the sum of the valence score of each word,
        Between -1 (most negative) and +1 (most positive).
        '''
        score_array = []
        analyzer = SentimentIntensityAnalyzer()
        for sentence in sentences:
            # Remove url links from text
            sentence = re.sub(r"http\S+", "", sentence)
            vs = analyzer.polarity_scores(sentence)
            print("{:-<65} {}".format(sentence, str(vs)))
            score_array.append(vs)

        print('SCORE ARRAY', score_array)
        total_compound_score = list(
            map(lambda c: c.get('compound'), score_array))
        print('TOTAL COMPOUND: ', total_compound_score)
        mean_compound_score = statistics.mean(total_compound_score)
        print('MEAN SCORE: ', mean_compound_score)

        return Response(mean_compound_score)
