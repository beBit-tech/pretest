from django.db import models

class Product(models.Model):
    number = models.CharField(max_length = 100, primary_key = True)
    name = models.CharField(max_length = 100)
    price = models.FloatField()