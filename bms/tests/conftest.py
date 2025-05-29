from django.utils import timezone

import pytest

from meetings.models import Meeting
from tasks.models import User, Task, Comment, TaskRating
from teams.models import Team


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')


@pytest.fixture
def team(user):
    return Team.objects.create(name='Test Team', admin=user)


@pytest.fixture
def task(user, team):
    return Task.objects.create(title='Test Task', created_by=user, assigned_to=user, responsible_team=team,
                               deadline=timezone.now() + timezone.timedelta(days=1), status='completed')

@pytest.fixture
def comment(task, user):
    return Comment.objects.create(task=task, author=user, text='Test Comment')


@pytest.fixture
def rating(task, user):
    return TaskRating.objects.create(task=task, rated_by=user, score=5)

@pytest.fixture
def meeting(user):
    meeting = Meeting.objects.create(title='Test Meeting', organizer=user, start_time=timezone.now(), end_time=timezone.now() + timezone.timedelta(hours=1))
    meeting.participants.add(user)
    return meeting