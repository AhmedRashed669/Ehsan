from rest_framework.viewsets import ModelViewSet
from .serializer import DonorSerializer
from donors.models import Donor
from django.contrib.auth.models import User

class DonorViewSet(ModelViewSet):
    serializer_class = DonorSerializer
    queryset = Donor.objects.all()
    
    def perform_create(self, serializer):
        email = self.request.data.get('email')
        user = User.objects.create_user(username=email)
        serializer.save(username = user)