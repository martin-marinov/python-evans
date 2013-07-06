from django.views.generic import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib import messages
from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['points'] = self.request.user.points
        return context


class PermissionDeniedView(RedirectView):
    error_message = 'Нямате достъп до тази страница.'

    def get_redirect_url(self):
        messages.error(self.request, self.error_message, fail_silently=True)
        return reverse('home-page')

custom_permission_denied_view = PermissionDeniedView.as_view()
