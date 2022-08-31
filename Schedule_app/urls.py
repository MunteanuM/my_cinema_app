from django.urls import path

from . import views

from .views import *

urlpatterns = [
    # path('schedule_movie/', views.schedule_movie, name='schedule_movie'),
    # path('schedule_movie_cinema/', views.schedule_movie_cinema, name='schedule_movie_cinema'),
    path('book_ticket/', views.bookticket, name='book_ticket'),
    path('cinema/', views.cinema, name='cinema'),
    path('movie/', views.movie, name='movie'),
    path('hall/', views.hall, name='hall'),
    path('time/', views.time, name='time'),
    path('choose_seats/', views.seats, name='seats'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('confirmbooking/<uidb64>/<token>/', ConfirmBooking.as_view(), name='confirmbooking'),
    path('download_bookings', views.download_csv, name='download_bookings'),

]
