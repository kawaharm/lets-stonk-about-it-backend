from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast
import json


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
        # Decode bytestring
        req = request.body.decode('utf-8')
        # Convert bytestring to dictionary
        stock = ast.literal_eval(req)
        print("stock info from REACT: ", stock)

        BASE_URL = "https://api.polygon.io/v2/aggs/"
        url = BASE_URL+"ticker/{}/range/1/day/{}/{}?".format(
            stock["ticker"], stock["dates"][0], stock["dates"][1])
        print('URL', url)
        response = execute_polygon_api_call(url)
        print('response data', response)
        print('response type', type(response))

        return HttpResponse(json.dumps(response))

        # print('FROM REACT: ', name)
        # print('TYPE: ', type(name))
        # q = []
        # for stock in stock_list:
        #     if stock.get('name') == name:
        #         q = stock['keywords']
        # print('Q IS ', q)
        # url = BASE_URL+"".format(
        #     q[0], q[1])
        # response = execute_twitter_api_call(url)
