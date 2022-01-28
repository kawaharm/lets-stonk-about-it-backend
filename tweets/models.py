from django.db import models


class Tweet(models.Model):
    # stock = models.ForeignKey(
    #     Stock, on_delete=models.CASCADE)  # M:1 association
    message = models.CharField(max_length=280)  # max char in tweet
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    # Compound score from sentiment analysis using vader lexicon
    sentiment_score = models.DecimalField(max_digits=4, decimal_places=3)

    # Print as string representation in Python shell
    def __str__(self):
        return f"{self.message}; {self.date}; {self.time}; {self.sentiment_score}"
