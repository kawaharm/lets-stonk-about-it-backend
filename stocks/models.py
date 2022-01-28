from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=50)
    ticker = models.CharField(max_length=5)
    day_low = models.DecimalField(max_digits=8, decimal_places=2)
    day_high = models.DecimalField(max_digits=8, decimal_places=2)
    day_close = models.DecimalField(max_digits=8, decimal_places=2)

    # Print as string representation in Python shell

    def __str__(self):
        return f"{self.name}; {self.ticker}; {self.day_low};  {self.day_high}; {self.day_close};"
