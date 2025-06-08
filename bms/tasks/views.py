from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView
from django.views import View
from django.utils import timezone
from datetime import timedelta

from .forms import AddTaskForm, CommentForm, TaskRatingForm
from .models import Task, Comment, TaskRating


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

class AddComment(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
        return redirect('tasks:task_detail', pk=task.pk)

class UpdateTaskStatus(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if 'status' in request.POST:
            task.status = request.POST['status']
            task.save()
        return redirect('tasks:task_detail', pk=task.pk)


class RateTaskView(LoginRequiredMixin, UpdateView):
    model = TaskRating
    form_class = TaskRatingForm
    template_name = 'tasks/rate_task.html'

    def get_object(self):
        task_id = self.kwargs['pk']
        task = Task.objects.get(pk=task_id)

        # Получаем или создаём оценку
        rating, created = TaskRating.objects.get_or_create(
            task=task,
            defaults={
                'rated_by': self.request.user,
                'score': 3,  # Значение по умолчанию
            }
        )
        return rating

    def form_valid(self, form):
        # Проверяем, что пользователь — руководитель
        if self.request.user.role not in ['manager', 'admin']:
            form.add_error(None, "Только руководитель может оценивать задачи!")
            return self.form_invalid(form)

        # Проверяем, что задача завершена
        if self.object.task.status != 'completed':
            form.add_error(None, "Нельзя оценить невыполненную задачу!")
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.task.pk})


class UserRatingsView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/user_ratings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Параметры периода из GET-запроса
        period = self.request.GET.get('period', 'month')

        # Вычисляем даты периода
        if period == 'week':
            start_date = timezone.now() - timedelta(days=7)
        elif period == 'month':
            start_date = timezone.now() - timedelta(days=30)
        elif period == 'year':
            start_date = timezone.now() - timedelta(days=365)
        else:
            start_date = None

        # Получаем оценки
        context['ratings'] = user.get_user_ratings(start_date)
        context['average_rating'] = user.get_average_rating(start_date)
        context['period'] = period

        return context