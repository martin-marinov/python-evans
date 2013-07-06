from .views import DashboardView

from announcements.views import AnnouncementsList
from django.conf import settings
from django.conf.urls import patterns, include, url

from topics.views.post import PostView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'python_evans_project.views.home', name='home'),
                       # url(r'^python_evans_project/', include('python_evans_project.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('accounts.urls')),
                       url(r'', include('users.urls')),
                       url(r'^announcements/', AnnouncementsList.as_view(), name='announcements'),
                       url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
                       url(r'^topics/', include('topics.urls')),
                       url(r'^tasks/', include('tasks.urls')),
                       url(r'^post/(?P<pk>\d+)', PostView.as_view(), name='topics.views.post-view'),
                       url(r'^$', AnnouncementsList.as_view(template_name='index.html'), name='home-page'),
                       )

handler403 = 'python_evans_project.views.custom_permission_denied_view'

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)
