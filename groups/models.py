from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    """Profile model for users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} Profile"
