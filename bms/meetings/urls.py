from django.urls import path
from .views import MeetingListView, MeetingCreateView, MeetingUpdateView, MeetingCancelView, MeetingDetailView

app_name = 'meetings'

urlpatterns = [
    path('', MeetingListView.as_view(), name='list'),
    path('new/', MeetingCreateView.as_view(), name='create'),
    path('<int:pk>/', MeetingDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', MeetingUpdateView.as_view(), name='update'),
    path('<int:pk>/cancel/', MeetingCancelView.as_view(), name='cancel'),
]
