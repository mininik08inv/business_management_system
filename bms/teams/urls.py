from django.urls import path
from .views import (ShowTeam, ShowAllTeams, AddTeam, AddTeamMember, RemoveTeamMember, )

app_name = 'teams'

urlpatterns = [
    path('<int:pk>/', ShowTeam.as_view(), name='team_detail'),
    path('all/', ShowAllTeams.as_view(), name='teams_all'),
    path('add/', AddTeam.as_view(), name='add_team'),
    path('<int:pk>/add-member/', AddTeamMember.as_view(), name='add_member'),
    path('<int:team_pk>/remove-member/<int:user_pk>/', RemoveTeamMember.as_view(), name='remove_member'),
]
