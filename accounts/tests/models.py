from django.test import TestCase
from accounts.tests.factories import User, AdminUser
from django.db import IntegrityError
from accounts.models import UserProfile


class AccountsModelTests(TestCase):
    """
    Test the model and manager.
    """

    def test_shorten_name_1(self):
        user = User.build(name='Петър Иванов')
        self.assertEqual(user.shorten_name, 'Петър Иванов')

    def test_shorten_name_2(self):
        user = User.build(name='Петър Петров Иванов')
        self.assertEqual(user.shorten_name, 'Петър Иванов')

    def test_shorten_name_3(self):
        user = User.build(name='Петър Петров Петров Иванов')
        self.assertEqual(user.shorten_name, 'Петър Иванов')

    def test_first_name_1(self):
        user = User.build(name='Петър')
        self.assertEqual(user.first_name, 'Петър')

    def test_first_name_2(self):
        user = User.build(name='Петър Петров')
        self.assertEqual(user.first_name, 'Петър')

    def test_first_name_3(self):
        user = User.build(name='Петър Петров Иванов')
        self.assertEqual(user.first_name, 'Петър')

    def test_admin_has_0_points(self):
        admin = AdminUser.create()
        self.assertEqual(admin.points, 0)

    def test_email_is_unique(self):
        User.create(email="pesho@abv.bg")
        with self.assertRaises(IntegrityError):
            User.create(email="pesho@abv.bg")

    def test_faculty_number_is_unique(self):
        User.create(faculty_number=1)
        with self.assertRaises(IntegrityError):
            User.create(faculty_number=1)

    def test_older_users_first(self):
        first = User()
        second = User()
        third = User()
        self.assertEqual(list(UserProfile.objects.all()), [first, second, third])
        self.assertNotEqual(list(UserProfile.objects.all()), [second, first, third])
