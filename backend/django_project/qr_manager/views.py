from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import QrCode
from .serializers import QrCodeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def home(request):
    return HttpResponse("Hello World !")

@api_view(["GET", "POST"])
def qr_codes(request):
    if request.method == "GET":
        qrcodes = QrCode.objects.all()
        serializer = QrCodeSerializer(qrcodes, many=True)
        return JsonResponse(serializer.data, safe=False)
    
    if request.method == "POST":
        serializer = QrCodeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(["GET", "PUT", "DELETE"])
def qr_code_item(request, id):

    try:
        qrcode = QrCode.objects.get(pk=id)
    except QrCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "GET":
        serializer = QrCodeSerializer(qrcode)
        return Response(serializer.data)
    if request.method == "PUT":
        serializer = QrCodeSerializer(qrcode, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        qrcode.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)