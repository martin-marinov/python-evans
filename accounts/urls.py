from django.conf.urls import patterns, url
from accounts.views import LoginView, LogoutView, RegistrationView

urlpatterns = patterns('',
                       url(r'^users/sign_in$', LoginView.as_view(),
                           name='accounts.views.login'),
                       url(r'^users/sign_out$', LogoutView.as_view(),
                           name='accounts.views.logout'),
                       url(r'^registration/new$', RegistrationView.as_view(),
                           name='accounts.views.registration'),
                       )
