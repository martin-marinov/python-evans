from django.core.exceptions import PermissionDenied
from django.views.generic import View, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin

from topics.forms import ReplyForm
from topics.models import Reply, Topic

from braces.views import LoginRequiredMixin
from python_evans_project.mixins import OwnerOrSuperUserRequiredMixin


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
        return super(ReplyCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReplyEditView(OwnerOrSuperUserRequiredMixin, LoginRequiredMixin, UpdateView):
    owner_path = 'author'
    model = Reply
    form_class = ReplyForm
    template_name = "reply_edit.html"

    def get_form_kwargs(self):
        kwargs = super(ReplyEditView, self).get_form_kwargs()
        kwargs.update({'initial': {'body': self.object.body.raw}})
        return kwargs

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.author != request.user and not request.user.is_staff:
    #         raise PermissionDenied()
    #     return super(ReplyEditView, self).dispatch(request, *args, **kwargs)
