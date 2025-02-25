from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import UserManager


# Create your models here.


class User(AbstractUser):
    user_img = models.ImageField(upload_to='user_image', null=True, blank=True, default='user_image/default.jpg')
    username = None
    email = models.EmailField(
        "Email Address",
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    is_verified = models.BooleanField(default=False)

    def get_absolute_url(self):
        return self.user_img.url


    def __str__(self):
        return self.email