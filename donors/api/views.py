from rest_framework.viewsets import ModelViewSet
from .serializer import DonorSerializer,DonationSerializer
from donors.models import Donor,PatientCase_Donors
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import action

class DonorViewSet(ModelViewSet):
    serializer_class = DonorSerializer
    queryset = Donor.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def perform_create(self, serializer):
        email = self.request.data.get('email')
        user = User.objects.create_user(username=email,password=email)
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

    