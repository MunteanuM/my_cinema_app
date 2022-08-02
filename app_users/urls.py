from django.urls import path, include
from django.contrib import admin
from .views import SignUpView, ActivateAccount

from . import views

urlpatterns = [
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/',views.logout_user, name="logout_user"),
   # path('register_user/', views.register_user, name="register_user"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
]
