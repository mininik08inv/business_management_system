from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView

from tasks.forms import AddTaskForm
from tasks.models import Task


# Create your views here.

class ShowTask(DetailView):
    template_name = 'tasks/task_detail.html'
    slug_url_kwarg = 'pk'
    context_object_name = 'task'


class ShowAllTasks(ListView):
    template_name = 'tasks/tasks_all.html'
    context_object_name = 'tasks'
    title_page = 'список задач'

    def get_queryset(self):
        tasks_lst = Task.objects.all()
        return tasks_lst


class AddTask(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddTaskForm
    template_name = 'tasks/addtask.html'
    title_page = 'Добавление задачи'
    permission_required = 'tasks.add_task'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.created_by = self.request.user
        return super().form_valid(form)
