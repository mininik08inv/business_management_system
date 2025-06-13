from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from meetings.models import Meeting


User = get_user_model()

class MeetingForm(forms.ModelForm):
    organizer = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.HiddenInput(),
        required=True
    )

    class Meta:
        model = Meeting
        fields = ['organizer', 'title', 'description', 'start_time', 'end_time', 'participants']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if not self.request or not self.request.user.is_authenticated:
            raise ValidationError("Требуется авторизация")

        if self.request:
            self.fields['organizer'].initial = self.request.user
            if 'participants' in self.fields:
                self.fields['participants'].queryset = User.objects.exclude(pk=self.request.user.pk)