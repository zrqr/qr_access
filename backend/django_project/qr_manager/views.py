from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import QrCode
from .serializers import QrCodeSerializer


# Create your views here.
def home(request):
    return HttpResponse("Hello World !")

def get_qr_codes(request):
    qrcodes = QrCode.objects.all()
    serializer = QrCodeSerializer(qrcodes, many=True)
    return JsonResponse(serializer.data, safe=False)