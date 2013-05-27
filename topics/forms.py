from django.forms import ModelForm
from topics.models import Topic, Reply


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        exclude = ('author',)


class ReplyForm(ModelForm):
    class Meta:
        model = Reply
        exclude = ('author', 'topic')
