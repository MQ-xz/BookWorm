from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),

    path('login', Login.as_view(), name='login'),
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', Logout.as_view(), name='logout'),
    path('changePassword', ChangePassword.as_view(), name='changePassword'),

    path('newNote', NewNote.as_view(), name='newNote'),
    path('note/<slug:link>', Note.as_view(), name='note'),
    path('updateNote/<slug:link>', UpdateNote.as_view(), name='updateNote'),
    path('NoteVisibility/<slug:link>', NoteVisibility.as_view(), name='NoteVisibility'),
    path('NoteUser/<slug:link>', NoteUser.as_view(), name='NoteUser'),

    path('settings', Settings.as_view(), name='settings')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
