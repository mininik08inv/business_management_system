import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from unittest.mock import patch, Mock

from tasks.models import Task
from teams.models import Team

User = get_user_model()

@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1))
    assert task.title == 'Test Task'
    assert task.created_by == user
    assert task.responsible_team == team
    assert task.status == 'open'
    assert task.priority == 'medium'
    assert task.deadline > timezone.now()

@pytest.mark.django_db
def test_task_has_rating():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1))
    assert task.has_rating == False
    task.status = 'completed'
    task.set_rating(user, 5)
    assert task.has_rating == True

@pytest.mark.django_db
def test_task_get_rating():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1))
    assert task.get_rating() is None
    task.status = 'completed'
    task.set_rating(user, 5)
    assert task.get_rating().score == 5

@pytest.mark.django_db
def test_task_set_rating():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1))
    task.status = 'completed'
    rating, created = task.set_rating(user, 5)
    assert rating.score == 5
    assert created == True
    rating, created = task.set_rating(user, 4)
    assert rating.score == 4
    assert created == False

@pytest.mark.django_db
def test_task_set_rating_fail():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1), status='in_progress')
    with pytest.raises(ValidationError):
        task.set_rating(user, 5)

@pytest.mark.django_db
def test_task_is_overdue():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() - timezone.timedelta(days=1))
    assert task.is_overdue() == True
    task = Task.objects.create(title='Test Task', created_by=user, responsible_team=team, deadline=timezone.now() + timezone.timedelta(days=1))
    assert task.is_overdue() == False
