from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast
import json
import finnhub

API_KEY = settings.FINNHUB_API_KEY


stock_list = [
    {
        "name": "gme",
        "keywords": ["gamestop", "gme"],
    },
    {
        "name": "aapl",
        "keywords": ["apple", "aapl"],
    },
]


@csrf_exempt
def get_stocks(request):

    if request.method == 'POST':
        # # Decode bytestring
        # req = request.body.decode('utf-8')
        # # Convert bytestring to dictionary
        # stock = ast.literal_eval(req)
        # print("stock info from REACT: ", stock)

        # BASE_URL = "https://api.polygon.io/v2/aggs/"
        # url = BASE_URL+"ticker/{}/range/1/day/{}/{}".format(
        #     stock["ticker"], stock["dates"][0], stock["dates"][1])
        # print('URL', url)
        # response = execute_polygon_api_call(url)
        # print('response data', response)
        # print('response type', type(response))

        # return HttpResponse(json.dumps(response))

        # Decode bytestring
        req = request.body.decode('utf-8')
        # Convert bytestring to dictionary
        stock = ast.literal_eval(req)
        print("stock info from REACT: ", stock)

        # Setup client
        finnhub_client = finnhub.Client(api_key=API_KEY)

        # Stock candles
        response = finnhub_client.stock_candles(
            'AAPL', 'D', 1645753154, 1645753154)
        print(response)

        return HttpResponse(json.dumps(response))
