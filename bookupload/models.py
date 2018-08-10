from django.db import models

class Book(models.Model):
    NAME = models.CharField(max_length=500,)
    SIZE = models.BigIntegerField()
    imgsPATH = models.FilePathField(blank=True, null=True)
    capaPATH = models.FilePathField(blank=True, null=True)
    PAGES = models.BigIntegerField(blank=True, null=True)
    
class Page(models.Model):
    BOOK = models.ForeignKey('Book', on_delete=None, blank=True, null=True)
    NUMERO = models.BigIntegerField()
    PAGINA = models.CharField(max_length=500, blank = True, null = True)


class Object(models.Model):
    X = models.FloatField()
    Y = models.FloatField()
    MODE = models.BooleanField()
    COLOR = models.CharField(max_length = 500)
    WIDTH = models.BigIntegerField()
    SIZE = models.BigIntegerField()
    BOOK = models.ForeignKey('Book', on_delete=None, blank=True, null=True)
    PAGE = models.ForeignKey('Page', on_delete=None, blank=True, null=True)

