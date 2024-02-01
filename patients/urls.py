from django.urls import path
from .views import *

app_name = 'patients'

urlpatterns = [
    path('',PatientList.as_view(),name="patient-list"),
    path('createpatient/',CreatePatient.as_view(),name="add-patient"),
    path('updatepatient/<int:pk>/',UpdatePatient.as_view(),name="update-patient"),
    path('deletepatient/<int:pk>/',DeletePatient.as_view(),name="delete-patient"),
    path('patientdetail/<int:pk>',PatientDetail.as_view(),name="patient-detail"),
    path('createpatientcase/<pk>',PatientCaseCreate,name="create-case")


]