from topics.models import Post
from django.views.generic.base import RedirectView
from django.views.generic.detail import SingleObjectMixin


class PostView(SingleObjectMixin, RedirectView):
    model = Post

    def get_redirect_url(self, **kwargs):
            post = self.get_object()
            ## Follows a dirty hack, which tries to avoid the usage of third
            ## party libraries to access child models from the parent model.
            ## The same is done in the original(Ruby) evanse
            try:
                # The post is of type 'Topic', call it's url
                url = post.topic.get_absolute_url()
            except Post.DoesNotExist:
                # The post is of type 'Reply', call it's url
                url = post.reply.get_absolute_url()
            return url
