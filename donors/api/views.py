from rest_framework.viewsets import ModelViewSet
from .serializer import DonorSerializer,DonationSerializer,GeneralDonationserializer
from donors.models import Donor,PatientCase_Donors,GeneralDonations
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action
from django.core.mail import send_mail

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

    
class DonationsViewSet(ModelViewSet):
    serializer_class = DonationSerializer
    queryset =  PatientCase_Donors.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ["get","post",]


class GeneralDonationViewSet(ModelViewSet):
    serializer_class = GeneralDonationserializer
    queryset = GeneralDonations.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    http_method_names = ['get','post']


    