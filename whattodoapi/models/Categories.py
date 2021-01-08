"""Category model Module"""
from django.db import models

class Categories(models.Model):
    """Category database model"""
    label = models.CharField(max_length=25)
