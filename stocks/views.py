from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast
import json
import finnhub

import datetime as dt
from matplotlib import pyplot as plt
from matplotlib import style
import base64
from io import BytesIO
from pandas_datareader import data as pdr
import yfinance as yf


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
        end = dt.datetime(2019, 1, 2)

        # Retrieve stock market data from Yahoo Finance
        # tesla = pdr.DataReader('TSLA', 'yahoo', start, end, interval='30')
        tesla = yf.download("NVDA", period="5d", interval="30m")
        print(tesla)

        def create_graph():
            # Create buffer for saving image of graph
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # Encode image then decode to utf-8
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()  # free buffer memory
            return encoded

        # tesla['Close'].plot(figsize=(8, 8), label='Tesla')
        plt.switch_backend('AGG')

        close = tesla['Close']
        # ax = close.plot(figsize=(12, 12))
        # ax.set_xlabel('Date')
        # ax.set_ylabel('Closing Price')
        # ax.tight_layout()
        # ax.grid()
        # ax.figure.savefig('stockgraph.png')

        fig, ax = plt.subplots()
        ax.plot(close, color='red')
        # ax.set_xticks(x_order)
        # ax.set_xticklabels(dates, rotation=45)
        plt.title('Stock Graph')
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.ylabel('Price (USD)')
        plt.tight_layout()
        plt.savefig('stockgraph2.png')
        plotfinal = create_graph()
        html_graph = 'data:image/png;base64, {}'.format(
            plotfinal)

        return HttpResponse(html_graph)

        # return HttpResponse(json.dumps(response))
