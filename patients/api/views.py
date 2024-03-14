from rest_framework.generics import (ListAPIView,)
from . import serializer
from patients.models import PatientCase,Patient
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


# class PatientCaseList(ListAPIView):
#     serializer_class = serializer.PatientCaseSerializer

#     def get_queryset(self):
#         patientlist = PatientCase.objects.filter(is_accepted = True)
#         return patientlist
    
class PatientCaseViewSet(ModelViewSet):
    serializer_class = serializer.PatientCaseSerializer
    queryset = PatientCase.objects.filter(is_accepted = True)
    http_method_names = ["get",]
    # pagination_class = "PageNumberPagination"
    

    
