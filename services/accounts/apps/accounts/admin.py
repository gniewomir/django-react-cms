from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from .models import User, ElevatedToken, IdentityToken


class IdentityTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


class ElevatedTokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created')
    fields = ('user',)
    ordering = ('-created',)


admin.site.register(ElevatedToken, ElevatedTokenAdmin)
admin.site.register(IdentityToken, IdentityTokenAdmin)
admin.site.register(Permission)
admin.site.register(User, UserAdmin)
