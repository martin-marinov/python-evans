from django.views.generic import CreateView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from topics.forms import ReplyForm
from topics.models import Reply, Topic
from django.shortcuts import get_object_or_404


class ReplyCreateView(CreateView):
    form_class = ReplyForm
    model = Reply

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = get_object_or_404(Topic, pk=self.kwargs['pk'])
        return super(ReplyCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ReplyRedirectView(SingleObjectMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        reply = self.get_object()
        return reply.get_absolute_url()


# class TopicView(RedirectView):
#     def get(self, request, *args, **kwargs):
#         view = TopicView.as_view()
#         return view(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         view = ReplyCreateView.as_view()
#         return view(request, *args, **kwargs)


