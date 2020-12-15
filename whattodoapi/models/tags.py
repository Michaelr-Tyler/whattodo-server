"""Tag model Module"""
from django.db import models

class Tags(models.Model):
    """Tag database model"""
    label = models.CharField(max_length=25)
