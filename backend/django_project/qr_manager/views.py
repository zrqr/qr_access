from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import QrCode, CustomVariable
from .serializers import QrCodeSerializer, CustomVariableSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime
import secrets
import qrcode

import requests
ARDUINO_API = "http://192.168.0.18/open_the_gate/"

# Create your views here.
def home(request):
    return HttpResponse("Hello World !")

@api_view(["GET",  "POST"])
def qr_codes(request):

    if request.method == "GET":
        qrcodes = QrCode.objects.all()
        serializer = QrCodeSerializer(qrcodes, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        new_code = {}

        new_code["date_created"] = datetime.datetime.today().date()
        new_code["name"] = request.data["name"]
        new_code["date_finish"] = request.data["date_finish"]
        new_code["token"] = secrets.token_urlsafe(16)
        new_code["senha"] = f"{str(secrets.randbelow(999999)).zfill(6)}"

        serializer = QrCodeSerializer(data = new_code)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    
@api_view(["GET"])
def get_image(request, id):

    try:
        qrcode_instance = QrCode.objects.get(pk=id)
    except QrCode.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "GET":
        serializer = QrCodeSerializer(qrcode_instance)
        token = serializer.data["token"]

        img = qrcode.make(token)

        response = HttpResponse(content_type='image/png')

        img.save(response, 'png')
        return response

def check_qrcode(token:str):

    try:
        token_filter = QrCode.objects.filter(token=token)
        if token_filter.count() == 0:
            return status.HTTP_401_UNAUTHORIZED
        else:
            qrcode_instance = QrCode.objects.filter(id__in=token_filter.values('id'))[0]
    
            serializer = QrCodeSerializer(qrcode_instance)

            date_finish = datetime.date.fromisoformat(serializer.data["date_finish"])

            if date_finish >= datetime.date.today():
                call_open()
                return status.HTTP_200_OK
            else:
                return status.HTTP_410_GONE
        
    except:
        return status.HTTP_400_BAD_REQUEST


def check_pass(password:str):

    try:
        token_filter = QrCode.objects.filter(senha=password)
        if token_filter.count() == 0:
            return status.HTTP_401_UNAUTHORIZED
        else:
            qrcode_instance = QrCode.objects.filter(id__in=token_filter.values('id'))[0]

            serializer = QrCodeSerializer(qrcode_instance)

            date_finish = datetime.date.fromisoformat(serializer.data["date_finish"])

            if date_finish >= datetime.date.today():
                call_open()
                return status.HTTP_200_OK
            else:
                return status.HTTP_410_GONE

    except:
        return status.HTTP_400_BAD_REQUEST

@api_view(["GET"])  
def check_password(request, password:str):

    return Response(status=check_pass(password))


@api_view(["GET"])  
def check_qr(request, token:str):

    return Response(status=check_qrcode(token))

def get_var(variable):
    var_obj = CustomVariable.objects.get(name=variable)
    serializer = CustomVariableSerializer(var_obj)
    return serializer.data


def call_open():

    todo = {"open": True, "apiKey": "pacatatucotianao"}
    response = requests.post(ARDUINO_API, json=todo)
    print(response.status_code)

@api_view(["GET", "PUT"])
def var(request, variable):

    if request.method == "GET":
        try:
            value = get_var(variable)
            return JsonResponse(value, safe=False)
        except CustomVariable.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        try:
            var_obj = CustomVariable.objects.get(name=variable)
            serializer = CustomVariableSerializer(var_obj, data = {"name": variable, "value": request.data["value"]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            
        except CustomVariable.DoesNotExist:    
            serializer = CustomVariableSerializer(data = {"name": variable, "value": request.data["value"]})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)