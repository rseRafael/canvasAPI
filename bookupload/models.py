from django.db import models

class Book(models.Model):
    NAME = models.CharField(max_length=500, blank = True)
    SIZE = models.BigIntegerField(blank = True)
    PATH = models.FilePathField(blank = True )
    

class Object(models.Model):
    X = models.FloatField()
    Y = models.FloatField()
    MODE = models.BooleanField()
    COLOR = models.CharField(max_length = 500)
    WIDTH = models.BigIntegerField()
    SIZE = models.BigIntegerField()
    stack = models.ForeignKey('Stack', on_delete=None)

class Stack(models.Model):
    BOOK  = models.ForeignKey('Book', on_delete=None)