from django.contrib import admin

from .models import Robot


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'serial', 'model', 'version', 'created')
    search_fields = ('serial', 'model', 'version')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Robot, PostAdmin)
