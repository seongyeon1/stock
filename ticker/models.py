from django.db import models

# Create your models here.

class Ticker(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=32, verbose_name='종목이름')

    def __str__(self):
        return self.name