from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['points'] = self.request.user.points
        return context
