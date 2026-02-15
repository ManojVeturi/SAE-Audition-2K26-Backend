from django.db import models
import json
# from django.utils import timezone
# from datetime import timedelta
from django.utils.timezone import now, timedelta


class AuditionData(models.Model):
    domains_choices = [
        ('Event Management', 'Event Management'),
        ("Automobiles", "Automobiles"),
        ("Robotics", "Robotics"),
        ("Web Development", "Web Development"),
        ("Graphics Designing", "Graphics Designing"),
    ]
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    roll = models.CharField(max_length=10, null=True, unique=True)
    phone = models.IntegerField(max_length=10, null=True)
    department = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True)
    year = models.CharField(max_length=30, null=True)
    domain = models.JSONField(default=list, null=True, blank=True)  # Store serialized JSON
    questions_answers = models.JSONField(default=dict, blank=True, null=True)
    # questions_answers2 = models.JSONField(default=dict, blank=True, null=True)
    # desc = models.CharField(max_length=200, null=True, unique=False)


    def __str__(self):
        return self.name


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        """Check if OTP is expired (valid for 5 minutes)"""
        return now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return self.email
