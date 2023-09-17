from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("qrcodes/", views.qr_codes),
    path("qrcodes/<int:id>", views.qr_code_item)
]