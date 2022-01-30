import requests
from django.conf import settings


api_key = settings.POLYGON_API_KEY
BASE_URL = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17?apiKey=cw5qbTXQL5a6GfZ7PXpa34aoVGhBwhZs"


def get_authentication(res):

    res.headers["Authorization"] = f"Bearer {api_key}"
    return res


def execute_polygon_api_call(url):
    response = requests.get(url, auth=get_authentication)
    print('RESPONSE AT EXECUTE: ', response)
    return response.json()
