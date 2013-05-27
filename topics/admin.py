from django.contrib import admin

from topics.models import Topic
from topics.forms import TopicForm


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

admin.site.register(Topic, TopicAdmin)
