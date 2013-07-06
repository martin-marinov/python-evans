from datetime import timedelta

import factory
from tasks import models
from django.utils.timezone import now


class Task(factory.DjangoModelFactory):
    FACTORY_FOR = models.Task

    name = 'Task'
    description = 'Simple description'
    closes_at = now()


class ClosedTask(Task):
    closes_at = now() - timedelta(days=1)


class OpenedTask(Task):
    closes_at = now() + timedelta(days=1)
