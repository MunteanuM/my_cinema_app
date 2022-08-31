from django.db import models
from basepage.models import Movie, Cinema, CinemaHall, City
from django.contrib.auth.models import User
from django.core.validators import validate_comma_separated_integer_list
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_users.models import NewsletterSub
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User




# Create your models here.


class ScheduledMovies(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, related_query_name='moviepass')

    def __str__(self):
        return self.movie.title


@receiver(post_save, sender=ScheduledMovies, dispatch_uid="send_mail_newsletter")
def newsletter_mail(sender, instance, **kwargs):
    emails = []
    for i in NewsletterSub.objects.filter(subscribed=True):
        emails.append(i.user.email)
    send_mail(
        subject='New film running in cinema',
        message='{} is now running in cinemas'.format(instance.movie),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails
    )


class ScheduleMovieCinema(models.Model):
    movie = models.ForeignKey(ScheduledMovies, on_delete=models.SET_NULL, null=True, related_query_name='movieback')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='city_rel',
                             related_query_name='cityback')
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, related_name='cinema_rel',
                               related_query_name='cinemaback')
    hall = models.ForeignKey(CinemaHall, on_delete=models.SET_NULL, null=True, related_query_name='hallback')
    playing = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.city.city} {self.cinema.name} {self.hall.name} {self.movie} {self.playing}"


class BookTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reservation')
    schedule = models.ForeignKey(ScheduleMovieCinema, on_delete=models.SET_NULL, null=True)
    seats = models.CharField(validators=[validate_comma_separated_integer_list], max_length=200,
                             blank=True, null=True, default='')
    book_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.schedule} {self.seats}"
