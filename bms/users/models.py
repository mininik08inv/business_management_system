from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg
from django.urls import reverse
from django.apps import apps



class User(AbstractUser):
    """Кастомная модель пользователя с расширенными полями"""

    ROLE_CHOICES = [
        ('user', 'Обычный пользователь'),
        ('manager', 'Менеджер'),
        ('admin', 'Администратор команды'),
    ]

    email = models.EmailField('Email адрес', unique=True)
    fullname = models.CharField(max_length=100, verbose_name='ФИО')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль")
    team = models.ForeignKey(
        to='teams.Team',
        verbose_name='Команда',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.fullname

    @property
    def is_team_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    def delete(self, *args, **kwargs):
        """Удаление аккаунта без возможности восстановления"""
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:profile', kwargs={'pk': self.pk})

    def get_user_ratings(self, start_date=None, end_date=None):
        """
        Возвращает все оценки задач пользователя за период
        """
        TaskRating = apps.get_model('tasks', 'TaskRating')
        ratings = TaskRating.objects.filter(task__assigned_to=self)

        if start_date:
            ratings = ratings.filter(rated_at__gte=start_date)
        if end_date:
            ratings = ratings.filter(rated_at__lte=end_date)

        return ratings.select_related('task', 'rated_by')

    def get_average_rating(self, start_date=None, end_date=None):
        """
        Возвращает среднюю оценку за период
        """
        ratings = self.get_user_ratings(start_date, end_date)
        avg = ratings.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else None