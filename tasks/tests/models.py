from datetime import timedelta

from django.utils.timezone import now
from django.test import TestCase

from tasks.tests.factories import Task
from tasks.models import Task as TaskModel


class TaskModelTests(TestCase):
    def test_can_tell_task_is_closed(self):
        task = Task.build(closes_at=(now()-timedelta(days=1)))
        self.assertTrue(task.is_closed)
        task = Task.build(closes_at=(now()+timedelta(days=1)))
        self.assertFalse(task.is_closed)

    def test_amounts_to_six_points_by_default(self):
        task = Task()
        self.assertEqual(task.max_points, 6)

    def test_tasks_are_sorted_chronologically(self):
        second = Task(closes_at=now()-timedelta(days=1))
        first = Task(closes_at=now()-timedelta(days=2))
        self.assertEqual(list(TaskModel.objects.all()), [first, second])
