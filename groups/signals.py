from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import HttpRequest
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from .models import Profile
from django.contrib.auth import get_user_model

user = get_user_model()


def get_or_create_profile_pic(profile: Profile, user):
    first_name, last_name = user.first_name, user.last_name
    print(user)

    # Attempt to get the social account's profile picture
    profile_pic = None
    try:
        social_account = SocialAccount.objects.filter(user=user).first()
        if social_account:
            profile_pic = social_account.extra_data.get("picture")

        if not profile_pic:  # If no social picture, construct based on names
            if first_name and last_name:
                profile_pic = f"https://avatar.iran.liara.run/username?username={first_name+last_name}"
            else:
                profile_pic = "https://avatar.iran.liara.run/public"

        # Save the profile picture to the profile
        profile.profile_picture = profile_pic
        profile.save()

        print("Profile picture saved successfully")
    except SocialAccount.DoesNotExist:
        # Handle case where no social account exists (fallback logic)
        profile.profile_picture = "https://avatar.iran.liara.run/public"
        profile.save()


@receiver(user_signed_up)
def create_profile_for_social_user(sender, request: HttpRequest, user: User, **kwargs):
    """Signal for saving user's profile pictures"""
    profile, created = Profile.objects.get_or_create(user=user)
    get_or_create_profile_pic(profile, user)


@receiver(signal=post_save, sender=user)
def create_profile_before_save(sender, instance, created, **kwargs):
    """Signal for saving user's profile pictures"""

    if created:
        Profile.objects.create(user=instance)

    if Profile.objects.filter(user=instance).exists():
        profile = Profile.objects.get(user=instance)
        get_or_create_profile_pic(profile, instance)
    else:
        Profile.objects.create(user=instance)
        profile = Profile.objects.get(user=instance)
        get_or_create_profile_pic(profile, instance)
