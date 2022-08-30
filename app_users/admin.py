from django.contrib import admin
from .forms import NewsletterForm
from .models import NewsletterSub

admin.site.register(NewsletterSub)
# Register your models here.
