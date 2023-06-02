from django.contrib import admin
from .models import Garden


@admin.register(Garden)
class GardenAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'business_code', 'avg_score','id')
