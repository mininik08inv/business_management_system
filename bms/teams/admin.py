from django.contrib import admin
from .models import Team, TeamMember

class TeamMemberInline(admin.TabularInline):  # или admin.StackedInline
    model = TeamMember
    extra = 1  # Количество пустых форм для добавления

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline]
    list_display = ['name', 'admin']
    filter_horizontal = ['members']  # Если хотите удобный интерфейс выбора участников

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'role']
    list_filter = ['team', 'role']