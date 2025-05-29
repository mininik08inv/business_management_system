from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.utils import timezone
from datetime import timedelta, date
from calendar import monthcalendar, monthrange
from tasks.models import Task
from meetings.models import Meeting


class CalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'mycalendar/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now()

        # Устанавливаем даты для отображения
        context['month_date'] = today
        context['day_date'] = today

        # Получаем задачи и встречи для текущего месяца
        month_tasks = Task.objects.filter(
            Q(created_by=user) | Q(assigned_to=user),
            deadline__month=today.month,
            deadline__year=today.year
        )

        month_meetings = Meeting.objects.filter(
            Q(organizer=user) | Q(participants=user),
            start_time__month=today.month,
            start_time__year=today.year,
            is_cancelled=False
        )

        # Создаем календарь на месяц
        cal = monthcalendar(today.year, today.month)
        month_calendar = []

        for week in cal:
            week_days = []
            for day in week:
                if day == 0:
                    week_days.append({'day': ''})
                else:
                    day_date = date(today.year, today.month, day)
                    day_events = []

                    # Добавляем задачи
                    for task in month_tasks.filter(deadline__day=day):
                        day_events.append(f"Задача: {task.title}")

                    # Добавляем встречи
                    for meeting in month_meetings.filter(start_time__day=day):
                        day_events.append(f"Встреча: {meeting.title}")

                    week_days.append({
                        'day': day,
                        'events': day_events,
                        'is_today': day == today.day
                    })
            month_calendar.append(week_days)

        context['month_calendar'] = month_calendar

        # Данные для дневного вида
        context['day'] = {
            'tasks': Task.objects.filter(
                Q(created_by=user) | Q(assigned_to=user),
                deadline__date=today.date()
            ),
            'meetings': Meeting.objects.filter(
                Q(organizer=user) | Q(participants=user),
                start_time__date=today.date(),
                is_cancelled=False
            )
        }

        return context