from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()

# meetings/models.py
from django.db import models
from django.core.exceptions import ValidationError


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='organized_meetings'
    )
    participants = models.ManyToManyField(
        'users.User',
        related_name='meetings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def clean(self):
        if not hasattr(self, 'organizer'):
            raise ValidationError("Организатор встречи должен быть указан")

        if self.end_time <= self.start_time:
            raise ValidationError("Время окончания должно быть позже времени начала")

        # Проверка наложения встреч
        conflicts = Meeting.objects.filter(
            models.Q(organizer=self.organizer) | models.Q(participants=self.organizer),
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
            is_cancelled=False
        ).exclude(pk=self.pk if self.pk else None)

        if conflicts.exists():
            raise ValidationError("У вас уже есть встреча в это время")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)