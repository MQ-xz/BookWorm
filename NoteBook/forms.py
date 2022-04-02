from urllib import request
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import *
from django.db.models import Q



class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class NoteForm(ModelForm):
    class Meta:
        model = note
        fields = ['title', 'description', 'content', 'visibility']


class NoteVisibilityForm(ModelForm):
    class Meta:
        model = note
        fields = ['visibility']


class NoteUserForm(ModelForm):
    class Meta:
        model = noteUser
        fields = ['user', 'can_edit']
