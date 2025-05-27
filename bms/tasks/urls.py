from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path('add-task/', views.AddTask.as_view(), name='add_task'),
    path('task-detail/<int:pk>', views.ShowTask.as_view(), name='task_detail'),
    path('tasks/', views.ShowAllTasks.as_view(), name='logout'),

  ]