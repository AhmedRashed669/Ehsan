from django.urls import path
from .views import *

app_name = 'patients'

urlpatterns = [
    path('',PatientList.as_view(),name="patient_list")
]