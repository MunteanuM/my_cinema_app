import datetime

from django import forms
from django.forms import ModelForm, Select
from .models import ScheduledMovies, ScheduleMovieCinema, BookTicket
from basepage.models import City, Cinema, CinemaHall, Movie
from dynamic_forms import DynamicField, DynamicFormMixin
from datetime import date


class CreateSchedule(ModelForm):
    class Meta:
        model = ScheduledMovies
        fields = '__all__'


class CreateScheduleCinema(ModelForm):
    class Meta:
        model = ScheduleMovieCinema
        fields = '__all__'



class TicketBookForm(DynamicFormMixin, forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
    )

    def cinema_choice(form):
        city = form['city'].value()
        return Cinema.objects.filter(cinemaback__city=city)

    cinema = DynamicField(
        forms.ModelChoiceField,
        queryset=cinema_choice,
    )

    def movie_choice(form):
        cinema = form['cinema'].value()
        city = form['city'].value()
        ScheduledMovies.objects.filter(movieback__cinema=cinema, movieback__city=city)
        return ScheduledMovies.objects.filter(movieback__cinema=cinema, movieback__city=city)

    movie = DynamicField(
        forms.ModelChoiceField,
        queryset=movie_choice,
    )

    def hall_choice(form):
        movie = form['movie'].value()
        cinema = form['cinema'].value()
        city = form['city'].value()
        return CinemaHall.objects.filter(hallback__movie=movie, hallback__cinema=cinema, hallback__city=city)

    hall = DynamicField(
        forms.ModelChoiceField,
        queryset=hall_choice,
    )

    def time_choice(form):
        cinema = form['cinema'].value()
        city = form['city'].value()
        movie = form['movie'].value()
        hall = form['hall'].value()
        return ScheduleMovieCinema.objects.filter(hall=hall, cinema=cinema, city=city, movie=movie,
                                                  playing__gte=datetime.datetime.now()).values_list(
            'playing', flat=True)

    time = DynamicField(
        forms.ModelChoiceField,
        queryset=time_choice,
    )


class Bookings(ModelForm):
    class Meta:
        model = BookTicket
        fields = '__all__'
