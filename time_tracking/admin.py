#time_tracking/models.py
from django.contrib import admin
from .models import Time_Entry, Project

# Register your models here.

admin.site.register(Project)
admin.site.register(Time_Entry)