from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from donors.models import Donor
from django.contrib.auth.models import User

class DonorSerializer(ModelSerializer):
    username = serializers.CharField(required = False)
    class Meta:
        model = Donor
        fields = ["username","email","phone_number"]

    # def create(self, validated_data):
    #     return super().create(validated_data)