import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from teams.models import Team

User = get_user_model()


@pytest.mark.django_db
def test_show_team(client, user, team, task):
    client.login(username='testuser', password='1testpasswordA')

    response = client.get(reverse('teams:team_detail', kwargs={'pk': team.pk}))
    assert response.status_code == 200
    assert 'teams/team_detail.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_show_all_teams(client, user, team):
    client.login(username='testuser', password='1testpasswordA')
    response = client.get(reverse('teams:teams_all'))
    assert response.status_code == 200
    assert 'teams/teams_all.html' in [template.name for template in response.templates]
    assert response.context['teams'][0] == team


@pytest.mark.django_db
def test_add_team(client, user):
    client.login(username='testuser', password='1testpasswordA')
    response = client.post(reverse('teams:add_team'), {'name': 'New Team', 'user': user})
    assert response.status_code == 302
    assert Team.objects.count() == 1
    assert Team.objects.last().name == 'New Team'
    assert Team.objects.last().admin == user


@pytest.mark.django_db
def test_add_team_member(client, user, team):
    client.login(username='testuser', password='1testpasswordA')
    response = client.post(reverse('teams:add_member', kwargs={'pk': team.pk}), {'user': user.pk})
    assert response.status_code == 302
    assert team.members.count() == 1
    assert user in team.members.all()


@pytest.mark.django_db
def test_remove_team_member(client, user, team):
    client.login(username='testuser', password='1testpasswordA')
    response = client.post(reverse('teams:remove_member', kwargs={'team_pk': team.pk, 'user_pk': user.pk}))
    assert response.status_code == 302
    assert team.members.count() == 0
    assert user not in team.members.all()


@pytest.mark.django_db
def test_remove_team_member_fail(client, user, team):
    client.login(username='testuser', password='1testpasswordA')
    user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='1testpasswordA')
    client.logout()
    client.login(username='testuser2', password='1testpasswordA')
    response = client.post(reverse('teams:remove_member', kwargs={'team_pk': team.pk, 'user_pk': user2.pk}))
    assert response.status_code == 403

    assert user2 not in team.members.all()
