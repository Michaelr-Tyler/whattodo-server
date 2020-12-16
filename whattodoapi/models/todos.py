"""Todo model Module"""
from django.db import models
from django.contrib.auth.models import User


class Todos(models.Model):
    """Todo database model"""
    task = models.CharField(max_length=100)
    urgent = models.IntegerField()
    important = models.IntegerField()
    category = models.OneToOneField("Categories", on_delete=models.CASCADE, unique=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def tags(self):
        """Property to access each todo's associated tag instances
        
        todotags_set is a queryset of posttags objects for which the post instance 
        (aka self)'s primary key exists as that posttag's "post_id" foreign key
        """
        todo_tags = self.todotags_set.all()
        return [ td.tag for td in todo_tags]