from django.conf.urls import patterns, url
from tasks.views import TasksListView, TaskDetailView, MySolutionView, SolutionsListView, SolutionDetailView

urlpatterns = patterns('',
                       url(r'^$', TasksListView.as_view(), name='tasks.views.tasks-list'),
                       url(r'(?P<task_fk>\d+)/solutions/(?P<pk>\d+)$',
                           SolutionDetailView.as_view(), name='tasks.views.solution-detail'),
                       url(r'(?P<pk>\d+)$', TaskDetailView.as_view(), name='tasks.views.task-detail'),
                       url(r'(?P<task_fk>\d+)/my_solution$', MySolutionView.as_view(), name='tasks.views.my-solution'),
                       url(r'(?P<pk>\d+)/solutions$', SolutionsListView.as_view(), name='tasks.views.solutions-list'),
                       )
