from django.urls import path
from .views import (ShowTask, ShowAllTasks, AddTask,
                   AddComment, UpdateTaskStatus)

app_name = 'tasks'

urlpatterns = [
    path('<int:pk>/', ShowTask.as_view(), name='task_detail'),
    path('all/', ShowAllTasks.as_view(), name='tasks_all'),
    path('add/', AddTask.as_view(), name='add_task'),
    path('<int:pk>/comment/', AddComment.as_view(), name='add_comment'),
    path('<int:pk>/update-status/', UpdateTaskStatus.as_view(), name='update_status'),
]