from django.contrib import admin
from .models import *


# Register your models here.
myModels = [note, noteUser]
admin.site.register(myModels)
