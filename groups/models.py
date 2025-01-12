from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    """Profile model for users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.URLField(name="Profile pics", null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
