import factory
from accounts import models


class User(factory.DjangoModelFactory):
    FACTORY_FOR = models.UserProfile

    email = factory.Sequence(lambda n: 'person-%d@example.org' % n)
    faculty_number = factory.Sequence(lambda n: '%05d' % n)
    name = 'John D. Doe'


class AdminUser(User):
    is_superuser = True
