from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateNewMessage
from django.views.generic import ListView
from ratelimit.decorators import ratelimit
from contextlib import closing
import psycopg2
import os
import pandas as pd
import csv
from .models import Movie


# from .models import ToDoList, Item

# Create your views here.
#@ratelimit(key='ip')
#def login(response):
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
    return render(response, 'basepage/contact.html', {"form":form, 'submitted':submitted})

@ratelimit(key='ip')
def films(response):
    return render(response, 'basepage/films.html', {})

@ratelimit(key='ip')
def playing_films(response):
    return render(response, 'basepage/playing_films.html', {})

def import_csv(request):
    file = r'C:\Users\mihamunteanu\DjangoProjects\cinema\imdb_top_1000.csv'
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

     # data = pd.read_csv('imdb_top_1000.csv',sep=',')
     #data.to_sql
     # movies = [
     #     Movie(
     #         poster = data.to_sql[row]['Poster_Link'],
     #         title = data.ix[row]['Series_Title'],
     #         release_year = data.ix[row]['Released_Year'],
     #         certificate = data.ix[row]['Certificate'],
     #         runtime = data.ix[row]['Runtime'],
     #         genre = data.ix[row]['Genre'],
     #         imdb_rating = data.ix[row]['IMDB_Rating'],
     #         description = data.ix[row]['Overview'],
     #         meta_score = data.ix[row]['Meta_score'],
     #         film_director = data.ix[row]['Director'],
     #         star1 = data.ix[row]['Star1'],
     #         star2 = data.ix[row]['Star2'],
     #         star3 = data.ix[row]['Star3'],
     #         star4 = data.ix[row]['Star4'],
     #         votes = data.ix[row]['No_of_Votes'],
     #         gross_earnings = data.ix[row]['Gross'],
     #     )
     #     for row in range (500)
     # ]
     # Movie.objects.bulk_create(movies)

 #  file = r'C:\Users\mihamunteanu\DjangoProjects\cinema\imdb_top_1000.csv'
 #  connections = psycopg2.connect(dbname="cinema_app_db", user="postgres", password=os.getenv("PASSWORD"))
 #  with open(file, 'rb') as csvfile:
 #       # with connections.cursor() as cursor:
 #              cursor.copy_expert( "Copy basepage_movie from {} ".format(csvfile),
 #                  file=csvfile,
 #                  table='basepage_movie', #<-- table name from db
 #                  sep=',',  #<-- delimiter
 #                  columns=(
 #                      'poster',
 #                      'title',
 #                      'release_year',
 #                      'certificate',
 #                      'runtime',
 #                      'genre',
 #                      'imdb_rating',
 #                      'description',
 #                      'meta_score',
 #                      'film_director',
 #                      'star1',
 #                      'star2',
 #                      'star3',
 #                      'star4',
 #                      'votes',
 #                      'gross_earnings',
 #                  )
 #          )
 #  connections.commit()
 #  connections.close()
 #  return HttpResponse('Done!')





