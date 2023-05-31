from django.contrib import admin

from .models import Plant, PlantImage


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_valid',)


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ('plant',)



