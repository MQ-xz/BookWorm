from django.db import models
from django.contrib.auth.models import User
from django_editorjs import EditorJsField


# Create your models here.
class note(models.Model):

    VISIBILITY = (
        ('public', 'Public'),
        ('private', 'Private'),
        ('whitelist', 'Whitelist'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    content = EditorJsField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.SlugField(max_length=300, unique=True)
    visibility = models.CharField(choices=VISIBILITY, default='private', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class noteUser(models.Model):
    note = models.ForeignKey(note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ["note", "user"]
