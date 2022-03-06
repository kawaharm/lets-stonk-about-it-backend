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

        # Retrieve stock market data from Yahoo Finance
        company = stock['ticker']
        period = stock['period']
        interval = '60m' if period == '1d' else '1d'

        stock_data = yf.download(
            company, period=period, interval=interval)
        print(stock_data)

        def create_graph():
            # Create buffer for saving image of graph
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            # Encode image then decode to utf-8
            encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()  # free buffer memory
            return encoded

        plt.switch_backend('AGG')
        close = stock_data['Close']  # Extract closing prices
        fig, ax = plt.subplots()
        ax.plot(close, color='red')
        plt.title('Stock Performance for ${}'.format(company))
        plt.xlabel('Date')
        plt.xticks(rotation=45)
        plt.ylabel('Closing Price (USD)')
        plt.tight_layout()
        plotfinal = create_graph()
        html_graph = 'data:image/png;base64, {}'.format(
            plotfinal)

        return HttpResponse(html_graph)

        # return HttpResponse(json.dumps(response))
