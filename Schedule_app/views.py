from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateSchedule, CreateScheduleCinema, TicketBookForm
from django.contrib.auth.models import User


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
    # submitted = False
    # if response.method == "POST":
    #     form = TicketBookForm(response.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect('/book_ticket?submitted=True')
    # else:
    #     form = TicketBookForm
    #     if 'submitted' in response.GET:
    #         submitted = True
    # return render(response, 'bookticket.html', {"form": form, 'submitted': submitted, 'logedin': True})
    else:
        return render(response, 'bookticket.html', {'logedin': False})


def cinema(response):
    form = TicketBookForm(response.GET)
    print(form['cinema'])
    return HttpResponse(form['cinema'])
