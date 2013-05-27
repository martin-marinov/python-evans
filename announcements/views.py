from announcements.models import Announcement
from django.views.generic import ListView


class AnnouncementsList(ListView):

    model = Announcement
    context_object_name = 'announcements'
    template_name = "announcements.html"
