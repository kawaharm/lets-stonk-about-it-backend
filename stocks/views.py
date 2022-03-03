from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast
import json
import finnhub

import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import stylefrom pandas_datareader import data as pdr


API_KEY = settings.FINNHUB_API_KEY


@csrf_exempt
def get_stocks(request):

    if request.method == 'POST':
        # Decode bytestring
        req = request.body.decode('utf-8')
        # Convert bytestring to dictionary
        stock = ast.literal_eval(req)
        print("stock info from REACT: ", stock)

        # interval = ''
        # if stock['period'] == 'D':
        #     interval = '30'

        # # Setup client
        # finnhub_client = finnhub.Client(api_key=API_KEY)

        # # Stock candles
        # response = finnhub_client.stock_candles(
        #     stock["ticker"], "D", stock["dates"][0], stock["dates"][1])
        # print(response)

        start = dt.datetime(2019, 1, 1)
        end = dt.datetime(2020, 8, 14)

        tesla = pdr.DataReader('TSLA', 'yahoo', start, end)
        print(tesla)

        return HttpResponse(json.dumps(response))
