from django import forms

class CreateNewMessage(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    email = forms.CharField(label="email", max_length=200)
    phone_number = forms.CharField(label="Phone Number", max_length=20)
    city = forms.CharField(label="City", max_length=200)
    subject = forms.CharField(label="Subject", max_length=200)
    message = forms.CharField(label="Message", max_length=200)