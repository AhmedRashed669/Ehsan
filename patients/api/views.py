from rest_framework.generics import (ListAPIView,)
from . import serializer
from patients.models import PatientCase,Patient


class PatientCaseList(ListAPIView):
    serializer_class = serializer.PatientCaseSerializer

    def get_queryset(self):
        patientlist = PatientCase.objects.filter(is_accepted = True)
        return patientlist
    
