from django.contrib import admin


from .models import Task, Comment, TaskRating


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'assigned_to', 'deadline', 'status')
    list_display_links = ('title', )



@admin.register(TaskRating)
class TaskRatingAdmin(admin.ModelAdmin):
    list_display = ('task', 'rated_by', 'score')
    list_display_links = ('task', )



