
from django.db import models

# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=200)
    poster = models.URLField()
    description = models.TextField()
    imdb_link = models.URLField()
    imdb_id = models.CharField(max_length=200)
    trailer_url = models.URLField()
    length = models.TimeField()

class Cinema(models.Model):
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    hall = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Cinema_Hall(models.Model):
    name = models.CharField(max_length=200)
    seats = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
