from rest_framework import routers
from patients.api.views import PatientCaseViewSet
from donors.api.views import DonorViewSet,DonationsViewSet
from fcm_django.api.rest_framework import FCMDeviceCreateOnlyViewSet

router = routers.DefaultRouter()
router.register('patientcases', PatientCaseViewSet, basename="patientcase")
router.register('donors', DonorViewSet, basename="donor")
router.register('donations', DonationsViewSet, basename="donation")
router.register('devices', FCMDeviceCreateOnlyViewSet)