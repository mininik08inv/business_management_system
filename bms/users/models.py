from django.contrib.auth.models import AbstractUser
from django.db import models
from teams.models import Team


class User(AbstractUser):
    """Кастомная модель пользователя с расширенными полями"""

    class Role(models.TextChoices):
        USER = 'user', 'Обычный пользователь'
        MANAGER = 'manager', 'Менеджер'
        ADMIN = 'admin', 'Администратор команды'

    email = models.EmailField('Email адрес', unique=True)
    role = models.CharField(
        'Роль',
        max_length=25,
        choices=Role.choices,
        default=Role.USER
    )
    team = models.ForeignKey(
        Team,
        verbose_name='Команда',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField('Активен', default=True)

    # Переопределяем поле username, чтобы использовать email как основное для входа
    # username = None
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def is_team_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    def delete(self, *args, **kwargs):
        """Удаление аккаунта без возможности восстановления"""
        super().delete(*args, **kwargs)
