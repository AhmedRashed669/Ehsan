from django.http import JsonResponse
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from fcm_django.models import FCMDevice

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

@receiver(user_logged_out)
def delete_token(sender, user, request, **kwargs):
    try:
        FCMDevice.objects.get(user = user).delete()
    except:
        print("No Token Found")








# @csrf_exempt
# def test(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         value = data.get('shit',None)
#         if value is not None:
#             return JsonResponse({'shit': value})

#     return JsonResponse({'eror':'sth wrong'},status = 400)


