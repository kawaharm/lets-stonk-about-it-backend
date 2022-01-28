from rest_framework import generics
from .serializers import StockSerializer
from .util import *


from .models import Stock


class StockList(generics.ListCreateAPIView):

    queryset = Stock.objects.all()
    serializer_class = StockSerializer
