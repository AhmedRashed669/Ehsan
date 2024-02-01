from collections.abc import Iterable
from django.db import models
from accounts.models import Hospital
from django.urls import reverse,reverse_lazy

# Create your models here.
class Patient(models.Model):
    male = "M"
    female = "F"
    Gender_choices = {
        male:"Male",
        female:"Female"
    }
    first_name = models.CharField(max_length = 256)
    middle_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256)
    phone_number = models.PositiveBigIntegerField()
    age = models.PositiveSmallIntegerField()
    sex = models.CharField(max_length=1,choices = Gender_choices)

    def __str__(self) -> str:
        return "{} {} {}".format(self.first_name,self.middle_name,self.last_name)
    
    def get_absolute_url(self):
        return reverse_lazy("patients:create-case",kwargs={'pk':self.pk})

class PatientCase(models.Model):
    urgent = "U"
    surgery ="S"
    treatment = "T"
    case_type_choices = {
        urgent : "Urgent",
        surgery : "Surgery",
        treatment : "Treatment"
    }
    patient_name = models.OneToOneField(Patient,models.CASCADE)
    reported_by = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)
    diagnose = models.CharField(max_length = 256)
    is_successful = models.BooleanField(default = False)
    cost = models.PositiveIntegerField()
    case_type = models.CharField(max_length=1,choices = case_type_choices)

    def __str__(self) -> str:
        return str(self.patient_name)
    
    # def get_absolute_url(self):
    #     return reverse("patients:patient-list")

    # def set_name(self,name):
    #     self.patient_name = name
    #     self.save()
