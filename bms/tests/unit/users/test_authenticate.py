import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import MultipleObjectsReturned
from unittest.mock import patch, Mock

from users.authentication import EmailAuthBackend

User = get_user_model()


@pytest.mark.django_db
def test_authenticate_success():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    backend = EmailAuthBackend()
    assert backend.authenticate(None, username='test@example.com', password='1testpasswordA') == user


@pytest.mark.django_db
def test_authenticate_fail():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    backend = EmailAuthBackend()
    assert backend.authenticate(None, username='test@example.com', password='wrongpassword') is None


@pytest.mark.django_db
def test_get_user_success():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    backend = EmailAuthBackend()
    assert backend.get_user(user.id) == user


@pytest.mark.django_db
def test_get_user_fail():
    user = User.objects.create_user(username='testuser', email='test@example.com', password='1testpasswordA')
    backend = EmailAuthBackend()
    assert backend.get_user(user.id + 1) is None
