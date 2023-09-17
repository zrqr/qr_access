from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("qrcodes/", views.get_qr_codes)
]