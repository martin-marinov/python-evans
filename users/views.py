from django.views.generic import ListView, UpdateView, DetailView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from users.forms import EditProfileForm
from braces.views import LoginRequiredMixin
from django.contrib.auth import get_user_model


class UsersListView(ListView):
    model = get_user_model()
    paginate_by = 32
    template_name = 'users-list.html'
    context_object_name = 'users'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    context_object_name = 'user'
    success_url = reverse_lazy('dashboard')
    success_message = 'Профилът ви е обновен'
    template_name = 'edit_profile.html'
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        self.kwargs.update({'pk': self.request.user.pk})
        return super(EditProfileView, self).get_object(queryset)

    def get_form_kwargs(self):
        kwargs = super(EditProfileView, self).get_form_kwargs()
        kwargs.update({'initial': {'github': self.request.user.github,
                                   'twitter': self.request.user.twitter,
                                   'skype': self.request.user.skype,
                                   'phone_number': self.request.user.phone_number,
                                   'site:': self.request.user.site,
                                   'about': self.request.user.about,
                                   'subscribed': self.request.user.subscribed}})
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, self.success_message, fail_silently=True)
        return super(EditProfileView, self).form_valid(form)


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = 'user-detail.html'
    context_object_name = 'current_user'
