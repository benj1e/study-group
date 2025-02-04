from django.urls import path
from django.views.generic import TemplateView
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
