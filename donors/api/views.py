from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializer import DonorSerializer,DonationSerializer,GeneralDonationserializer,SpecficDonorGeneralDonationsSerializer,SpecficDonorCaseDonationsSerializer
from donors.models import Donor,PatientCase_Donors,GeneralDonations
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication,BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from django.core.mail import send_mail
from fcm_django.api.rest_framework import FCMDeviceViewSet
from fcm_django.models import FCMDevice

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
        
        

    
class DonationsViewSet(ModelViewSet):
    serializer_class = DonationSerializer
    queryset =  PatientCase_Donors.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ["post",]


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





    