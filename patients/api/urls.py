from django.urls import path
from patients.api.views import PatientCaseList

app_name = 'patients api'
urlpatterns = [
    path('',PatientCaseList.as_view(),name="patient-list"),
]