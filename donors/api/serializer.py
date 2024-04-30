from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from donors.models import Donor,PatientCase_Donors,GeneralDonations
from django.contrib.auth.models import User
from patients.models import PatientCase

# class WatchLaterSerializer(ModelSerializer):
#     watch_later = serializers.StringRelatedField(many = True)
#     class Meta:
#         model = Donor
#         fields = ['watch_later']


class SimpleCaseSerializer(ModelSerializer):
    class Meta:
        model = PatientCase
        fields = ['diagnose']

class SpecficDonorCaseDonationsSerializer(ModelSerializer):
    patient_case = SimpleCaseSerializer(read_only=True)
    class Meta:
        model = PatientCase_Donors
        fields = ['patient_case','amount','donation_date']


class SpecficDonorGeneralDonationsSerializer(ModelSerializer):
    # pp = serializers.CharField(read_only = True ,default = None)
    class Meta:
        model = GeneralDonations
        fields = ['amount','donation_date']

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




