from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    role = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
