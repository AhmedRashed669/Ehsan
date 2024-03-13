from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from donors.models import Donor,PatientCase_Donors
from django.contrib.auth.models import User


class DonationSerializer(ModelSerializer):
    class Meta:
        model = PatientCase_Donors
        fields = "__all__"

class DonorSerializer(ModelSerializer):
    username = serializers.CharField(required = False)
    # cases = serializers.StringRelatedField(many=True)
    cases = DonationSerializer(source ='patientcase_donors_set', many = True, read_only=True)
    class Meta:
        model = Donor
        fields = "__all__"

    # def create(self, validated_data):
    #     return super().create(validated_data)


