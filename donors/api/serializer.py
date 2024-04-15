from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from donors.models import Donor,PatientCase_Donors,GeneralDonations
from django.contrib.auth.models import User


class DonationSerializer(ModelSerializer):
    date = serializers.DateTimeField(required = False)
    class Meta:
        model = PatientCase_Donors
        fields = "__all__"

class GeneralDonationserializer(ModelSerializer):
    class Meta:
        model = GeneralDonations
        fields = '__all__'

class DonorSerializer(ModelSerializer):
    username = serializers.CharField(required = False)
    # watch_later = serializers.StringRelatedField(many = True,read_only = True)
    # cases = serializers.StringRelatedField(many=True)
    cases = DonationSerializer(source ='patientcase_donors_set', many = True, read_only=True)
    general_donation = GeneralDonationserializer(source ='generaldonations_set', many = True, read_only=True)
    class Meta:
        model = Donor
        fields = "__all__"

    # def create(self, validated_data):
    #     return super().create(validated_data)




