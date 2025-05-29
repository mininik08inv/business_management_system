from django.urls import path
from .views import (ShowTask, ShowAllTasks, AddTask,
                    AddComment, UpdateTaskStatus, RateTaskView, UserRatingsView)

app_name = 'tasks'

urlpatterns = [
    path('<int:pk>/', ShowTask.as_view(), name='task_detail'),
    path('<int:pk>/rate/', RateTaskView.as_view(), name='rate_task'),
    path('my-ratings/', UserRatingsView.as_view(), name='user_ratings'),
    path('all/', ShowAllTasks.as_view(), name='tasks_all'),
    path('add/', AddTask.as_view(), name='add_task'),
    path('<int:pk>/comment/', AddComment.as_view(), name='add_comment'),
    path('<int:pk>/update-status/', UpdateTaskStatus.as_view(), name='update_status'),
]