import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone

from tasks.models import Task, Comment, TaskRating
from teams.models import Team

User = get_user_model()


@pytest.mark.django_db
def test_task_all(client, user):
    client.login(username='testuser', password='1testpasswordA')
    response = client.get(reverse('tasks:tasks_all'))
    assert response.status_code == 200
    assert 'tasks/tasks_all.html' in [template.name for template in response.templates]
    assert 'Мои задачи' in str(response.content.decode('utf-8'))


def test_task_all_unauthenticated(client):
    response = client.get(reverse('tasks:tasks_all'))
    assert response.status_code == 302
    assert response.url == '/users/login/?next=/tasks/all/'


@pytest.mark.django_db
def test_task_detail_page(client, user, team, task):
    client.login(username='testuser', password='1testpasswordA')
    response = client.get(reverse('tasks:task_detail', kwargs={'pk': task.id}))
    assert response.status_code == 200
    assert 'tasks/task_detail.html' in [template.name for template in response.templates]
    assert 'Test Task' in str(response.content.decode('utf-8'))


@pytest.mark.django_db
def test_add_task(client):
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    team = Team.objects.create(name='Test Team', admin=user)
    client.login(username='testuser', password='1testpasswordA')
    data = {'title': 'Test Task', 'description': 'This is a test task.',
            'deadline': timezone.now() + timezone.timedelta(days=1), 'responsible_team': team.id}
    response = client.post(reverse('tasks:add_task'), data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comment_creation(user, team, task, comment):
    assert comment.task == task
    assert comment.author == user
    assert comment.text == 'Test Comment'
    assert comment.created_at <= timezone.now()


@pytest.mark.django_db
def test_comment_str(user, team, task, comment):
    assert str(comment) == f'Комментарий от {user} к задаче {task.id}'


@pytest.mark.django_db
def test_task_rating_creation(user, team, task, rating):
    assert rating.task == task
    assert rating.rated_by == user
    assert rating.score == 5
    assert rating.feedback == ''
    assert rating.rated_at <= timezone.now()


@pytest.mark.django_db
def test_task_rating_str(user, team, task, rating):
    assert str(rating) == f"Оценка 5 для задачи #{task.id}"


@pytest.mark.django_db
def test_task_rating_clean_fail(user, team, task, rating):
    with pytest.raises(ValidationError):
        rating.clean()


@pytest.mark.django_db
def test_task_rating_clean_fail2(user, team, task, rating):
    user.role = 'user'
    user.save()
    with pytest.raises(ValidationError):
        rating.clean()


@pytest.mark.parametrize('period, period_days', [('week', 7), ('month', 30), ('year', 365)])
@pytest.mark.django_db
def test_user_ratings_view_period(client, user, period, period_days):
    client.login(username='testuser', password='1testpasswordA')
    response = client.get(reverse('tasks:user_ratings'), {'period': period})
    assert response.status_code == 200
    assert 'tasks/user_ratings.html' in [template.name for template in response.templates]
    assert response.context['period'] == period
    assert len(response.context['ratings']) == len(
        user.get_user_ratings(timezone.now() - timezone.timedelta(days=period_days)))
    assert response.context['average_rating'] == user.get_average_rating(
        timezone.now() - timezone.timedelta(days=period_days))


@pytest.mark.django_db
def test_user_ratings_view_default(client, user):
    client.login(username='testuser', password='1testpasswordA')
    response = client.get(reverse('tasks:user_ratings'))
    assert response.status_code == 200
    assert 'tasks/user_ratings.html' in [template.name for template in response.templates]
    assert response.context['period'] == 'month'
    assert len(response.context['ratings']) == len(user.get_user_ratings())
    assert response.context['average_rating'] == user.get_average_rating()
