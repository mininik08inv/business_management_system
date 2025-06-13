from django.conf import settings
from django.contrib.auth import get_user_model

from django.db import models
from django.core.exceptions import ValidationError

User = get_user_model()

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_meetings'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='meetings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)

    def clean(self):
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
