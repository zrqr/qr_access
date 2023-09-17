from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("qrcodes/", views.qr_codes),
    path("qrcodes/<int:id>", views.qr_code_item),
    path("new_code/", views.create_qrcode),
    path("qrcode_image/<int:id>", views.get_image)
]