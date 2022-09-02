from django.urls import path

from . import views
from Schedule_app import views as ticket_app

urlpatterns = [
    # path('login/',views.login,name='login'),
    path('home/', views.home, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('films/', views.films, name='films'),
    path('playing_films/', views.playing_films, name='playing_films'),
    # path('upload_csv/', views.import_csv, name='upload_csv')
    path('book_ticket/', ticket_app.bookticket, name='bookticket'),
    path('movie_details/', views.movie_details, name='movie_details')

]
