from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, QueryDict
from .forms import CreateSchedule, CreateScheduleCinema, TicketBookForm
from django.contrib.auth.models import User
from .models import ScheduleMovieCinema, BookTicket
from basepage.models import SeatModel, City, Cinema, CinemaHall
from django.core.mail import send_mail
from django.conf import settings

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


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
                                                      hall=data['hall'], playing=data['time']).values()
        seats_context = SeatModel.objects.filter(name__icontains='city{}'.format(data['city'])). \
            filter(name__icontains='cinema{}'.format(data['cinema'])) \
            .filter(name__icontains='hall{}'.format(data['hall'])). \
            order_by('id').values()
        reserved_seats = BookTicket.objects.filter(schedule=schedule[0]['id']).values()

        print(seats_context[0])

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
    BookTicket.objects.create(
        seats=seat_list,
        schedule_id=schedule_id,
        user_id=response.user.id
    )
    send_mail(
        subject='Your tickets',
        message='Here are your tickets for seats {} for this movie: {}'.format(seat_list, ScheduleMovieCinema.objects.
                                                                               filter(id=schedule_id)[0]),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[response.user.email]
    )
    return HttpResponse('Booking succesfull! Check your email for your confirmation!')


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
