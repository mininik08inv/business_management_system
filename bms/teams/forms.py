from django import forms
from django.contrib.auth import get_user_model

from teams.models import Team

User = get_user_model()

class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),  # Только активные пользователи
        label="Пользователь",
        empty_label="Выберите пользователя"
    )

    def __init__(self, *args, **kwargs):
        self.exclude_users = kwargs.pop('exclude_users', [])
        super().__init__(*args, **kwargs)
        if self.exclude_users:
            self.fields['user'].queryset = User.objects.exclude(id__in=[u.id for u in self.exclude_users])


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']