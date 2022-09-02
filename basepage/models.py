from django.db import models

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=300)
    poster = models.URLField()
    description = models.TextField()
    release_year = models.CharField(max_length=100)
    film_director = models.CharField(max_length=300)
    imdb_link = models.URLField()
    imdb_id = models.CharField(max_length=100)
    imdb_rating = models.CharField(max_length=100)
    runtime = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class MovieTrailer(models.Model):
    imdb_id = models.CharField(max_length=200)
    trailer_id = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, related_name='movie')

    def __str__(self):
        return self.imdb_id


class City(models.Model):
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.city


class Cinema(models.Model):
    address = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='cinemas')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    name = models.CharField(max_length=200)
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, related_name='halls')
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SeatModel(models.Model):
    available = models.BooleanField()
    name = models.CharField(max_length=200)
    hall = models.ForeignKey(CinemaHall, on_delete=models.SET_NULL, null=True, related_query_name='seatback')

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField("Name", max_length=200)
    email = models.CharField("email", max_length=200)
    phone_number = models.CharField("Phone Number", max_length=20)
    city = models.CharField("City", max_length=200)
    subject = models.CharField("Subject", max_length=200)
    message = models.CharField("Message", max_length=200)

    def __str__(self):
        return self.name


class UploadCsv(models.Model):
    file = models.CharField("file", max_length=300)

    def __str__(self):
        return self.file
