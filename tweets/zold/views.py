import statistics
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .util import *
from rest_framework import generics
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import re
import numpy as np
import base64
from io import BytesIO
from .models import Tweet
import matplotlib.pyplot as plt


# from matplotlib.figure import Figure
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class TweetList(generics.ListCreateAPIView):
    '''
    Get a set of tweets, or create new tweets
    '''
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def post(self, request):
        print('FROM FRONTEND: ', request)
        url = "https://api.twitter.com/2/tweets/search/recent?query=aapl%20%23aapl&start_time=2022-01-22T00:00:00.000Z&end_time=2022-01-28T13:00:00.000Z&max_results=100&sort_order=recency&tweet.fields=created_at"
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

        # x = np.array(x_order)
        # y = np.array(avg_scores)
        plt.switch_backend('AGG')   # Set matplotlib backend so we can use plt
        plt.xticks(x_order, dates, rotation="vertical")
        plt.figure(figsize=(10, 5))
        plt.title('Average Sentiment Score for Tweets')
        plt.xlabel('Date')
        plt.ylabel('Average Compound Score')
        plt.plot(x_order, avg_scores)
        plt.savefig('saved_fig.png')
        plotfinal = create_graph()
        html_graph = 'data:image/png;base64, {}'.format(
            plotfinal)

        return Response(html_graph)

        # # Generate plot
        # fig = Figure()
        # axis = fig.add_subplot(1, 1, 1)
        # axis.set_title("title")
        # axis.set_xlabel("x-axis")
        # axis.set_ylabel("y-axis")
        # axis.grid()
        # axis.plot(range(5), range(5), "ro-")

        # # Convert plot to PNG image
        # pngImage = BytesIO()
        # FigureCanvas(fig).print_png(pngImage)

        # # Encode PNG image to base64 string
        # pngImageB64String = "data:image/png;base64,"
        # pngImageB64String += base64.b64encode(
        #     pngImage.getvalue()).decode('utf8')

        # return Response(pngImageB64String)

        # x = np.arange(0, 10, 0.1)
        # y = np.sin(x)

        # plt.switch_backend('AGG')   # Set matplotlib backend so we can use plt
        # plt.plot(x, y)
        # plt.savefig('saved_fig.png')


# XY PLOTS:  {'2022-01-27': 0.3818, '2022-01-24': -1.0386, '2022-01-23': 0.9399, '2022-01-22': -0.7904, '2022-01-21': -0.4121}
