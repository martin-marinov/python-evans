from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import View, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from topics.forms import ReplyForm
from topics.models import Reply, Topic

from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from guardian.shortcuts import assign_perm


class ReplyCreateView(LoginRequiredMixin, SingleObjectMixin, FormMixin, View):
    form_class = ReplyForm
    model = Topic

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = self.get_object()
        self.object = form.save()
        assign_perm('topics.change_reply', self.request.user, self.object)
        return super(ReplyCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReplyEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "topics.change_reply"
    model = Reply
    form_class = ReplyForm
    template_name = "reply_edit.html"
    error_message = 'Нямате достъп до тази страница.'
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super(ReplyEditView, self).get_form_kwargs()
        kwargs.update({'initial': {'body': self.object.body}})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        try:
            super(ReplyEditView, self).dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, self.error_message, fail_silently=True)
            return redirect('home-page')
