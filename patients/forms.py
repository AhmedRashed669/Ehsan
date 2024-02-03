from django import forms
from .models import PatientCase

class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = ('diagnose','cost','case_type')