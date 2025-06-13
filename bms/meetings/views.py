

from django.db.models import Q
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from meetings.models import Meeting
from meetings.forms import MeetingForm


class MeetingListView(LoginRequiredMixin, ListView):
    model = Meeting
    template_name = 'meetings/meeting_list.html'

    def get_queryset(self):
        return Meeting.objects.filter(
            Q(organizer=self.request.user) |
            Q(participants=self.request.user),
            Q(end_time__gte=timezone.now()),
            is_cancelled=False
        ).order_by('start_time').distinct()

class MeetingDetailView(LoginRequiredMixin, DetailView):
    model = Meeting
    template_name = 'meetings/meeting_detail.html'
    context_object_name = 'meeting'

    def get_queryset(self):
        return Meeting.objects.filter(organizer=self.request.user)


class MeetingCreateView(LoginRequiredMixin, CreateView):
    form_class = MeetingForm
    template_name = 'meetings/meeting_form.html'
    success_url = reverse_lazy('meetings:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        if kwargs.get('data'):
            # Добавляем организатора в данные формы до валидации
            data = kwargs['data'].copy()
            data['organizer'] = self.request.user.pk
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        # На всякий случай дублируем установку организатора
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class MeetingUpdateView(LoginRequiredMixin, UpdateView):
    model = Meeting
    form_class = MeetingForm
    template_name = 'meetings/meeting_form.html'
    success_url = reverse_lazy('meetings:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        if kwargs.get('data'):
            # Добавляем организатора в данные формы до валидации
            data = kwargs['data'].copy()
            data['organizer'] = self.request.user.pk
            kwargs['data'] = data
        return kwargs

    def form_valid(self, form):
        # На всякий случай дублируем установку организатора
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class MeetingCancelView(LoginRequiredMixin, DeleteView):
    model = Meeting
    fields = []
    template_name = 'meetings/meeting_confirm_cancel.html'
    success_url = reverse_lazy('meetings:list')
