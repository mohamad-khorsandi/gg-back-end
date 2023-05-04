from django.contrib import admin
from .models import User, TemporaryUser
from django.contrib.auth.models import Group


@admin.register(TemporaryUser)
class TemporaryUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'created')


admin.site.unregister(Group)
admin.site.register(User)