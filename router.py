from rest_framework import routers
from patients.api.views import PatientCaseViewSet
from donors.api.views import DonorViewSet


router = routers.DefaultRouter()
router.register('patientcases', PatientCaseViewSet, basename="patientcase")
router.register('donors', DonorViewSet, basename="donor")