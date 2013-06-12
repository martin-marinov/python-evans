from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse

from topics import REPLIES_PER_PAGE


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    starred = models.BooleanField(default=False)


class Topic(Post):
    title = models.CharField(max_length=255)

    def last_post(self):
        if self.replies.count() > 0:
            return self.replies.latest()
        else:
            return self

    def get_absolute_url(self):
        return reverse('topics.views.common.topic-reply-detail', args=[str(self.pk)])


class Reply(Post):
    topic = models.ForeignKey(Topic, related_name='replies')

    class Meta:
        verbose_name_plural = 'replies'
        get_latest_by = "created_at"
        ordering = ['created_at']

    def get_absolute_url(self):
        topic_url = reverse('topics.views.common.topic-reply-detail',
                            kwargs={'pk': self.topic.pk})
        return '{}?page={}#reply_{}'.format(topic_url, self.get_page(), self.pk)

    def get_page(self):
        replies_before_this = self.topic.replies.filter(id__lt=self.id).count()
        return replies_before_this // REPLIES_PER_PAGE + 1

admin.site.register(Reply)
