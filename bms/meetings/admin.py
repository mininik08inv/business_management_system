from django.contrib import admin

from meetings.models import Meeting


# Register your models here.

@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time')
    list_display_links = ('title', 'organizer')
