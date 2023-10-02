from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("qrcodes/", views.qr_codes),
    path("qrcodes/<int:id>", views.qr_code_item),
    path("image/<int:id>", views.get_image),
    path("check_qr/<str:token>", views.check_qr), 
    path("check_password/<str:password>", views.check_password), 
    path("var/<str:variable>", views.var) 
]