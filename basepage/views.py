from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateNewMessage
from django.views.generic import ListView

# from .models import ToDoList, Item

# Create your views here.

def index(response):
    return render(response, 'basepage/base.html', {})


def home(response):
    return render(response, 'basepage/home.html', {})


def contact(response):
    form = CreateNewMessage()
    return render(response, 'basepage/contact.html', {"form":form})


def films(response):
    return render(response, 'basepage/films.html', {})





