from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NoteType(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateField( auto_now_add=True)
    updated_at = models.DateField( auto_now=True)

class Notes(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='media/')
    deadline_at = models.DateField( auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(NoteType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateField( auto_now_add=True)
    updated_at = models.DateField( auto_now=True)
    
    