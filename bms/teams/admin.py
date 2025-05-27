from django.contrib import admin
from teams.models import Team

# Register your models here.

admin.site.register(Team)

# @admin.register(Team)
# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('name', )
#     list_display_links = ('name', )