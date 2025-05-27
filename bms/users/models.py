from django.contrib.auth.models import AbstractUser
from django.db import models

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
