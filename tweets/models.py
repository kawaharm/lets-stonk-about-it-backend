from django.db import models

# Create your models here.


class Stock(models.Model):
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=5)
    day_low = models.DecimalField(max_digits=8, decimal_places=2)
    day_high = models.DecimalField(max_digits=8, decimal_places=2)
    day_close = models.DecimalField(max_digits=8, decimal_places=2)
    # Sum of all tweet's sentiment score
    total_sentiment_score = models.DecimalField(max_digits=4, decimal_places=3)


class Tweet(models.Model):
    stock = models.ForeignKey(
        Stock, on_delete=models.CASCADE)  # M:1 association
    message = models.CharField(max_length=280)  # max char in tweet
    date = models.DateField('date')
    time = models.TimeField('time')
    # Compound score from sentiment analysis using vader lexicon
    sentiment_score = models.DecimalField(max_digits=4, decimal_places=3)

    # Print as string representation in Python shell
    def __str__(self):
        return f"{self.message} {self.date} {self.time} {self.sentiment_score}"
