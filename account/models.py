from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

from account.manager import UserManager

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superadmin = models.BooleanField(default=False)
    is_center_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.full_name



class Story(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stories/images/', null=True, blank=True)
    video = models.FileField(upload_to='stories/videos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(hours=24))


    def __str__(self):
        return self.title

    def is_expired(self):
        return timezone.now() > self.expires_at

    def view_count(self):
        return self.views.count()