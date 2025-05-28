from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView
from django.views import View

from .forms import AddTaskForm, CommentForm
from .models import Task, Comment

class ShowTask(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
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