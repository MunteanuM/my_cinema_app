import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateNewMessage, UploadFile
from ratelimit.decorators import ratelimit
import csv
from .models import Movie, MovieTrailer
from django.core.paginator import Paginator
from Schedule_app.models import ScheduledMovies


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
                        if row:
                            _, created = Movie.objects.get_or_create(
                                title=row[0],
                                poster=row[1],
                                description=row[2],
                                release_year=row[3],
                                film_director=row[4],
                                imdb_link=row[5],
                                imdb_id=row[6],
                                imdb_rating=row[7],
                                runtime=row[8],
                            )
                return HttpResponse('Done!')
        else:
            form = UploadFile
            if 'submitted' in request.GET:
                submitted = True
        return render(request, 'basepage/uploadcsv.html', {"form": form, "submitted": submitted})
    else:
        return HttpResponse('Feature unavaliable for standard users!')


def movie_details(request):
    data = request.GET['movie_data']
    movie_data = Movie.objects.filter(title=data)
    video_data = MovieTrailer.objects.filter(imdb_id__in=movie_data.values_list('imdb_id'))
    return render(request, 'basepage/movie_details.html', {"movie": movie_data,
                                                           "trailer": video_data})
