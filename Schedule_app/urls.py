from django.urls import path

from . import views

urlpatterns = [
    # path('schedule_movie/', views.schedule_movie, name='schedule_movie'),
    # path('schedule_movie_cinema/', views.schedule_movie_cinema, name='schedule_movie_cinema'),
    path('book_ticket/', views.bookticket, name='book_ticket'),
    path('cinema/', views.cinema, name='cinema')

]
