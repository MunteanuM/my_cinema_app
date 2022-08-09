from django.db import models


# Create your models here.


class Movie(models.Model):
    poster = models.URLField()
    title = models.CharField(max_length=300)
    release_year = models.CharField(max_length=100)
    certificate = models.CharField(max_length=100)
    runtime = models.CharField(max_length=100)
    genre = models.CharField(max_length=200)
    imdb_rating = models.CharField(max_length=100)
    description = models.TextField()
    meta_score = models.CharField(max_length=100)
    film_director = models.CharField(max_length=300)
    star1 = models.CharField(max_length=300)
    star2 = models.CharField(max_length=300)
    star3 = models.CharField(max_length=300)
    star4 = models.CharField(max_length=300)
    votes = models.CharField(max_length=100)
    gross_earnings = models.CharField(max_length=100)


class SeatModel(models.Model):
    available = models.BooleanField()
    name = models.CharField(max_length=200)


class CinemaHall(models.Model):
    name = models.CharField(max_length=200)
    seats = models.ForeignKey(SeatModel, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Cinema(models.Model):
    address = models.CharField(max_length=200)
    # hall = models.CharField(max_length=200)
    hall = models.ForeignKey(CinemaHall, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__ (self):
        return self.name


class City(models.Model):
    city = models.CharField(max_length=200)
    cinemas = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.city


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
