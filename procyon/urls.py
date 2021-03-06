from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r'^stars/', include('procyon.starcatalog.urls')),
    url(r'^stories/', include('procyon.stories.urls')),
    url(r'^maker/', include('procyon.starsystemmaker.urls')),
    url(r"^account/", include("account.urls")),
    url(r'^generators/', include('procyon.generators.urls'), name="generators"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
