from django.utils.timezone import now

from django.db import models
from django.conf import settings

from markupfield.fields import MarkupField


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = MarkupField(markup_type='markdown')
    max_points = models.PositiveSmallIntegerField(default=6)
    closes_at = models.DateTimeField()

    class Meta:
        ordering = ['closes_at']

    @property
    def is_closed(self):
        return self.closes_at < now()


class Solution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             editable=False,
                             related_name='solutions')
    task = models.ForeignKey(Task,
                             editable=False,
                             related_name='solutions')
    code = models.TextField()
    points = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)
    updated_at = models.DateTimeField(auto_now=True,
                                      editable=False)

    class Meta:
        ordering = ['created_at']
        unique_together = (("user", "task"),)


class Revision(models.Model):
    solution = models.ForeignKey(Solution,
                                 editable=False,
                                 related_name='revisions')
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False)

    class Meta:
        ordering = ['created_at']
        get_latest_by = 'created_at'
