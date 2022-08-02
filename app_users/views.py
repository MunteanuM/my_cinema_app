from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_user(response):
    if response.method == "POST":
        username = response.POST['username']
        password = response.POST['password']
        user = authenticate(response, username=username, password=password)
        if user is not None:
            login(response, user)
            return redirect('homepage')
        else:

            messages.success(response, ("Couldn't find your user, please try again!"))
            return redirect ('login_user')
    else:
        return render(response,'authentication/login.html', {})

def logout_user(response):
    logout(response)
    messages.success(response, ("Logged out..."))
    return redirect('homepage')
