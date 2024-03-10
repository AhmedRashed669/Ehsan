from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from patients.models import PatientCase
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver


# Create your models here.
class Donor(models.Model):
    male = "Male"
    female = "Female"
    Gender_choices = {
        male:"Male",
        female:"Female"
    }
    username = models.OneToOneField(User,on_delete = models.CASCADE)
    first_name  = models.CharField()
    last_name  = models.CharField()
    phone_number = models.PositiveBigIntegerField()
    email = models.EmailField()
    sex = models.CharField(max_length=6,choices = Gender_choices)
    cases = models.ManyToManyField(PatientCase,
                                   through="PatientCase_Donors",
                                   related_name="donors")

    def __str__(self) -> str:
        return "{} {}".format(self.first_name,self.last_name).title()
    
# @receiver(post_save,sender = Donor)
# def create_user(sender,instance,created,**kwargs):
#     if created:
#         User.objects.create(username = instance.full_name,email = instance.email)
#         print(created)

# post_save.connect(create_user,sender=Donor)


class PatientCase_Donors(models.Model):
    patient_case = models.ForeignKey(PatientCase,on_delete = models.CASCADE)
    donor = models.ForeignKey(Donor,on_delete = models.CASCADE)
    amount =  models.PositiveBigIntegerField()
    date = models.DateTimeField()

