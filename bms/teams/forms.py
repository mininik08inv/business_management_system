from django import forms
from django.contrib.auth import get_user_model

from teams.models import Team

User = get_user_model()

class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Пользователь",
        empty_label="Выберите пользователя"
    )

    def __init__(self, *args, **kwargs):
        exclude_users = kwargs.pop('exclude_users', None)
        super().__init__(*args, **kwargs)

        queryset = User.objects.filter(is_active=True)

        if exclude_users:
            exclude_ids = [u.id if hasattr(u, 'id') else u for u in exclude_users]
            queryset = queryset.exclude(id__in=exclude_ids)

        self.fields['user'].queryset = queryset


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']