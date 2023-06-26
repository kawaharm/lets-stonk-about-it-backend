import requests
from django.conf import settings
import tweepy

# Bearer token to authorize call to Twitter API
bearer_token = settings.BEARER_TOKEN
consumer_key = settings.API_KEY
consumer_secret = settings.API_SECRET
access_token = settings.ACCESS_TOKEN
access_token_secret = settings.ACCESS_SECRET

BASE_URL = "https://api.twitter.com/2/tweets/search/recent"


def create_url():
    tweet_fields = "tweet.fields=lang,author_id"
    ids = "ids=1278747501642657792,1255542774432063488"
    url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
        ids, tweet_fields)
    return url


def bearer_oauth(res):
    """
    Method required by bearer token authentication.
    """

    res.headers["Authorization"] = f"Bearer {bearer_token}"
    res.headers["User-Agent"] = "v2TweetLookupPython"
    return res


def execute_twitter_api_call(url):
    # response = requests.get(url, auth=bearer_oauth)
    # if response.status_code != 200:
    #     raise Exception(
    #         "Request returned an error: {} {}".format(
    #             response.status_code, response.text
    #         )
    #     )
    # return response.json()

    # client = tweepy.Client(bearer_token=bearer_token)
    client = tweepy.Client(
        consumer_key=consumer_key, consumer_secret=consumer_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

    # Get Users

    # This endpoint/method returns a variety of information about one or more users
    # specified by the requested IDs or usernames

    user_ids = [2244994945, 6253282]

    # By default, only the ID, name, and username fields of each user will be
    # returned
    # Additional fields can be retrieved using the user_fields parameter
    response = client.get_users(
        ids=user_ids, user_fields=["profile_image_url"])

    for user in response.data:
        print(user.username, user.profile_image_url)

    return response


def get_recent_tweets():
    url = create_url()
    return execute_twitter_api_call(url)
