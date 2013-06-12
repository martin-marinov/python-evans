from django.conf.urls import patterns, url
from topics.views.topic import TopicsListView, TopicCreateView
from topics.views.common import TopicReplyDetail, LastPostView
from topics.views.reply import ReplyEditView

urlpatterns = patterns('',
                       url(r'^$', TopicsListView.as_view(), name='topics.views.topics-list'),
                       url(r'new', TopicCreateView.as_view(), name='topics.views.topic-create'),
                       url(r'(?P<pk>\d+)/last_reply', LastPostView.as_view(), name='topics.views.common.last-post'),
                       url(r'(?P<pk>\d+)$', TopicReplyDetail.as_view(), name='topics.views.common.topic-reply-detail'),
                       url(r'(?P<topic_fk>\d+)/replies/(?P<pk>\d+)/edit$', ReplyEditView.as_view(), name='topics.views.reply.reply-edit'),
                       )
