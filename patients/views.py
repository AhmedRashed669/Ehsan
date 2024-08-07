from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import (ListView,CreateView,UpdateView,DeleteView,DetailView,FormView)
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib.auth import get_user
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import PatientCaseForm
from accounts.models import HospitalEmployee,Hospital
from patients.models import *
from firebase_admin.messaging import Message,Notification
from fcm_django.models import FCMDevice
from .fcm import send_message
import threading

# Create your views here.
class PatientList(LoginRequiredMixin,ListView):
    model = Patient

    def get_queryset(self) -> QuerySet[Any]:
        querySet = super().get_queryset()
        #query for hospital employee
        try:
            #query for hospital employee
            hospital = self.request.user.hospitalemployee.hospital
            return querySet.filter(patientcase__reported_by = hospital,
                                    patientcase__is_successful = False)
        except:                
            #query for system employee
            try:
                if self.request.user.systememployee:
                    return querySet.filter(patientcase__is_approve = False)
                
            except:
                return super().get_queryset()   
        #context name will be patieint_list

class PatientHistory(LoginRequiredMixin,ListView):
    model = Patient
    template_name_suffix = 'history_list'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset.filter(patientcase__is_successful = True)

            
def approve_case(request,pk):
    patient_case = get_object_or_404(PatientCase,pk = pk)
    patient_case.approve()
    patient_pk = patient_case.patient_name.id

    return redirect("patients:patient-detail",pk = patient_pk )

def succeed_case(request,pk):
    patient_case = get_object_or_404(PatientCase,pk = pk)
    patient_case.succeeded()
    patient_pk = patient_case.patient_name.id
    return redirect("patients:patient-detail",pk = patient_pk )

def accept_case(request,pk):
    # thread = threading.Thread(target=send_message)
    # thread.start()
    patient_case = get_object_or_404(PatientCase,pk = pk)
    patient_case.accepted()
    patient_pk = patient_case.patient_name.id 
    # return redirect("patients:patient-detail",pk = patient_pk )
    return redirect("patients:patient-detail",pk = patient_pk )


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

class DeletePatient(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = Patient
    success_url = reverse_lazy('patients:patient-list')
    context_object_name = "patient"
    permission_required = "patients.delete_patient"


class PatientDetail(LoginRequiredMixin,DetailView):
    model = Patient
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query = PatientCase.objects.filter(patient_name_id = self.kwargs['pk'])
        context['patientcase'] = query
        return context

    #Patient Cases
    
class PatientCaseCreate(LoginRequiredMixin,CreateView):
    model = PatientCase
    form_class = PatientCaseForm
    template_name = 'patients/patientcase_form.html'

    def form_valid(self, form):
        patient = get_object_or_404(Patient, pk=self.kwargs['pk'])
        try:
            hospital = self.request.user.hospitalemployee.hospital    
        except:
            hospital = Hospital.objects.get(hospital_name = 'admin')

        patientcase = form.save(commit=False)
        patientcase.patient_name = patient
        patientcase.reported_by = hospital
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patients:patient-detail', kwargs={'pk': self.object.patient_name.pk})


class PatientCaseDetail(LoginRequiredMixin,DetailView):
    model = PatientCase
    context_object_name = "patientcase"

class UpdatePatientCase(LoginRequiredMixin,UpdateView):
    model = PatientCase
    fields = ('diagnose','cost','case_type')
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse_lazy("patients:case-detail",kwargs = {'pk':self.object.pk})
    

class DeletePatientCase(LoginRequiredMixin,PermissionRequiredMixin,DeleteView):
    model = PatientCase
    context_object_name = "patientcase"
    permission_required = "patients.delete_patientcase"
    

    def get_success_url(self) -> str:
        return reverse_lazy("patients:patient-detail",kwargs = {'pk':self.object.patient_name.pk})
    

