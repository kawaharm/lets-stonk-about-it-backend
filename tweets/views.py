from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TweetSerializer

from .models import Tweet


def hello(request):
    content = {"message": "Hello World"}
    return HttpResponse(content)
