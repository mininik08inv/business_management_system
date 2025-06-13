from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнено'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='assigned_tasks')
    responsible_team = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def has_rating(self):
        """Есть ли у задачи оценка?"""
        return hasattr(self, 'rating')

    def get_rating(self):
        """Получить оценку задачи"""
        return getattr(self, 'rating', None)

    def set_rating(self, user, score, feedback=''):
        """
        Поставить оценку задаче.
        """
        if self.status != 'completed':
            raise ValidationError("Нельзя оценить невыполненную задачу!")

        rating, created = TaskRating.objects.update_or_create(
            task=self,
            defaults={
                'rated_by': user,
                'score': score,
                'feedback': feedback
            }
        )
        return rating, created

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title

    def is_overdue(self):
        return timezone.now() > self.deadline

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tasks:task_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к задаче {self.task.id}'


class TaskRating(models.Model):
    RATING_CHOICES = [
        (1, '1 - Плохо'),
        (2, '2 - Ниже среднего'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]

    task = models.OneToOneField(
        'Task',
        on_delete=models.CASCADE,
        related_name='rating',
        verbose_name="Задача"
    )
    rated_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name="Кто оценил"
    )
    score = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        verbose_name="Оценка"
    )
    feedback = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )
    rated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оценки"
    )

    class Meta:
        verbose_name = "Оценка задачи"
        verbose_name_plural = "Оценки задач"
        ordering = ['-rated_at']

    def __str__(self):
        return f"Оценка {self.score} для задачи #{self.task.id}"

    def clean(self):
        # Проверяем, что оценивает руководитель (manager или admin)
        if self.rated_by.role not in ['manager', 'admin']:
            raise ValidationError("Только руководитель может оценивать задачи!")

        # Проверяем, что задача завершена
        if self.task.status != 'completed':
            raise ValidationError("Можно оценивать только выполненные задачи!")