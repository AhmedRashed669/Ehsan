from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.contrib.auth import login,authenticate
from .models import HospitalEmployee
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        # Check if the user is a HospitalEmployee or SystemEmployee
        if hasattr(user, 'hospitalemployee') or hasattr(user, 'systememployee') or user.is_superuser:
            print("Received data: ", form.cleaned_data)  # Print received data
            response_data = {'message': True}
            print("Response data: ", response_data)  # Print response data
            login(self.request,user)
            return JsonResponse(response_data)    
        else:
            response_data = {'message': False}
            print("Response data: ", response_data)  # Print response data
            return JsonResponse(response_data)

# @csrf_exempt
# def test(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         value = data.get('shit',None)
#         if value is not None:
#             return JsonResponse({'shit': value})

#     return JsonResponse({'eror':'sth wrong'},status = 400)


