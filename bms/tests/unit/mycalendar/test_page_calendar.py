import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()


@pytest.mark.django_db
def test_calendar_view(client, user, task, meeting):
    task.deadline = timezone.now()
    task.status = 'in_progress'
    task.save()

    meeting.start_time = timezone.now()
    meeting.end_time = timezone.now() + timezone.timedelta(hours=1)
    meeting.save()

    client.login(username='testuser', password='1testpasswordA')

    response = client.get(reverse('calendar'))

    assert response.status_code == 200
    assert 'mycalendar/calendar.html' in [template.name for template in response.templates]

    assert response.context['month_date'].replace(second=0, microsecond=0) == timezone.now().replace(second=0,
                                                                                                     microsecond=0)
    assert response.context['day_date'].replace(second=0, microsecond=0) == timezone.now().replace(second=0,
                                                                                                   microsecond=0)

    # Проверяем задачи и встречи
    assert list(response.context['day']['tasks']) == [task]
    assert list(response.context['day']['meetings']) == [meeting]