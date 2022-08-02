from django import forms
from django.forms import ModelForm
from .models import Contact

class CreateNewMessage(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
