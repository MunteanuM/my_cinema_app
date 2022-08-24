from django.contrib import admin
from .models import ScheduledMovies, ScheduleMovieCinema
from basepage.models import Cinema
from .forms import CreateScheduleCinema


# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    form = CreateScheduleCinema
    class Media:
        js = ('Schedule_app/js/admindropajax.js',)


admin.site.register(ScheduleMovieCinema, ScheduleAdmin)
admin.site.register(ScheduledMovies)
# admin.site.register(ScheduleMovieCinema)
