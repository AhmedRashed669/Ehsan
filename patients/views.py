from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,DetailView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import PatientCaseForm
from accounts.models import HospitalEmployee,Hospital
from patients.models import *

# Create your views here.
class PatientList(LoginRequiredMixin,ListView):
    model = Patient

    # def get_queryset(self) -> QuerySet[Any]:
    #     if user.HospitalEmployee:
    #         return Patient.objects.filter(patient_name =)
    #     else:

    #context name will be patieint_list


class CreatePatient(LoginRequiredMixin,CreateView):
    model = Patient
    fields = '__all__'

class UpdatePatient(LoginRequiredMixin,UpdateView):
    model = Patient
    fields = '__all__'
    template_name_suffix = "_update_form"
    # success_url = reverse_lazy('patients:patient-list')

    def get_success_url(self):
        return reverse_lazy('patients:patient-detail',kwargs = {'pk' : self.object.pk})

class DeletePatient(LoginRequiredMixin,DeleteView):
    model = Patient
    success_url = reverse_lazy('patients:patient-list')
    context_object_name = "patient"


class PatientDetail(LoginRequiredMixin,DetailView):
    model = Patient
    #still figuring it out
    # def get_queryset(self) -> QuerySet[Any]:
    #     query = super().get_queryset()
    #     query = PatientCase.objects.get(patient_name_id = self.kwargs['pk'])
    #     return query
    #working
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = PatientCase.objects.filter(patient_name_id = self.kwargs['pk'])
        context['patientcase'] = query
        return context

    #Patient Cases

@login_required
def patient_case_create(request,pk):
    patient = get_object_or_404(Patient,pk=pk)
    try:
        hospital = request.user.hospitalemployee.hospital    
    except:
        hospital = Hospital.objects.get(hospital_name = 'admin')
        
    # print(hospital)
    # if not hospital:
    # hospital = Hospital.objects.get(hospital_name = 'admin')
    # print(hospital)
    if request.method == 'POST':
        form = PatientCaseForm(request.POST)
        if form.is_valid:
            patientcase = form.save(commit=False)
            patientcase.patient_name = patient
            patientcase.reported_by = hospital
            patientcase.save()  
            return redirect('patients:patient-detail',pk=patient.pk)
        
    else:
        form = PatientCaseForm()

    return render(request,'patients/patientcase_form.html',{'form':form})   
    

# class PatientCaseCreate(FormView):
#     template_name = 'patients/patientcase_form.html'
#     form_class =  PatientCaseForm 
#     success_url = 'patients:patient-detail'
    
    


class PatientCaseDetail(LoginRequiredMixin,DetailView):
    model = PatientCase
    context_object_name = "patientcase"

class UpdatePatientCase(LoginRequiredMixin,UpdateView):
    model = PatientCase
    fields = ('diagnose','cost','case_type')
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy("patients:case-detail",kwargs = {'pk':self.object.pk})