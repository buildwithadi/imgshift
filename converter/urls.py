from django.urls import path
from .views import home, convert_image  # ✅ Fix Import Issue

urlpatterns = [
    path("", home, name="home"),
    path("convert/", convert_image, name="convert_image"),
]
