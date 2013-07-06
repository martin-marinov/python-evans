import os
import re
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from accounts.storage import OverwriteStorage


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, faculty_number, password=None):
        """
        Creates and saves a UserProfile with the given email,
        name, faculty_number and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=UserProfileManager.normalize_email(email),
                          name=name,
                          faculty_number=faculty_number
                          )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, faculty_number, password):
        """
        Creates and saves a superuser with the given email,
        name, faculty_number and password.
        """
        user = self.create_user(email=email,
                                name=name,
                                faculty_number=faculty_number,
                                password=password,
                                )
        user.is_superuser = True
        user.save(using=self._db)
        return user


def get_avatar_path(instance, filename):
    return os.path.join('photos', str(instance.id) + ".png")


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email',
                              max_length=255,
                              unique=True,
                              db_index=True)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True, editable=False)
    #Custom
    faculty_number = models.PositiveIntegerField(unique=True)
    points = models.PositiveSmallIntegerField(default=0)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, storage=OverwriteStorage())
    #Custom non-required
    github = models.CharField(max_length=255, blank=True, default='')
    twitter = models.CharField(max_length=255, blank=True, default='')
    skype = models.CharField(max_length=255, blank=True, default='')
    phone_number = models.CharField(max_length=255, blank=True, default='')
    site = models.CharField(max_length=255, blank=True, default='')
    about = models.TextField(blank=True, default='')
    subscribed = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['faculty_number', 'name']

    class Meta:
        app_label = 'accounts'
        ordering = ['registered_at']

    def __unicode__(self):
        return self.email

    def get_short_name(self):
        return self.shorten_name

    @property
    def shorten_name(self):
        match = re.search("(?P<first_name>\S+).* (?P<last_name>\S+)$", self.name)
        return ' '.join(match.group('first_name', 'last_name'))

    @property
    def first_name(self):
        try:
            return self.name.split(' ')[0]
        except IndexError:
            return None

    def get_absolute_url(self):
        return reverse('users.views.user-detail', kwargs={'pk': self.pk})

    @property
    def is_staff(self):
        # This field designates whether the user can log into the admin section.
        # Only superusers can :P
        return self.is_superuser
