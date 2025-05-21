from rest_framework import serializers
from .models import CustomerData  # Ensure this import path is correct for your app


class CustomerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerData
        fields = '__all__'
