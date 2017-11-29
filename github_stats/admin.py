from django.contrib import admin

from .models import GitHubUser, GitHubCommit

admin.site.register(GitHubUser)
admin.site.register(GitHubCommit)
