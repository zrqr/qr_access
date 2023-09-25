from rest_framework import serializers
from .models import QrCode

class QrCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ["id", "name", "date_created", "date_finish", "token"]