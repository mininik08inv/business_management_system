from django import forms
from django.contrib.auth import get_user_model

from .models import Task


class AddTaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False  # Add this if the field is optional
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'team', 'priority', 'deadline']
