from django.shortcuts import render
from django.views.generic import (ListView,DetailView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

# Create your views here.
class PatientList(LoginRequiredMixin,ListView):
    model = Patient
    #context name will be patieint_list

