import statistics
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .util import *
from django.http import HttpResponse
import re
import base64
from io import BytesIO
from .models import Tweet
import matplotlib.pyplot as plt
from django.views.decorators.csrf import csrf_exempt
import sys
from datetime import datetime
import json

# BASE_URL = "https://api.twitter.com/2/tweets/search/recent"
BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"

stock_list = [
    {
        "name": "GME",
        "keywords": ["gamestop", "gme"],
    },
    {
        "name": "AAPL",
        "keywords": ["apple", "aapl"],
    },
    {
        "name": "TSLA",
        "keywords": ["tesla", "tsla"],
    },
    {
        "name": "AMC",
        "keywords": ["amc", "amc"],
    },
    {
        "name": "AMZN",
        "keywords": ["amazon", "amzn"],
    },
    {
        "name": "NVDA",
        "keywords": ["nvidia", "nvda"],
    },
]


def date_converter(date_str):
    input_format = "%a %b %d %H:%M:%S %z %Y"
    output_format = "%Y-%m-%d"

    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, input_format)

    # Format the datetime object to the desired output format
    formatted_date = date_obj.strftime(output_format)

    return formatted_date


@csrf_exempt
def get_tweets(request):

    if request.method == 'POST':
        # Decode json
        name = request.body.decode('utf-8')
        sys.stdout.flush()  # for logging in Heroku
        q = []
        for stock in stock_list:
            if stock.get('name') == name:
                q = stock['keywords']

        # Collect last 500 tweets using pagination
        # Twitter API only allows 100 tweets max per request
        url = BASE_URL+"?q={}%20%23{}&count=100&result_type=mixed&lang=en".format(
            q[0], q[1])
        tweet_collection = []
        response = execute_twitter_api_call(url)
        tweet_collection.append(response)

        ''' Commenting out bc Twitter API v1.1 max count = 100
        # Use next_token to retrieve next 100 tweets
        for i in range(4):
            next_token = response.get("meta", {}).get("next_token")
            if next_token:
                next_url = url + "&next_token=" + next_token
                response = execute_twitter_api_call(next_url)
                tweet_collection.append(response)
        '''

        '''
        Sentiment Analysis using VADER lexicon.
        Each sentence comprise of a neg, neu, pos, and compound score.
        Compound score is the sum of the valence score of each word,
        Between -1 (most negative) and +1 (most positive).
        '''
        analyzer = SentimentIntensityAnalyzer()
        tweets_and_scores = []
        for t in tweet_collection:
            for res in t['statuses']:
                tweet = {}
                tweet["message"] = res.get('text')
                tweet["created_at"] = res.get('created_at')
                # Remove url links from tweet for sentiment analyzer
                rm_links = re.sub(r"http\S+", "", res.get('text'))
                # polarity_scores: ex. {'neg': 0.0, 'neu': 0.929, 'pos': 0.071, 'compound': 0.3818}
                vs = analyzer.polarity_scores(rm_links)
                tweet["compound_score"] = vs['compound']
                tweets_and_scores.append(tweet)

        # Calculating average compound score of tweets_and_scores by date
        xy_plots = {}
        for t in tweets_and_scores:
            # Extract YYYY-MM-DD only
            date = date_converter(t["created_at"])
            score = t["compound_score"]

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
        for date, score in xy_plots.items():
            dates.insert(0, date)
            avg_scores.insert(0, score)

        tweet_data = {}
        tweet_data['dates'] = dates
        tweet_data['avg_scores'] = avg_scores

        return HttpResponse(json.dumps(tweet_data))
