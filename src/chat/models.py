from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Message(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.message


class Room(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.CharField(max_length=255, unique=True)
    created_by = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    messages = models.ManyToManyField(Message, blank=True)

    class Meta:
        ordering = ('created_at',)

    def get_absolute_url(self):
        return reverse('chat_uuid', kwargs={'uuid': self.uuid})

    def __str__(self):
        return self.name


