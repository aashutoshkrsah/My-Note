from django.contrib import admin
from .views import Notes, NoteType

# Register your models here.
admin.site.register(Notes)
admin.site.register(NoteType)