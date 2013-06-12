from django.test import TestCase
from topics.tests.factories import Topic, Reply


class TopicsModelsTests(TestCase):
    def test_reply_should_be_editable_by_owner_and_admin_only(self):
        reply = Reply()
        