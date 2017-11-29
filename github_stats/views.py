import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from .forms import AddGitHubUserForm
from .models import GitHubUser, GitHubCommit


def index(request):
    """Render the main Github stats view"""
    if request.method == 'POST':
        form = AddGitHubUserForm(request.POST)
        if form.is_valid():
            # TODO(itamar): makes this async to avoid request timeout
            user = GitHubUser.make_user(form.cleaned_data['username'])
    else:
        form = AddGitHubUserForm()

    all_users = GitHubUser.objects.all()
    return render(
        request, 'github/index.html',
        {'form': form, 'github_users': all_users})


@csrf_protect
def load_commits(request):
    """AJAX endpoint for loading a user commit stats frmo Github API

    Returns a JSON {"status": "<message>"} object.
    """
    # TODO(itamar): makes this async to avoid request timeout
    if request.is_ajax():
        if request.method == 'POST':
            req = json.loads(request.body)
            username = req['username']
            try:
                user = GitHubUser.objects.get(username=username)
            except:
                return JsonResponse({'status': 'bad user'}), 404
            GitHubCommit.load_commits(user)
            return JsonResponse({'status': 'OK'})
    return JsonResponse({'status': 'error'}), 403
