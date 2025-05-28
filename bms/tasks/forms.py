from django import forms
from .models import Task, Comment, TaskRating


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'responsible_team', 'priority', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }


class TaskRatingForm(forms.ModelForm):
    class Meta:
        model = TaskRating
        fields = ['score', 'feedback']
        widgets = {
            'score': forms.Select(choices=TaskRating.RATING_CHOICES),
            'feedback': forms.Textarea(attrs={'rows': 3}),
        }
