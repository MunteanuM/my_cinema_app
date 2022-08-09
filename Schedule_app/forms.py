from django import forms
from django.forms import ModelForm
from .models import ScheduledMovies, ScheduleMovieCinema


class CreateSchedule(ModelForm):
    class Meta:
        model = ScheduledMovies
        fields = '__all__'


class CreateScheduleCinema(ModelForm):
    class Meta:
        model = ScheduleMovieCinema
        fields = '__all__'
