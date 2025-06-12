from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView
from django.utils import timezone
from datetime import timedelta

from tasks.forms import AddTaskForm, CommentForm, TaskRatingForm
from tasks.models import Task, Comment, TaskRating


class ShowTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        context['comment_form'] = CommentForm()
        context['rating'] = task.get_rating()
        context['can_rate_task'] = (
                task.status == 'completed' and
                self.request.user.role in ['manager', 'admin']
        )

        return context


class ShowAllTasks(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_all.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class AddTask(LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'tasks/addtask.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('tasks:task_detail', kwargs={'pk': self.object.pk})


class AddComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.task = task
        comment.author = self.request.user
        comment.save()
        return redirect('tasks:task_detail', pk=task.pk)


class UpdateTaskStatus(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['status']

    def form_valid(self, form):
        form.save()
        return redirect('tasks:task_detail', pk=self.object.pk)


class RateTaskView(LoginRequiredMixin, UpdateView):
    model = TaskRating
    form_class = TaskRatingForm
    template_name = 'tasks/rate_task.html'

    DEFAULT_RATING_SCORE = 3

    def get_object(self):
        task_id = self.kwargs['pk']
        task = Task.objects.get(pk=task_id)

        # Получаем или создаём оценку
        rating, created = TaskRating.objects.get_or_create(
            task=task,
            defaults={
                'rated_by': self.request.user,
                'score': self.DEFAULT_RATING_SCORE,
            }
        )
        return rating

    def form_valid(self, form):
        # Проверяем, что пользователь — руководитель
        if self.request.user.role not in ['manager', 'admin']:
            raise ValidationError("Только руководитель может оценивать задачи!")

        # Проверяем, что задача завершена
        if self.object.task.status != 'completed':
            raise ValidationError("Нельзя оценить невыполненную задачу!")

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.task.pk})


class UserRatingsView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/user_ratings.html'

    @staticmethod
    def get_start_date(period):
        period_map = {
            'week': 7,
            'month': 30,
            'year': 365
        }
        if period in period_map:
            return timezone.now() - timedelta(days=period_map[period])
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Параметры периода из GET-запроса
        period = self.request.GET.get('period', 'month')

        start_date = self.get_start_date(period)

        # Получаем оценки
        context['ratings'] = user.get_user_ratings(start_date)
        context['average_rating'] = user.get_average_rating(start_date)
        context['period'] = period

        return context
