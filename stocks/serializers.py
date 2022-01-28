from rest_framework import serializers
from .models import Stock


# Stock Serializer
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
