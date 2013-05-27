from topics.models import Topic
from topics.forms import TopicForm
from django.views.generic import ListView, DetailView, CreateView


class TopicsListView(ListView):
    model = Topic
    paginate_by = 30
    template_name = 'topics.html'
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    model = Topic
    template_name = 'show_topic.html'
    context_object_name = 'topic'


class TopicCreateView(CreateView):
    model = Topic
    form_class = TopicForm
    template_name = 'topic_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(TopicCreateView, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
