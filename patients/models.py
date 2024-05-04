from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import Hospital,HospitalEmployee
from django.urls import reverse,reverse_lazy
from django.utils import timezone
from .fcm import send_message
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from .fcm import send_message
from django.contrib.auth.models import User



# Create your models here.
class Patient(models.Model):
    male = "Male"
    female = "Female"
    Gender_choices = {
        male:"Male",
        female:"Female"
    }
    first_name = models.CharField(max_length = 256)
    middle_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256)
    phone_number = models.PositiveIntegerField()
    age = models.PositiveSmallIntegerField()
    sex = models.CharField(max_length=6,choices = Gender_choices)
    

    def __str__(self) -> str:
        return "{} {} {}".format(self.first_name,self.middle_name,self.last_name).title()
    
    def get_absolute_url(self):
        return reverse_lazy("patients:create-case",kwargs={'pk':self.pk})


class PatientCase(models.Model):
    urgent = "Urgent"
    surgery ="Surgery"
    treatment = "Treatment"
    case_type_choices = {
        urgent : "Urgent",
        surgery : "Surgery",
        treatment : "Treatment"
    }
    patient_name = models.ForeignKey(Patient,models.CASCADE)
    reported_by = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)
    diagnose = models.CharField(max_length = 256)
    is_successful = models.BooleanField(default = False,verbose_name = "Successful")
    cost = models.PositiveIntegerField()
    case_type = models.CharField(max_length=10,choices = case_type_choices)
    created_date = models.DateTimeField(default = timezone.now)
    is_approve = models.BooleanField(default = False,verbose_name = "Approve") #work on it
    is_accepted = models.BooleanField(default = False,verbose_name = "Accept") #validated
    docs =  models.FileField(upload_to='patients_docs',null=True)

    def __str__(self) -> str:
        return  "{}-{}".format(self.patient_name,self.diagnose).title()
    
    
    def approve(self):
        self.is_approve = True
        self.save()

    def succeeded(self):
        self.is_successful = True
        self.save()
    
    def accepted(self):
        self.is_accepted = True
        self.save()

    class Meta:
        permissions = (("can_approve_cases","Set case as approved"),
                       ("can_succeed_case","Set case as successful"),)
        
        ordering = ["-created_date"]
    # def get_absolute_url(self):
    #     return reverse("patients:patient-list")

@receiver(post_save, sender = PatientCase)
def notify_admin_case(sender, instance = None, created = False, **kwargs):
    if created:
        mess = Message(
        notification=Notification(title="New Case", body="A new case was added by a hospital check it out!",image='https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8250.jpg?w=1060&t=st=1713138548~exp=1713139148~hmac=efcc95fb70d0f61ef4f10874d38994b404cee5d87e085b7c3df334ae2739d0a7'),
        )
        users = User.objects.filter(systememployee__isnull=False)
        devices = FCMDevice.objects.filter(user__in=users)
        if devices.exists():
                devices.send_message(mess)


@receiver(post_save, sender = PatientCase)
def notify_hospital_case(sender, instance = None, created = False, **kwargs):
    print("approved")
    if instance.is_approve:
        mess = Message(
        notification=Notification(title="{} case is approved".format(instance.diagnose).title(), 
                                  body="A case has been approved check it out!",
                                  image='https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8250.jpg?w=1060&t=st=1713138548~exp=1713139148~hmac=efcc95fb70d0f61ef4f10874d38994b404cee5d87e085b7c3df334ae2739d0a7'),
        )
        # users = User.objects.filter(hospitalemployee_set = instance.reported_by)
        users = User.objects.filter(hospitalemployee__hospital=instance.reported_by)
        devices = FCMDevice.objects.filter(user__in=users)
        if devices.exists():
                devices.send_message(mess)



        
        

        


