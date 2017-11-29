from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

import github_stats.urls


admin.autodiscover()


urlpatterns = [
    url(R'^favicon.ico$',
        RedirectView.as_view(url=settings.STATIC_URL + '/favicon.ico')),
    url(R'^admin/', include(admin.site.urls)),
    url(R'', include(github_stats.urls)),
]
