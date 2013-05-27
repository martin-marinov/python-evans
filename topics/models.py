from django.db import models
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)


class Topic(Post):
    title = models.CharField(max_length=255)

    def last_post(self):
        print(self.replies.count())
        if self.replies.count() > 0:
            return self.replies.latest()
        else:
            return self

    def get_absolute_url(self):
        return reverse('topics.views.common.topic-reply-detail', args=[str(self.pk)])

    class Meta:
        ordering = ['-updated_at']


class Reply(Post):
    topic = models.ForeignKey(Topic, related_name='replies')

    class Meta:
        verbose_name_plural = 'replies'
        get_latest_by = "updated_at"

    def get_absolute_url(self):
        return '{0}#reply_{1}'.format(reverse('topics.views.common.topic-reply-detail',
                                              kwargs={'pk': self.topic.pk}),
                                      self.pk)

admin.site.register(Reply)
