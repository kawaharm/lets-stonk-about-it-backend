from rest_framework import generics
from .serializers import StockSerializer
from .util import *


from .models import Stock


class StockList(generics.ListCreateAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self, request):
        url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2020-06-01/2020-06-17"
        response = execute_polygon_api_call(url)
        print('RESPONSE from views', response)
