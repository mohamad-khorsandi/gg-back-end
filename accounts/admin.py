from django.contrib import admin
from django.contrib.auth.models import Group

from .models import NormalUser, TemporaryUser, GardenOwnerProfile


@admin.register(TemporaryUser)
class TemporaryUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created')


@admin.register(GardenOwnerProfile)
class GardenOwnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'national_id', 'business_id', 'license']


@admin.register(NormalUser)
class NormalUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'password', 'is_garden_owner', 'light_condition', 'have_allergy',
                    'location_type_condition', 'attention_need',
                    'have_pet']


admin.site.unregister(Group)