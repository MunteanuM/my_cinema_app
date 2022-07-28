from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CreateNewMessage
from django.views.generic import ListView
from ratelimit.decorators import ratelimit

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





