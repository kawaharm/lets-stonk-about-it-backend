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

        print(q)

        # Collect last 500 tweets using pagination
        # Twitter API only allows 100 tweets max per request
        url = BASE_URL+"?q={}%20%23{}&count=100&result_type=mixed&lang=en".format(
            q[0], q[1])
        tweet_collection = []
        response = execute_twitter_api_call(url)
        tweet_collection.append(response)
        print(len(tweet_collection[0]["statuses"]))

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
            for res in t['data']:
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
        # print('AVERAGE SCORE', xy_plots)

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
        # print('DATES', dates)
        # print('X_ORDER', x_order)

        def create_graph():
            # Create buffer for saving image of graph
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # Encode image then decode to utf-8
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()  # free buffer memory
            return encoded

        plt.switch_backend('AGG')   # Set matplotlib backend so we can use plt
        fig, ax = plt.subplots()
        ax.plot(x_order, avg_scores)
        ax.set_xticks(x_order)
        ax.set_xticklabels(dates, rotation=45)
        plt.title('Average Sentiment for ${}'.format(name))
        plt.xlabel('Date')
        plt.ylabel('Average Compound Score')
        plt.tight_layout()
        plotfinal = create_graph()
        html_graph = 'data:image/png;base64, {}'.format(
            plotfinal)

        return HttpResponse(html_graph)
