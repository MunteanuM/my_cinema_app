from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.views.generic import View
from .forms import SignUpForm, NewsletterForm
from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.utils.encoding import force_str

from django.core.mail import send_mail
from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from .models import NewsletterSub


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
            return redirect('login_user')
    else:
        return render(response, 'authentication/login.html', {})


def logout_user(response):
    logout(response)
    messages.success(response, ("Logged out..."))
    return redirect('homepage')


# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'authentication/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your CinemaX Account'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [to_email]
            )
            # email = EmailMessage(subject, message, to=[to_email])
            # email.send()
            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('homepage')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account has been confirmed.'))
            return redirect('login_user')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('homepage')


def news_sub(request):
    form = NewsletterForm()
    return render(request, 'newsletter.html', {'form': form})


def subscribe(request):
    data = request.GET.get('email')
    user = User.objects.filter(email__iexact=data)
    for i in user:
        if NewsletterSub.objects.get(user=i):
            NewsletterSub.objects.update(user=i,
                                         subscribed=True)
        else:
            NewsletterSub.objects.create(
                user=i,
                subscribed=True
            )
    return HttpResponseRedirect('/home')


def news_unsub(request):
    unsub = True
    return render(request, 'newsletter.html', {'unsubscribe': unsub})


def unsubscribe(request):
    data = request.user
    user = User.objects.filter(username=data)
    for i in user:
        if NewsletterSub.objects.filter(user=i):
            NewsletterSub.objects.update(
                user=i,
                subscribed=False
            )
        else:
            NewsletterSub.objects.create(
                user=i,
                subscribed=False
            )


    return HttpResponseRedirect('/home')
