from rest_framework import serializers
from patients import models

class PatientCaseSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField()
    # patient_name = serializers.CharField(source = 'patient_name.first_name')
    reported_by = serializers.CharField(source = 'reported_by.hospital_name')
    
    class Meta:
        model = models.PatientCase
        fields = ["pk","patient_name","diagnose","cost","case_type","created_date","reported_by",]

    
