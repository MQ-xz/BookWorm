from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('home', home, name='home'),
    path('login', Login.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', Logout.as_view(), name='logout'),
    path('changePassword', ChangePassword.as_view(), name='changePassword'),

    path('newNote', NewNote.as_view(), name='newNote'),
    path('note/<slug:link>', Note.as_view(), name='note'),
    path('NoteVisibility/<slug:link>', NoteVisibility.as_view(), name='NoteVisibility'),
    path('NoteUser/<slug:link>', NewUser.as_view(), name='NewUser'),

    path('removeUser/<int:id>', RemoveUser.as_view(), name='removeUser'),

    path('recommendation', Recommendation.as_view(), name='recommendation'),

    path('users', UserSearch.as_view(), name='userSearch'),

    path('settings', Settings.as_view(), name='settings')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
