from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView
from django.views import View

from tasks.models import Task
from .forms import AddTeamForm, AddMemberForm
from .models import Team

User = get_user_model()

class ShowTeam(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(created_by__in=self.object.members.all())
        return context

class ShowAllTeams(LoginRequiredMixin, ListView):
    model = Team
    template_name = 'teams/teams_all.html'
    context_object_name = 'teams'

class AddTeam(LoginRequiredMixin, CreateView):
    form_class = AddTeamForm
    template_name = 'teams/addteam.html'

    def form_valid(self, form):
        team = form.save(commit=False)
        team.admin = self.request.user
        team.save()
        return redirect('teams:team_detail', pk=team.pk)


class AddTeamMember(LoginRequiredMixin, View):
    def get(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        form = AddMemberForm(exclude_users=team.members.all())
        return render(request, 'teams/add_member.html', {
            'form': form,
            'team': team
        })

    def post(self, request, pk):
        team = get_object_or_404(Team, pk=pk)
        form = AddMemberForm(request.POST, exclude_users=team.members.all())

        if form.is_valid():
            user = form.cleaned_data['user']
            team.members.add(user)
            return redirect('teams:team_detail', pk=team.pk)

        return render(request, 'teams/add_member.html', {
            'form': form,
            'team': team
        })


class RemoveTeamMember(LoginRequiredMixin, View):
    def post(self, request, team_pk, user_pk):
        team = get_object_or_404(Team, pk=team_pk)
        user = get_object_or_404(User, pk=user_pk)

        # Проверяем, что текущий пользователь - админ команды
        if request.user != team.admin:
            return HttpResponseForbidden()

        team.members.remove(user)
        return redirect('teams:team_detail', pk=team.pk)