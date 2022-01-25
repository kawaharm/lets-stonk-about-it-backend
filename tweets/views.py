from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Tweet


def index(request):
    tweet_list: Tweet.objects.all()
    context = {
        'tweet_list': tweet_list,
    }
    return render(request, 'tweets/index.html', context)
