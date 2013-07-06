from django.db import models

from markupfield.fields import MarkupField


class Announcement(models.Model):

    title = models.CharField(max_length=255)
    body = MarkupField(markup_type='markdown')
    created_at = models.DateTimeField(auto_now_add=True,
                                      editable=False,
                                      verbose_name='Date created')

    class Meta:
        ordering = ["-created_at"]
