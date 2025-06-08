import pytest
from django.urls import reverse


def test_homepage(client):
    response = client.get(reverse('core:home'))
    assert response.status_code == 200
    assert 'index.html' in [template.name for template in response.templates]
    assert 'Business Manager' in str(response.content)


