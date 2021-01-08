"""Tag model Module"""
from django.db import models
from django.contrib.auth.models import User


class Tags(models.Model):
    """Tag database model"""
    label = models.CharField(max_length=25)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
