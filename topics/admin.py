from django.contrib import admin


from topics.models import Topic, Reply
from topics.forms import TopicForm, ReplyForm


class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    list_display = ('title', 'starred')
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'starred')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Topic, TopicAdmin)


class ReplyAdmin(admin.ModelAdmin):
    form = ReplyForm

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(Reply, ReplyAdmin)
