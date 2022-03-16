from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .forms import *


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        notes = note.objects.filter(owner=request.user)
        context = {
            'user': request.user,
            'notes': notes
        }
        return render(request=request, template_name="Main/index.html", context=context)
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
            messages.warning(request, "Invalid username or password.")
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
                messages.warning(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, 'Auth/signup.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "Logged out successfully!")
        return HttpResponseRedirect('login')


class ChangePassword(View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'Auth/password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully!")
            return redirect(index)
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
            return render(request, 'Auth/password.html', {'form': form})


class NewNote(View):
    def get(self, request):
        form = NoteForm()
        return render(request, 'Note/new.html', {'form': form})

    def post(self, request):
        form = NoteForm(request.POST)
        if form.is_valid():
            form.owner_id = request.user.id
            form.save()
        return render(request, 'Note/new.html', {'form': form})


class Note(View):
    def get(self, request, link):
        noteData = note.objects.get(url=link)
        context = {
            'note': noteData,
        }

        try:
            user = noteUser.objects.get(note=noteData, user=request.user)
            user_can_edit = user.can_edit
        except Exception:
            user = False
            user_can_edit = False

        if request.user == noteData.owner or user_can_edit:
            notes = note.objects.filter(owner=request.user)
            context['notes'] = notes
            return render(request, 'Note/index.html', context=context)
        elif noteData.visibility == 'private' and user:
            context['visibility'] = 'private view only'
            return render(request, 'Note/view.html', context=context)
        elif noteData.visibility == 'public' or noteData.visibility == 'whitelist':
            context['visibility'] = noteData.visibility
            return render(request, 'Note/view.html', context=context)
        else:
            return HttpResponse("You don't have access to this note", )
