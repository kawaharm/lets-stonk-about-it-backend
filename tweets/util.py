import requests
import json
from django.conf import settings

# Bearer token to authorize call to Twitter API
bearer_token = settings.BEARER_TOKEN

BASE_URL = "https://api.twitter.com/2/tweets?"


def create_url():
    tweet_fields = "tweet.fields=lang,author_id"
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    ids = "ids=1278747501642657792,1255542774432063488"
    # You can adjust ids to include a single Tweets.
    # Or you can add to up to 100 comma-separated IDs

    '''
    {'data': [{'lang': 'en',
   'id': '1278747501642657792',
   'text': "It's been a year since Twitter's Developer Labs launched.\n\nAs we build towards the next generation of the #TwitterAPI (coming VERY soon), see what we've learned and changed along the way. https://t.co/WvjuEWCa6G",
   'author_id': '2244994945'},
  {'lang': 'en',
   'id': '1255542774432063488',
   'text': "During these unprecedented times, what’s happening on Twitter can help the world better understand &amp; respond to the pandemic. \n\nWe're launching a free COVID-19 stream endpoint so qualified devs &amp; researchers can study the public conversation in real-time. https://t.co/BPqMcQzhId",
   'author_id': '2244994945'}]}
    '''
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(res):
    """
    Method required by bearer token authentication.
    """

    res.headers["Authorization"] = f"Bearer {bearer_token}"
    res.headers["User-Agent"] = "v2TweetLookupPython"
    return res


def execute_twitter_api_call(url):
    print('BEARER TOKEN: ', bearer_oauth)
    response = requests.get(url, auth=bearer_oauth)
    print('STATUS CODE: ', response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_recent_tweets():
    url = create_url()
    return execute_twitter_api_call(url)
