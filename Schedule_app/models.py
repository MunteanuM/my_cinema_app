from django.db import models
from basepage.models import Movie, Cinema, CinemaHall, City, SeatModel
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list



# Create your models here.


class ScheduledMovies(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, related_query_name='moviepass')

    def __str__(self):
        return self.movie.title


class ScheduleMovieCinema(models.Model):
    movie = models.ForeignKey(ScheduledMovies, on_delete=models.SET_NULL, null=True, related_query_name='movieback')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_query_name='cityback')
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, related_query_name='cinemaback')
    hall = models.ForeignKey(CinemaHall, on_delete=models.SET_NULL, null=True, related_query_name='hallback')
    playing = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.city.city} {self.cinema.name} {self.hall.name} {self.movie} {self.playing}"


class BookTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    schedule = models.ForeignKey(ScheduleMovieCinema, on_delete=models.SET_NULL, null=True)
    seats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200,
                             blank=True, null=True, default='')

