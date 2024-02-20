from django.contrib import admin
from .models import Notes, NotesVersionHistory
# Register your models here.
admin.site.register(Notes)
admin.site.register(NotesVersionHistory)