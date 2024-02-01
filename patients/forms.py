from django import forms
from .models import PatientCase

class PatientCaseForm(forms.ModelForm):
    class Meta:
        model = PatientCase
        fields = ('reported_by','diagnose','cost','case_type')