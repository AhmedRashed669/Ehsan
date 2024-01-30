from django.shortcuts import render
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import *

# Create your views here.
class PatientList(LoginRequiredMixin,ListView):
    model = Patient
    #context name will be patieint_list


class CreatePatient(LoginRequiredMixin,CreateView):
    model = Patient
    fields = '__all__'

class UpdatePatient(LoginRequiredMixin,UpdateView):
    model = Patient
    fields = '__all__'
    template_name_suffix = "_update_form"
    success_url = reverse_lazy('patients:patient-list')

class DeletePatient(LoginRequiredMixin,DeleteView):
    model = Patient
    success_url = reverse_lazy('patients:patient-list')
    context_object_name = "patient"