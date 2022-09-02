import django_filters

from .models import ScheduleMovieCinema


class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = ScheduleMovieCinema
        fields = '__all__'
