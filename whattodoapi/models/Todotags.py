"""Todotag model Module"""
from django.db import models

class TodoTags(models.Model):
    """Todotag database model"""
    todo = models.ForeignKey("Todos", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tags", on_delete=models.CASCADE)
    