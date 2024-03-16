from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .models import HospitalEmployee
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.


class CustomLoginView(LoginView):

    template_name = "accounts/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()

        # Check if the user is a HospitalEmployee or SystemEmployee
        if hasattr(user, 'hospitalemployee') or hasattr(user, 'systememployee') or user.is_superuser:
            return super().form_valid(form)
        else:
            messages.error(self.request, 'You are not allowed to login.')
            return redirect('accounts:login')