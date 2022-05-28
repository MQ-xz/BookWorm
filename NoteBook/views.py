from distutils.log import Log
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from .forms import *
from django.utils.text import slugify
import string
import random
import json
from .REngine.GPT import getRecommendation


# Create your views here.

def home(request):
    return render(request=request, template_name="index.html")


def index(request):
    if request.user.is_authenticated:
        notes = note.objects.filter(owner=request.user)
        context = {
            'user': request.user,
            'notes': notes
        }
        if notes:
            last_edited = note.objects.filter(owner=request.user).order_by('-updated_at')[0].url
            return redirect('note', last_edited)
        return render(request=request, template_name="Main/index.html", context=context)
    else:
        return render(request=request, template_name="index.html")


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
                return redirect('index')
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
            form.save()
            # login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            print(form.error_messages)
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
        Note = note.objects.get(id=3)
        form = NoteForm(instance=Note)
        return render(request, 'Note/new.html', {'form': form})

    def post(self, request):
        url = slugify(request.POST['title'] + '-' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)))
        try:
            note.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                owner_id=request.user.id,
                url=url
            )
            return redirect(f'note/{url}?mode=edit')
        except Exception as e:
            return HttpResponse(e)


class Note(View):
    def get(self, request, link):
        try:
            mode = request.GET['mode']
        except Exception:
            mode = 'view'
        try:
            noteData = note.objects.get(url=link)
        except Exception:
            context = {
                'errorMessage': '404: Note not found.',
            }
            return render(request, 'Note/error.html', context=context, status=404)

        visibilityForm = NoteVisibilityForm(instance=noteData)
        noteUsersForm = NoteUserForm(instance=noteData)
        context = {
            'note': noteData,
            'url': link,
            'visibilityForm': visibilityForm,
            'noteUsersForm': noteUsersForm,
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
            context['mode'] = mode
            context['users'] = noteUser.objects.filter(note=noteData)
            if mode == 'edit':
                context['form'] = NoteForm(instance=noteData)
                return render(request, 'Note/index.html', context=context)
            else:
                context['form'] = NoteForm()
                return render(request, 'Note/index.html', context=context)
        elif noteData.visibility == 'private' and user:
            context['visibility'] = 'private view only'
            return render(request, 'Note/view.html', context=context)
        elif noteData.visibility == 'public' or noteData.visibility == 'whitelist':
            context['visibility'] = noteData.visibility
            return render(request, 'Note/view.html', context=context)
        else:
            context = {
                'errorMessage': '403: You do not have access to this note.',
            }
            return render(request, 'Note/error.html', context=context, status=403)

    def post(self, request, link):
        # update note
        try:
            note.objects.filter(url=link).update(content=request.POST['content'])
            return redirect(f'./{link}?mode=edit')
        except Exception as e:
            return HttpResponse(e)


class NoteVisibility(View):
    def post(self, request, link):
        try:
            note.objects.filter(url=link).update(visibility=request.POST['visibility'])
            messages.success(request, "Note visibility updated successfully!")
            return redirect(request.META['HTTP_REFERER'])
        except Exception as e:
            return messages.error(request, e)


# class NoteUser(View):
#     def post(self, request, link):
#         try:
#             noteUser.objects.filter(note=link).update(can_edit=request.POST['can_edit'])
#             return redirect(request.META['HTTP_REFERER'])
#         except Exception as e:
#             return messages.error(request, e)


class Recommendation(View):
    def post(self, request):
        prompt = json.loads(request.body)['content'].replace('<p>', '').replace('</p>', '\n').replace('<br>', '')
        print(prompt)
        data = getRecommendation(prompt.replace('   ', ''))
        # data = [
        #     {
        #         "text": "Python is a high level programming language that is widely used in many different application domains."
        #     },
        #     {
        #         "text": "22Python is a high level programming language that is widely used in many different application domains."
        #     },
        #     {
        #         "text": "23Python is a high level programming language that is widely used in many different application domains."
        #     },
        #     {
        #         "text": "24Python is a high level programming language that is widely used in many different application domains."
        #     }
        # ]
        # data = prompt + 'data'
        # content = ''
        # for i in data.split('\n'):
        #     if i == '':
        #         i = '<br>'
        #     content += '<p>' + i.replace('\n', '') + '</p>'
        # print(content)
        return JsonResponse({'status': 'ok', 'recommends': data})


class Settings(View):
    def get(self, request):
        return HttpResponse('hehe')


class UserSearch(View):
    def get(self, request):
        users = User.objects.filter(username__startswith=request.GET['username'])
        print(users)
        return JsonResponse(list(users.values('username', 'email')), safe=False)


class RemoveUser(View):
    def get(self, request, id):
        try:
            noteUser.objects.get(id=id).delete()
            return redirect(request.META['HTTP_REFERER'])
        except Exception as e:
            return messages.error(request, e)


class NewUser(View):
    def post(self, request, link):
        try:
            user = User.objects.get(username=request.POST['username'])
            noteid = note.objects.get(url=link).id
            print(user.id, noteid)
            noteUser.objects.create(
                note_id=noteid,
                user_id=user.id,
                can_edit=request.POST['role']
            )
            return redirect(request.META['HTTP_REFERER'])
        except Exception as e:
            messages.warning(request, e)
            return redirect(request.META['HTTP_REFERER'])
