from topics.models import Topic
from topics.forms import TopicForm, ReplyForm
from topics import TOPICS_PER_PAGE, REPLIES_PER_PAGE
from django.views.generic import ListView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Max


class TopicsListView(ListView):
    model = Topic
    paginate_by = TOPICS_PER_PAGE
    template_name = 'topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        queryset = super(TopicsListView, self).get_queryset()
        queryset = queryset.annotate(Max('replies__created_at')).order_by('-replies__created_at__max')
        return queryset


class TopicDetailView(SingleObjectMixin, ListView):
    template_name = 'show_topic.html'
    paginate_by = REPLIES_PER_PAGE

    def get_context_data(self, **kwargs):
        kwargs['topic'] = self.object
        kwargs['form'] = ReplyForm()
        return super(TopicDetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        self.object = self.get_object(Topic.objects.all())
        return self.object.replies.all()


class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topic_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TopicCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
