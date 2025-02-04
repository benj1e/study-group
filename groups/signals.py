from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpRequest
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from django.contrib.auth import get_user_model
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

User = get_user_model()


def fetch_and_save_avatar(profile: Profile, avatar_url: str):
    """Fetch the avatar from the provided URL and save it to the profile."""
    try:
        response = requests.get(avatar_url)
        if response.ok:
            file_path = default_storage.save(
                f"{settings.MEDIA_ROOT}/avatars/{profile.user.username}.jpg",
                ContentFile(response.content),
            )
            profile.avatar = file_path
            profile.save()
    except requests.RequestException as e:
        # Log the exception or handle it as needed
        print(f"Failed to fetch avatar: {e}")


def create_avatar(profile: Profile, user):
    """Check and save the user's profile picture from social accounts."""
    # Skip if the profile already has an avatar
    if profile.avatar and default_storage.exists(profile.avatar.path):
        print(profile.user.username, "already has an avatar", "at", profile.avatar.path)
        return

    # Attempt to get the social account's profile picture
    social_account = SocialAccount.objects.filter(user=user).first()
    if social_account:
        avatar_url = social_account.extra_data.get("picture")
        if avatar_url:
            fetch_and_save_avatar(profile, avatar_url)


@receiver(user_signed_up)
def create_profile_for_social_user(sender, request: HttpRequest, user, **kwargs):
    """Signal to create a profile and fetch avatar for social users on signup."""
    profile, _ = Profile.objects.get_or_create(user=user)
    create_avatar(profile, user)


@receiver(post_save, sender=Profile)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Signal to create or update a user's profile and fetch avatar if necessary."""
    # Create a profile if it doesn't exist
    profile, _ = Profile.objects.get_or_create(id=instance.id)
    instance = instance.user

    # If the user has no avatar, attempt to fetch it
    if created or not profile.avatar or not default_storage.exists(profile.avatar.path):
        create_avatar(profile, instance)
