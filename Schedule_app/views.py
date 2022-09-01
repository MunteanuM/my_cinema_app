import csv
import datetime

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from .forms import CreateSchedule, CreateScheduleCinema, TicketBookForm
from .models import ScheduleMovieCinema, BookTicket
from basepage.models import SeatModel, City, Cinema
from django.core.mail import send_mail
from django.conf import settings

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib import messages

from .tokens import reservation_confirmation_token
import zoneinfo

gmt = zoneinfo.ZoneInfo('Europe/Bucharest')


# Create your views here.


def schedule_movie(response):
    submitted = False
    if response.method == "POST":
        form = CreateSchedule(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule_movie?submitted=True')
    else:
        form = CreateSchedule
        if 'submitted' in response.GET:
            submitted = True
    return render(response, 'Schedule_app/Schedule_Movies.html', {"form": form, 'submitted': submitted})


def schedule_movie_cinema(response):
    submitted = False
    if response.method == "POST":
        form = CreateScheduleCinema(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/schedule_movie_cinema?submitted=True')
    else:
        form = CreateScheduleCinema
        if 'submitted' in response.GET:
            submitted = True
    return render(response, 'Schedule_app/Schedule_Movies_Cinema.html', {"form": form, 'submitted': submitted})


def bookticket(response):
    if response.user.is_authenticated:
        form = TicketBookForm()
        context = {'form': form}
        return render(response, 'bookticket.html', context)
    else:
        return render(response, 'bookticket.html', {'logedin': False})


def cinema(response):
    form = TicketBookForm(response.GET)
    return HttpResponse(form['cinema'])


def movie(response):
    form = TicketBookForm(response.GET)
    return HttpResponse(form['movie'])


def hall(response):
    form = TicketBookForm(response.GET)
    return HttpResponse(form['hall'])


def time(response):
    form = TicketBookForm(response.GET)
    return HttpResponse(form['time'])


def seats(response):
    if response.user.is_authenticated:
        data = response.POST
        schedule = ScheduleMovieCinema.objects.filter(city=data['city'], cinema=data['cinema'], movie=data['movie'],
                                                      hall=data['hall'], playing=datetime.datetime.strptime(data['time'][0:19], '%Y-%m-%d %H:%M:%S')).values()
        seats_context = SeatModel.objects.filter(name__icontains='city{}'.format(data['city'])). \
            filter(name__icontains='cinema{}'.format(data['cinema'])) \
            .filter(name__icontains='hall{}'.format(data['hall'])). \
            order_by('id').values()
        reserved_seats = BookTicket.objects.filter(schedule=schedule[0]['id'], book_confirmed=True).values()

        for seat in seats_context:
            for i in range(len(reserved_seats)):
                if str(seat['id']) in reserved_seats[i]['seats']:
                    seat['available'] = False
        return render(response, 'chooseseat.html', {'seats': seats_context,
                                                    'initial_seat': seats_context[0],
                                                    'schedule': schedule[0]['id']})
    else:
        return render(response, 'chooseseat.html', {'logedin': False})


def confirmation(response):
    data = response.POST
    reservations = []
    for bookings in data:
        reservations.append(bookings)
    reservations.pop(0)
    reservations.pop(len(reservations) - 1)
    reservations = SeatModel.objects.filter(name__in=reservations).values_list('id', flat=True)
    seat_list = ''
    for seat in reservations:
        seat_list = seat_list + '{}'.format(seat) + ','
    seat_list = seat_list[:len(seat_list) - 1]
    schedule_id = data['schedule_name']
    if 'confirmation' in data:
        BookTicket.objects.create(
            seats=seat_list,
            schedule_id=schedule_id,
            user_id=response.user.id,
            book_confirmed=True
        )
        send_mail(
            subject='Your tickets',
            message='Here are your tickets for seats {} for this movie: {}'.format(seat_list,
                                                                                   ScheduleMovieCinema.objects.
                                                                                   filter(id=schedule_id)[0]),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[response.user.email]
        )
        return HttpResponse('Booking succesfull! Check your email for your confirmation!')
    else:
        user = response.user
        book = BookTicket.objects.create(
            seats=seat_list,
            schedule_id=schedule_id,
            user_id=response.user.id,
            book_confirmed=False,
        )
        current_site = get_current_site(response)
        subject = 'Confirm your booking'
        message = render_to_string('confirmseat.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(book.id)),
            'token': reservation_confirmation_token.make_token(book),
        })
        to_email = user.email
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [to_email]
        )

        return HttpResponse('Check your email to confirm your seats!')


class ConfirmBooking(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            book = BookTicket.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, BookTicket.DoesNotExist):
            book = None
        if book is not None and reservation_confirmation_token.check_token(book, token):
            book.book_confirmed = True
            book.save()
            messages.success(request, ('Your booking has been confirmed.'))
            return redirect('homepage')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('homepage')


class CinemaList(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        city_data = request.data['city']
        cinema_choice = {}
        if city_data:
            cinemas = City.objects.get(id=city_data).cinemas.all().order_by('name')
            cinema_choice = {p.name: p.id for p in cinemas}
        return JsonResponse(data=cinema_choice, safe=False)


class HallList(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        cinema_data = request.data['cinema']
        hall_choice = {}
        if cinema_data:
            halls = Cinema.objects.get(id=cinema_data).halls.all().order_by('name')
            hall_choice = {p.name: p.id for p in halls}
        return JsonResponse(data=hall_choice, safe=False)


def download_csv(request):
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename={}'s Reservation.csv".format(user)
    writer = csv.writer(response)
    writer.writerow(["user", "schedule", "seats"])
    queryset = BookTicket.objects.filter(user=user.id)
    for s in queryset:
        writer.writerow([s.user, s.schedule, s.seats])
    return response
