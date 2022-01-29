from django.db import models
from django.contrib.postgres.fields import ArrayField


class Tweet(models.Model):
    name = models.CharField(max_length=280)  # max char in tweet
    keywords = ArrayField(models.CharField(max_length=20))

    # Print as string representation in Python shell

    def __str__(self):
        return f"{self.message}; {self.date}; {self.time}; {self.sentiment_score}"
