from django.db import models
from django.utils import timezone
from github import Github


class GitHubUser(models.Model):
    username = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    avatar_url = models.URLField()
    profile_url = models.URLField()
    date_created = models.DateTimeField()
    last_events_update = models.DateTimeField()

    def __str__(self):
        return 'GitHubUser: %s' % (self.username)

    def get_user_stats(self):
        """Return a stats dictionary for this user"""
        commits = GitHubCommit.objects.filter(user__username=self.username)
        stats = {
            'today': 0,
            'week': 0,
            'month': 0,
        }
        now = timezone.now()
        for commit in commits:
            if now - timezone.timedelta(days=1) <= commit.commit_date <= now:
                stats['today'] += 1
            if now - timezone.timedelta(weeks=1) <= commit.commit_date <= now:
                stats['week'] += 1
            if now - timezone.timedelta(days=30) <= commit.commit_date <= now:
                stats['month'] += 1
        return stats

    @classmethod
    def make_user(cls, username):
        """Create new GitHubUser object for username from Github API"""
        # TODO(itamar): Handle errors, rate-limiting in API
        github = Github()
        gh_user = github.get_user(username)
        user = cls(
            username=gh_user.login,
            fullname=gh_user.name or gh_user.login,
            avatar_url=gh_user.avatar_url,
            profile_url=gh_user.html_url,
            date_created=timezone.make_aware(gh_user.created_at,
                                             timezone.utc),
            last_events_update=timezone.datetime(1970, 1, 1,
                                                 tzinfo=timezone.utc))
        user.save()
        # Load commits from Github before returning
        GitHubCommit.load_commits(user)
        return user


class GitHubCommit(models.Model):
    user = models.ForeignKey('GitHubUser', on_delete=models.CASCADE)
    commit_sha = models.CharField(max_length=64)
    commit_url = models.URLField()
    commit_date = models.DateTimeField()
    commit_message = models.TextField()

    def __str__(self):
        return 'GitHubCommit: %s' % (self.commit_sha)

    @classmethod
    def load_commits(cls, user):
        """Load commits for user using Github Events API"""
        # TODO(itamar): Handle errors, rate-limiting in API
        github = Github()
        gh_user = github.get_user(user.username)
        # TODO(itamar): figure out how to request only newer events to reduce
        # the load on this API
        events = gh_user.get_events()
        for event in events:
            if event.type != 'PushEvent':
                continue
            commits = event.payload['commits']
            for commit in commits:
                # FIXME(itamar): need better author matching logic
                if commit['author']['name'] != user.fullname:
                    continue
                existing = (
                    cls.objects.filter(commit_sha=commit['sha']).count() > 0)
                if existing:
                    continue
                commit_obj = cls(
                    user=user,
                    commit_sha=commit['sha'],
                    commit_url=commit['url'],
                    # FIXME(itamar): get actual commit time, not push time
                    commit_date=timezone.make_aware(event.created_at,
                                                    timezone.utc),
                    commit_message=commit['message']
                )
                commit_obj.save()
        # update owning user object that we updated events now
        user.last_events_update = timezone.now()
        user.save()
