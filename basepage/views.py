from django.shortcuts import render
from django.http import HttpResponse
#from .models import ToDoList, Item

# Create your views here.

def index(response):
    return render(response, 'basepage/base.html',{})

def home(response):
    return render(response, 'basepage/home.html',{})
