from cmath import log
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('login')


class Login(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request=request, template_name="Auth/login.html", context={"form": form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect(index)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
        return render(request=request, template_name="Auth/login.html", context={"form": form})


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'Auth/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(index)
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, 'Auth/signup.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return HttpResponseRedirect('login')
