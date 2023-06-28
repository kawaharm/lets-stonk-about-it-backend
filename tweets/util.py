import requests
from django.conf import settings

# Bearer token to authorize call to Twitter API
bearer_token = settings.BEARER_TOKEN

# def create_url():
#     tweet_fields = "tweet.fields=lang,author_id"
#     ids = "ids=1278747501642657792,1255542774432063488"
#     url = "https://api.twitter.com/2/tweets/search/recent?{}&{}".format(
#         ids, tweet_fields)
#     return url


def bearer_oauth(res):
    """
    Method required by bearer token authentication.
    """

    res.headers["Authorization"] = f"Bearer {bearer_token}"
    res.headers["User-Agent"] = "v1TweetLookupPython"
    return res


def execute_twitter_api_call(url):
    response = requests.get(url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()
