from django.contrib import admin
from .models import NormalUser, TemporaryUser, GardenOwnerProfile
from django.contrib.auth.models import Group


@admin.register(TemporaryUser)
class TemporaryUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created')


@admin.register(GardenOwnerProfile)
class GardenOwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'national_id', 'business_id']


@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'is_garden_owner']


admin.site.unregister(Group)
