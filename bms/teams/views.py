from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView, ListView

from teams.forms import AddTeamForm, AddMemberForm
from teams.models import Team

User = get_user_model()


class ShowTeam(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.object
        context['members'] = team.members.all()
        context['is_admin'] = self.request.user == team.admin or self.request.user.role == 'admin'

        if context['is_admin']:
            available_users = User.objects.exclude(
                id__in=team.members.all().values_list('id', flat=True)
            )
            context['add_member_form'] = AddMemberForm(available_users=available_users)

        return context

    def post(self, request, *args, **kwargs):
        team = self.get_object()
        if not (request.user == team.admin or request.user.role == 'admin'):
            return HttpResponseForbidden()

        if 'add_member' in request.POST:
            available_users = User.objects.exclude(
                id__in=team.members.all().values_list('id', flat=True)
            )
            form = AddMemberForm(request.POST, available_users=available_users)
            if form.is_valid():
                user_id = form.cleaned_data['user_id']
                user = get_object_or_404(User, id=user_id)
                team.members.add(user)
        elif 'remove_member' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            team.members.remove(user)

        return redirect(reverse('teams:team_detail', kwargs={'pk': team.pk}))


class ShowAllTeams(ListView):
    template_name = 'teams/teams_all.html'
    context_object_name = 'teams'

    def get_queryset(self):
        teams_lst = Team.objects.all()
        return teams_lst

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'список команд'
        return context


class AddTeam(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = AddTeamForm
    template_name = 'teams/addteam.html'
    permission_required = 'teams.add_team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление Команды'
        return context


