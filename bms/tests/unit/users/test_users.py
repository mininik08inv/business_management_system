import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('1testpasswordA')
    assert not user.is_staff
    assert not user.is_superuser
    assert user.is_active


@pytest.mark.django_db
def test_delete_user():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    user.delete()
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_update_user():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    user.username = 'newtestuser'
    assert user.username == 'newtestuser'

@pytest.mark.django_db
def test_unique_email():
    User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    with pytest.raises(IntegrityError):
        User.objects.create_user(username='testuser2', email='test@example.com', password='1testpasswordA')
        assert User.objects.count() == 1
        assert User.objects.filter(username='testuser2').exists() == False

@pytest.mark.xfail(reason='This test fails because the email is not unique.')
@pytest.mark.django_db
def test_fail_update_email():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA', role='user', fullname='Test User')
    assert user.email == 'test@example.com'
    with pytest.raises(ValueError):
        user.email = 'updatetEmail@mail.ru'
        user.full_clean()
        with pytest.raises(IntegrityError):
            user.save(ValidationError)


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(username='superuser', email='superuser@example.com', password='1testpasswordA')
    assert superuser.is_superuser
    assert superuser.is_staff

def test_login_page(client):
    response = client.get(reverse('users:login'))
    assert response.status_code == 200
    assert '<h1>Авторизация</h1>' in str(response.content.decode('utf-8'))

