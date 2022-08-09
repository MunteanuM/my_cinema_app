from django import forms
from django.forms import ModelForm
from .models import Contact, UploadCsv


class CreateNewMessage(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class UploadFile(forms.Form):
    class Meta:
        model = UploadCsv
        fields = '__all__'
