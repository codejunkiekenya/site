# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from django.contrib.auth import views as auth_views
from filebrowser.sites import site



admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
]

urlpatterns += i18n_patterns(

   url(r'comments/', include('django_comments_xtd.urls')),
    #url(r'^comments/', include('django_comments.urls')),
    url(r'helpdesk/', include('helpdesk.urls')),
    url(r'contact/', include('contact_form.urls')),
	url(r'^survey/', include('survey.urls')),
	url(r'^polls/', include('polls.urls')),
	url(r'^reviews/', include('reviews.urls', namespace="reviews")),
    url(r'^parks/', include('parks.urls', namespace="parks")),
    url(r'^counties/', include('counties.urls', namespace="counties")),
    url(r'^companies/', include('companies.urls', namespace="companies")),
    url(r'^colleges/', include('colleges.urls', namespace="colleges")),
    url(r'^constituencies/', include('constituencies.urls', namespace="constituencies")),
    url(r'^wards/', include('wards.urls', namespace="wards")),
    url(r'^hospitals/', include('hospitals.urls', namespace="hospitals")),
    url(r'^hotels/', include('hotels.urls', namespace="hotels")),
    url(r'^schools/', include('schools.urls', namespace="schools")),
    url(r'^sports/', include('sports.urls', namespace="sports")),
    url(r'^associations/', include('associations.urls', namespace="associations")),
	url(r"^notifications/", include("pinax.notifications.urls")),
	url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
	url('^accounts/', include('django.contrib.auth.urls', namespace='accounts')),
	url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^ads/', include('ads.urls')),
    url(r'^admin/timeline/', include('admin_timeline.urls')),
    url(r'^admintools/', include('admin_tools.urls')),
    url(r'^admin/', include(admin.site.urls)), # NOQA
    url(r'^', include('cms.urls')),
)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns