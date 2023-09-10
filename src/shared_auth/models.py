from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True, verbose_name='')

    def __str__(self):
        return self.user.username
