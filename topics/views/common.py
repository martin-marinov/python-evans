from django.views.generic import View, RedirectView
from topics.views.reply import ReplyCreateView
from topics.views.topic import TopicDetailView
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import SingleObjectMixin
from topics.models import Topic


class TopicReplyDetail(View):
    def get(self, request, *args, **kwargs):
        view = TopicDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = login_required(ReplyCreateView.as_view())
        return view(request, *args, **kwargs)


class LastPostView(SingleObjectMixin, RedirectView):
    model = Topic

    def get_redirect_url(self, **kwargs):
        topic = self.get_object()
        url = topic.last_post().get_absolute_url()
        print(url)
        return url
