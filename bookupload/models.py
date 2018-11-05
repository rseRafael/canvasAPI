from django.db import models


class Book(models.Model):
    _name = models.CharField(max_length=500,blank=True, null=True)
    _imgsPath = models.FilePathField(blank=True, null=True)
    _pages = models.BigIntegerField(blank=True, null=True)
    _dirPath = models.FilePathField(blank=True, null=True)
    
class Page(models.Model):
    _book = models.ForeignKey('Book', on_delete=None, blank=True, null=True)
    _page = models.BigIntegerField(blank=True, null=True)
    _filename = models.CharField(max_length=500,blank=True, null=True)


class Markup(models.Model):
    _x = models.BigIntegerField(blank=True, null=True)
    _y = models.BigIntegerField(blank=True, null=True)
    _sizeX = models.BigIntegerField(blank=True, null=True)
    _sizeof = models.BigIntegerField(blank=True, null=True)
    _orgWidth = models.BigIntegerField(blank=True, null=True)
    _orgHeigth = models.BigIntegerField(blank=True, null=True)
    _type = models.CharField(max_length=500,blank=True, null=True)
    _color = models.CharField(max_length=500,blank=True, null=True) 
    _lineWidth = models.BigIntegerField(blank=True, null=True)
    _book = models.ForeignKey('Book', on_delete=None, blank=True, null=True)
    _page = models.ForeignKey('Page', on_delete=None, blank=True, null=True)

