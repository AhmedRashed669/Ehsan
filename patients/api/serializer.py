from rest_framework import serializers
from patients import models as patientmodel
from donors import models as donormodels
from django.db.models import Sum

class PatientCaseSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField()
    # patient_name = serializers.CharField(source = 'patient_name.first_name')
    reported_by = serializers.CharField(source = 'reported_by.hospital_name')
    age = serializers.IntegerField(source = 'patient_name.age')
    remainder_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = patientmodel.PatientCase
        fields = ["pk","patient_name","diagnose","cost","case_type","created_date","reported_by","age","remainder_cost"]

    def get_remainder_cost(self, obj):
        total_donation = donormodels.PatientCase_Donors.objects.filter(patient_case=obj).aggregate(total=Sum('amount'))['total']
        if total_donation is None:
            total_donation = 0
        return obj.cost - total_donation

        

