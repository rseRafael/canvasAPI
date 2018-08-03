from django.db import models

class Book(models.Model):
    NAME = models.CharField(max_length=500)
    TIPO = models.CharField(max_length=500)
    SIZE = models.BigIntegerField()
    DATE = models.FloatField()