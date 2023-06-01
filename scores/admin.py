from django.contrib import admin
from .models import GardenScore


@admin.register(GardenScore)
class GardenScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'garden', 'score']
