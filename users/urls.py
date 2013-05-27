from django.conf.urls import patterns, url
from users.views import EditProfileView, UsersListView, UserDetailView

urlpatterns = patterns('',
                       url(r'^profile/edit$', EditProfileView.as_view(),
                           name='users.views.profile-edit'),
                       url(r'^users$', UsersListView.as_view(),
                           name='users.views.list-users'),
                       url(r'^users/(?P<pk>\d+)', UserDetailView.as_view(),
                           name='users.views.user-detail'),
                       )
