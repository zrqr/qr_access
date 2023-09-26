from rest_framework import serializers
from .models import QrCode, CustomVariable

class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ["id", "name", "date_created", "date_finish", "token", "senha"]

class CustomVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomVariable
        fields = ["name", "value"]