import factory
from topics import models
from accounts.tests.factories import User


class Topic(factory.DjangoModelFactory):
    FACTORY_FOR = models.Topic

    title = factory.Sequence(lambda n: "Topic %d" % n)
    body = factory.LazyAttribute(lambda topic: "Body of '%s'" % topic.title)
    author = factory.SubFactory(User)


class Reply(factory.DjangoModelFactory):
    FACTORY_FOR = models.Reply

    author = factory.SubFactory(User)
    body = factory.Sequence(lambda n: "Reply No: %d" % n)
    topic = factory.SubFactory(Topic)
