from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, UpdateView

from tasks.models import Task, Revision, Solution
from tasks.forms import MySolutionForm

from braces.views import LoginRequiredMixin


class TasksListView(ListView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = "task_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            try:
                user_solution = Solution.objects.get(user=self.request.user, task=self.object)
                context['user_solution'] = user_solution
            except Solution.DoesNotExist:
                pass
        return context


class MySolutionView(LoginRequiredMixin, UpdateView):
    model = Solution
    form_class = MySolutionForm
    template_name = 'my_solution.html'
    success_message = 'Задачата е предадена успешно!'
    error_message = 'Вашето решение не бе прието.'

    def get_form_kwargs(self):
        kwargs = super(MySolutionView, self).get_form_kwargs()
        solution = self.get_object()
        if solution:
            kwargs.update({'initial': {'code': solution.code}})
        return kwargs

    def get_object(self, queryset=None):
        # Try to get solution if any. Else, a new one will be created
        self.task = Task.objects.get(pk=self.kwargs['task_fk'])
        try:
            solution = Solution.objects.get(user=self.request.user, task=self.task)
        except Solution.DoesNotExist:
            solution = None
        return solution

    def form_valid(self, form):
        # A new revision should be created
        form.instance.user = self.request.user
        form.instance.task = self.task
        solution = form.save()
        revision = Revision(solution=solution, code=solution.code)
        revision.save()
        return super(MySolutionView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.error_message, fail_silently=True)
        return super(MySolutionView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(MySolutionView, self).get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message, fail_silently=True)
        return reverse('tasks.views.task-detail', args=(self.object.task.pk,))


class SolutionsListView(DetailView):
    model = Task
    template_name = 'solutions_list.html'

    def get(self, request, *args, **kwargs):
        self.object = task = self.get_object()
        if not task.is_closed and not request.user.is_staff:
            raise PermissionDenied()
        return super(SolutionsListView, self).get(request, *args, **kwargs)


class SolutionDetailView(DetailView):
    model = Solution
    template_name = 'solution_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = solution = self.get_object()
        if not solution.task.is_closed and not request.user.is_staff:
            raise PermissionDenied()
        return super(SolutionDetailView, self).get(request, *args, **kwargs)
