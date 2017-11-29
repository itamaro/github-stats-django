from django import forms


class AddGitHubUserForm(forms.Form):
    username = forms.CharField(label='GitHub username', max_length=100)
