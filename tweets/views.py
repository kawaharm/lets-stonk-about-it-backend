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
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO


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

        '''
        Sentiment Analysis using VADER lexicon.
        Each sentence comprise of a neg, neu, pos, and compound score.
        Compound score is the sum of the valence score of each word,
        Between -1 (most negative) and +1 (most positive).
        '''
        analyzer = SentimentIntensityAnalyzer()
        tweets = []
        for res in response['data']:
            tweet = {}
            tweet["message"] = res.get('text')
            tweet["created_at"] = res.get('created_at')
            # Remove url links from tweet for sentiment analyzer
            rm_links = re.sub(r"http\S+", "", res.get('text'))
            # polarity_scores: ex. {'neg': 0.0, 'neu': 0.929, 'pos': 0.071, 'compound': 0.3818}
            vs = analyzer.polarity_scores(rm_links)
            tweet["compound_score"] = vs['compound']
            tweets.append(tweet)

        # Calculating average compound score of tweets by date
        xy_plots = {}
        for t in tweets:
            plot = t
            date = plot["created_at"].split("T")[0]  # Extract YYYY-MM-DD only
            score = plot["compound_score"]

            # If date exists, append score to list
            if xy_plots.get(date):
                xy_plots[date].append(score)
            else:
                xy_plots[date] = []
                xy_plots[date].append(score)

        # Replace score list with average score
        xy_plots = {date: statistics.mean(score)
                    for date, score in xy_plots.items()}

        # Set up line graph
        dates = []
        avg_scores = []
        x_order = []
        count = 0
        for date, score in xy_plots.items():
            dates.insert(0, date)
            avg_scores.insert(0, score)
            count += 1
            x_order.append(count)

        print('DATES:  ', dates)
        print('AVG SCORE:  ', avg_scores)
        print('x order:  ', x_order)

        def create_graph():
            # Create buffer for saving image of graph
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # Encode image then decode to utf-8
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()  # free buffer memory
            return encoded

        x = np.array(x_order)
        y = np.array(avg_scores)
        plt.switch_backend('AGG')   # Set matplotlib backend so we can use plt
        plt.xticks(x, dates)
        plt.figure(figsize=(10, 5))
        plt.plot(x, y)
        plt.title('Average Sentiment Score for Tweets')
        plt.xlabel('Date')
        plt.ylabel('Average Compound Score')
        plotfinal = create_graph()
        html_graph = '<img src="data:image/png;base64, {}" />'.format(
            plotfinal)

        return Response(html_graph)

# XY PLOTS:  {'2022-01-27': 0.3818, '2022-01-24': -1.0386, '2022-01-23': 0.9399, '2022-01-22': -0.7904, '2022-01-21': -0.4121}
