from django.urls import path
from .views import *

app_name = 'patients'

urlpatterns = [
    path('',PatientList.as_view(),name="patient-list"),
    path('createpatient/',CreatePatient.as_view(),name="add-patient"),
    path('updatepatient/<int:pk>/',UpdatePatient.as_view(),name="update-patient"),
    path('deletepatient/<int:pk>/',DeletePatient.as_view(),name="delete-patient"),
    path('patientdetail/<int:pk>',PatientDetail.as_view(),name="patient-detail"),
    path('createpatientcase/<pk>',PatientCaseCreate.as_view(),name="create-case"),
    path('casedetail/<int:pk>',PatientCaseDetail.as_view(),name = "case-detail"),
    path('updatepatientcase/<int:pk>/',UpdatePatientCase.as_view(),name="case-update"),
    path('deletepatientcase/<int:pk>/',DeletePatientCase.as_view(),name="delete-case"),
    path("approvecase/<pk>",approve_case,name="approve-case"),
    path("succeedcase/<pk>",succeed_case,name="succeed-case"),
    path("acceptcase/<pk>",accept_case,name="accept-case"),
]   