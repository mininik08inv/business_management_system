from django import forms
from django.contrib.auth import get_user_model

from .models import Team

User = get_user_model()


class AddMemberForm(forms.Form):
    user_id = forms.IntegerField(
        label="Выберите пользователя",
        widget=forms.Select(choices=[])
    )

    def __init__(self, *args, **kwargs):
        available_users = kwargs.pop('available_users', None)
        super().__init__(*args, **kwargs)
        if available_users:
            self.fields['user_id'].widget.choices = [
                (user.id, user.username) for user in available_users
            ]

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'admin', 'invite_code']
