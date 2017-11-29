from django.conf.urls import url

from .views import index, load_commits

urlpatterns = [
    url(R'^$', index, name='github'),
    url(R'^load_commits$', load_commits, name='load-commits'),
]
