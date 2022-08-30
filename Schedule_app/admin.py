from django.contrib import admin
from .models import ScheduledMovies, ScheduleMovieCinema, BookTicket
from basepage.models import Cinema
from .forms import CreateScheduleCinema


# Register your models here.


class ScheduleAdmin(admin.ModelAdmin):
    form = CreateScheduleCinema
    class Media:
        js = ('Schedule_app/js/admindropajax.js',)


@admin.action(description='Download csv')
def download_data(modeladmin, request, queryset):
    import csv
    f = open('reservations.csv', 'w', encoding="UTF-8")
    writer = csv.writer(f)
    writer.writerow(["user", "schedule", "seats"])
    for s in queryset:
        writer.writerow([s.user, s.schedule, s.seats])


class BookingAdmin(admin.ModelAdmin):
    search_fields = ["user",]
    list_filter = ("user",)
    actions = [download_data]


admin.site.register(BookTicket, BookingAdmin)

admin.site.register(ScheduleMovieCinema, ScheduleAdmin)
admin.site.register(ScheduledMovies)
# admin.site.register(ScheduleMovieCinema)
