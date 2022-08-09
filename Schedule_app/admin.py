from django.contrib import admin
from .models import ScheduledMovies, ScheduleMovieCinema
# Register your models here.
admin.site.register(ScheduledMovies)
admin.site.register(ScheduleMovieCinema)
