import logging
from django.contrib import admin
from django.urls import path, include


logger = logging.getLogger(__name__)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('', include('core.urls', namespace='core')),
]
