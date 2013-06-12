from django import forms
from topics.models import Topic, Reply


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        exclude = ('author',)


class ReplyForm(forms.ModelForm):
    body = forms.CharField(label='Отговор',
                           widget=forms.Textarea(),
                           error_messages={'required': 'Необходимо е да въведете текст.'})

    class Meta:
        model = Reply
        fields = ['body']
