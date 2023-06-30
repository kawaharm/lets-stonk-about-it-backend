from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast

from matplotlib import pyplot as plt
import base64
from io import BytesIO
import yfinance as yf
import json
from datetime import datetime


@csrf_exempt
def get_stocks(request):

    if request.method == 'POST':
        # Decode bytestring
        req = request.body.decode('utf-8')
        # Convert bytestring to dictionary
        stock = ast.literal_eval(req)

        # Retrieve stock market data from Yahoo Finance
        company = stock['ticker']
        period = stock['period']
        interval = '60m' if period == '1d' else '1d'

        stock_data = yf.download(
            company, period=period, interval=interval)

        def generate_graph_data(stock_data, interval):
            # Retrieve closing prices in JSON string
            data_json = stock_data['Close'].to_json(
                orient='split')
            # Convert JSON to dict
            data_dict = json.loads(data_json)
            dates = data_dict['index']
            for i in range(len(dates)):
                # Convert epoch time to datetime object
                date_obj = datetime.fromtimestamp(dates[i]//1000)
                if interval == '60m':
                    dates[i] = date_obj.strftime("%H:%M %p")
                else:
                    dates[i] = date_obj.strftime("%Y-%m-%d")
            # Revert back to JSON string
            return json.dumps(data_dict)

        return HttpResponse(generate_graph_data(stock_data, interval))
