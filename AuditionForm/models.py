from django.db import models
from django.utils.timezone import now
from datetime import timedelta


class AuditionData(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    roll = models.CharField(max_length=10, null=True, unique=True)

    # ✅ FIXED — was IntegerField with max_length (WRONG)
    phone = models.CharField(max_length=10, null=True)

    department = models.CharField(max_length=30, null=True)
    gender = models.CharField(max_length=30, null=True)
    year = models.CharField(max_length=30, null=True)

    domain = models.JSONField(default=list, null=True, blank=True)
    questions_answers = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name


class OTP(models.Model):
    otp = models.CharField(max_length=6)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return self.email
