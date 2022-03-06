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

BASE_URL = "https://api.twitter.com/2/tweets/search/recent"

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
        url = BASE_URL+"?query={}%20%23{}&max_results=100&sort_order=recency&tweet.fields=created_at".format(
            q[0], q[1])
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
        print('AVERAGE SCORE', xy_plots)

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
