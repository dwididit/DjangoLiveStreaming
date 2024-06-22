# DjangoLiveStreaming/models.py
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_streamer = models.BooleanField(default=False)


class Stream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    streamer = models.ForeignKey(User, related_name='streams', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    stream = models.ForeignKey(Stream, related_name='donations', on_delete=models.CASCADE)
    donor = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='pending')
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
