from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializer import DonorSerializer,DonationSerializer,GeneralDonationserializer,SpecficDonorGeneralDonationsSerializer,SpecficDonorCaseDonationsSerializer,SimpleCaseSerializer
from donors.models import Donor,PatientCase_Donors,GeneralDonations
from patients.models import PatientCase
from patients.api.serializer import PatientCaseSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from django.core.mail import send_mail
from fcm_django.api.rest_framework import FCMDeviceViewSet
from fcm_django.models import FCMDevice
from rest_framework import status
from django.db.models import Sum

class DonorViewSet(ModelViewSet):
    serializer_class = DonorSerializer
    queryset = Donor.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get','post','patch']
    
    #performs actions before saving to the db
    def perform_create(self, serializer):
        email = self.request.data.get('email')
        password =  self.request.data.get('password')
        user = User.objects.create_user(username=email,password=password)
        send_mail(
            "Donor creation",
            "Thank you for creating an account",
            "settings.EMAIL_HOST_USER",
            [email],
            fail_silently=False,
        )
        serializer.save(username = user)


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny,]
        return super().get_permissions()
    
    @action(detail=True,methods=['get'])
    def get_general_donations(self,request,pk = None):
        donations = GeneralDonations.objects.filter(donor = pk)
        serializer =  SpecficDonorGeneralDonationsSerializer(donations,many = True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['get'])
    def get_case_donations(self,request,pk = None):
        donations = PatientCase_Donors.objects.filter(donor = pk)
        serializer =  SpecficDonorCaseDonationsSerializer(donations,many = True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['get'])
    def watch_later_cases(self,request,pk=None):
        cases = PatientCase.objects.filter(watched_by = pk)
        serializer = PatientCaseSerializer(cases,many = True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def add_watch_later(self,request,pk = None):
        data = request.data
        case_id = data['watch_later']
        if case_id:
            donor = self.get_object()
            donor.watch_later.add(case_id)
            return Response(status=status.HTTP_202_ACCEPTED)

    
    @action(detail=True,methods=['post'])
    def remove_watch_later_cases(self,request,pk = None):
        data = request.data
        case_id = data['watch_later']
        if case_id:
            donor = self.get_object()
            donor.watch_later.remove(case_id)
            return Response(status=status.HTTP_202_ACCEPTED)

    
class DonationsViewSet(ModelViewSet):
    serializer_class = DonationSerializer
    queryset =  PatientCase_Donors.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ["post",]

    def create(self, request, *args, **kwargs):
        amount_donated = request.data.get('amount')
        case_id = request.data.get('patient_case')
        total_donation = PatientCase_Donors.objects.filter(patient_case=case_id).aggregate(total=Sum('amount'))['total'] or 0
        case = PatientCase.objects.get(id = case_id)
        remaining_cost = int(case.cost) - total_donation
        if amount_donated > remaining_cost:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().create(request, *args, **kwargs)


class GeneralDonationViewSet(ModelViewSet): 
    serializer_class = GeneralDonationserializer
    queryset = GeneralDonations.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['post']

class CustomFCMDeviceViewSet(FCMDeviceViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,SessionAuthentication,BasicAuthentication)
    http_method_names = ['post','delete']

    def create(self, request, *args, **kwargs):
        # Access the user from the request
        user = request.user

        # Create a new FCMDevice instance
        fcm_device = FCMDevice(user=user, **request.data)
        fcm_device.save()

        # You can add additional logic here if needed

        # Return a response
        return Response({
            'message': 'FCM Device created successfully for user: {}'.format(user.username)
        })





    