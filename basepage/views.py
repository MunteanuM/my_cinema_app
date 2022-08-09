import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateNewMessage, UploadFile
from django.views.generic import ListView
from ratelimit.decorators import ratelimit
import os
import csv
from .models import Movie, SeatModel
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from Schedule_app.models import ScheduledMovies
from datetime import date

# from .models import ToDoList, Item

# Create your views here.
# @ratelimit(key='ip')
# def login(response):
# return render(response, 'basepage/login.html', {})


@ratelimit(key='ip')
def home(response):
    return render(response, 'basepage/home.html', {})


@ratelimit(key='ip', rate='5/h')
def contact(response):
    submitted = False
    if response.method == "POST":
        form = CreateNewMessage(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contact?submitted=True')
    else:
        form = CreateNewMessage
        if 'submitted' in response.GET:
            submitted = True
    return render(response, 'basepage/contact.html', {"form": form, 'submitted': submitted})


@ratelimit(key='ip')
def films(response):
    return render(response, 'basepage/films.html', {})


@ratelimit(key='ip')
def playing_films(response):
    min_date = datetime.datetime.now() + datetime.timedelta(days=7)
    movie_list = ScheduledMovies.objects.filter(end_date__gte=min_date)
    pgn = Paginator(movie_list, 5)
    page = response.GET.get('page')
    movies = pgn.get_page(page)

    return render(response, 'basepage/playing_films.html', {'movie_list': movie_list,
                                                            'movies': movies})


def import_csv(request):
    if request.user.is_superuser:
        submitted = False
        if request.method == "POST":
            form = UploadFile(request.POST)
            if form.is_valid():
                path_csv = form.cleaned_data['file']
                file = r'{}'.format(path_csv)
                with open(file, 'r', encoding='UTF-8') as file:
                    reader = csv.reader(file)
                    next(reader)
                    for row in reader:
                        _, created = Movie.objects.get_or_create(
                            poster=row[0],
                            title=row[1],
                            release_year=row[2],
                            certificate=row[3],
                            runtime=row[4],
                            genre=row[5],
                            imdb_rating=row[6],
                            description=row[7],
                            meta_score=row[8],
                            film_director=row[9],
                            star1=row[10],
                            star2=row[11],
                            star3=row[12],
                            star4=row[13],
                            votes=row[14],
                            gross_earnings=row[15],
                        )
                return HttpResponse('Done!')
        else:
            # if request.method=="GET":
            form = UploadFile
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'basepage/uploadcsv.html', {"form": form, "submitted": submitted})
    else:
        return HttpResponse('Feature unavaliable for standard users!')
