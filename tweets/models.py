from django.db import models

# Create your models here.


class Tweet(models.Model):
    message = models.CharField(max_length=280)  # max char in tweet
