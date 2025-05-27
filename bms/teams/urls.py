from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path('add-team/', views.AddTeam.as_view(), name='add_team'),
    path('team-detail/<int:pk>', views.ShowTeam.as_view(), name='team_detail'),
    path('', views.ShowAllTeams.as_view(), name='teams'),

  ]