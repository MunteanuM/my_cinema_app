from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('home/',views.home,name='homepage'),
    path('contact/',views.contact,name='contactpage'),
    path('films/',views.films,name='filmspage'),
]