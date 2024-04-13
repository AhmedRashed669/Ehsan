from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from donors.models import Donor

# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"
    
class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "home.html"
    
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        try:
            donor = Donor.objects.get(username = user)
            return Response({
                'token': token.key,
                'donor_id': donor.pk,
                'full_name':donor.full_name,
                'email':donor.email,
                'phone_number':donor.phone_number
            })
        except:
                return Response({
                'token': token.key,
                'user_id': user.pk,
            })
