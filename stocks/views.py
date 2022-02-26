from .util import *
from django.http import HttpResponse
from .models import Stock
from django.views.decorators.csrf import csrf_exempt
import ast
import json
import finnhub

API_KEY = settings.FINNHUB_API_KEY


@csrf_exempt
def get_stocks(request):

    if request.method == 'POST':
        # Decode bytestring
        req = request.body.decode('utf-8')
        # Convert bytestring to dictionary
        stock = ast.literal_eval(req)
        print("stock info from REACT: ", stock)

        # Setup client
        finnhub_client = finnhub.Client(api_key=API_KEY)

        # Stock candles
        response = finnhub_client.stock_candles(
            stock["ticker"], stock["period"], stock["dates"][0], stock["dates"][1])
        print(response)

        return HttpResponse(json.dumps(response))
