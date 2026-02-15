from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

if (
    settings.DJANGO_SUPERUSER_USERNAME
    and settings.DJANGO_SUPERUSER_EMAIL
    and settings.DJANGO_SUPERUSER_PASSWORD
):
    if not User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists():
        User.objects.create_superuser(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            email=settings.DJANGO_SUPERUSER_EMAIL,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
        )
