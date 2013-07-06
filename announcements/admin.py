from django.contrib import admin
from announcements.models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'created_at')

admin.site.register(Announcement, AnnouncementAdmin)
