#-*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.http import is_safe_url
from django.views.generic import RedirectView
from django.views.generic.edit import FormView
from django.conf import settings
from django.shortcuts import redirect

from accounts.forms import LoginForm, RegistrationForm
from accounts.models import UserProfile

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView


class LoginView(FormView):
    template_name = 'sign_in.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    success_message = "Влязохте успешно. Дерзайте."

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        can log them in.
        """
        if self.check_and_delete_test_cookie():
            auth.login(self.request, form.get_user())
            messages.success(self.request, self.success_message, fail_silently=True)
            remember_me = form.cleaned_data['remember_me']
            if remember_me:
                self.request.session.set_expiry(0)
            return super(LoginView, self).form_valid(form)
        else:
            return redirect('home-page')

    def form_invalid(self, form):
        """
        The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        set the test cookie again and re-render the form with errors.
        """
        self.set_test_cookie()
        return super(LoginView, self).form_invalid(form)

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
        """
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(RedirectView):
    permanent = False
    redirect_field_name = auth.REDIRECT_FIELD_NAME
    redirect_url_overrides_redirect_field = False
    success_message = "Излязохте успешно от системата. Ще ни липсвате :'("
    redirect_url = 'home-page'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            auth.logout(request)
            messages.success(request, self.success_message, fail_silently=True)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        """
        Order of priority:
        * self.success URL (if success_url_overrides_redirect_field is an override)
        * a "next" paramater specified in the logout URL
        * the login URL
        """
        if self.redirect_url_overrides_redirect_field:
            return super(LogoutView, self).get_redirect_url(**kwargs)

        redirect_to = reverse(self.redirect_url)

        if self.redirect_field_name in self.request.REQUEST:
            redirect_to = self.request.REQUEST[self.redirect_field_name]
            # Security check -- don't allow redirection to a different host.
            if not is_safe_url(url=redirect_to, host=self.request.get_host()):
                redirect_to = self.request.path

        return redirect_to


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm
    template_name = 'registration_form.html'
    success_url = 'dashboard'

    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        name, faculty_number = cleaned_data['name'], cleaned_data['faculty_number']

        UserProfile.objects.create_user(email, name, faculty_number, password)

        new_user = auth.authenticate(email=email, password=password)
        auth.login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

