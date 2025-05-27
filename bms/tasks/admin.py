from django.contrib import admin


from .models import Task, Comment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to', 'deadline', 'status')
    list_display_links = ('title', )