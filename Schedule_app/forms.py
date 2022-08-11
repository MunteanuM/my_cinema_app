from django import forms
from django.forms import ModelForm, Select
from .models import ScheduledMovies, ScheduleMovieCinema
from basepage.models import City, Cinema, CinemaHall
from dynamic_forms import DynamicField, DynamicFormMixin


class CreateSchedule(ModelForm):
    class Meta:
        model = ScheduledMovies
        fields = '__all__'


class CreateScheduleCinema(ModelForm):
    class Meta:
        model = ScheduleMovieCinema
        fields = '__all__'


class TicketBookForm(DynamicFormMixin, forms.Form):

    def cinema_choice(form):
        city = form['city'].value()
        return ScheduleMovieCinema.objects.filter(city=city).values_list('cinema__name', flat=True)

    def initial_module(form):
        city = form['city'].value()
        return ScheduleMovieCinema.objects.filter(city=city).values_list('cinema__name', flat=True).first()

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        # ScheduleMovieCinema.objects.values_list('city__city', flat=True).distinct(),
        initial=City.objects.first()
        # ScheduleMovieCinema.objects.values_list('city__city', flat=True).distinct().first()
    )
    cinema = DynamicField(
        forms.ModelChoiceField,
        queryset=cinema_choice,
        initial=initial_module
    )

    # class Meta:
    # model = ScheduleMovieCinema
    # fields = '__all__'
    # choice = ScheduleMovieCinema.objects.all()
    # city_query = ScheduleMovieCinema.objects.values_list('city__city', flat=True).distinct()
    # City = forms.ModelChoiceField(queryset=city_query)
# cinema_query = ScheduleMovieCinema.objects.filter(city__city__in=City.widget.choices())\
# .values_list('cinema__name', flat=True).distinct()
# cinema = forms.ModelChoiceField(queryset=cinema_query)
#
# movie_query = ScheduleMovieCinema.objects.values_list('movie__movie__title', flat=True).distinct()
# movie = forms.ModelChoiceField(queryset=movie_query)
#
# hall_query = ScheduleMovieCinema.objects.values_list('hall__name', flat=True).distinct()
# hall = forms.ModelChoiceField(queryset=hall_query)


# cinema = forms.ModelChoiceField(choice)
# cinema = forms.ModelChoiceField(queryset=ScheduleMovieCinema.cinema)
# hall = forms.ModelChoiceField(queryset=ScheduleMovieCinema.hall)
# movie = forms.ModelChoiceField(queryset=ScheduleMovieCinema.movie)
# playing = forms.ModelChoiceField(queryset=ScheduleMovieCinema.playing)
