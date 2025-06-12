from django import forms
from django.contrib.auth import get_user_model

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
        if self.request:
            self.fields['organizer'].initial = self.request.user
            self.fields['participants'].queryset = self.fields['participants'].queryset.exclude(pk=self.request.user.pk)