from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from patients.models import PatientCase
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
from django.contrib.auth.models import User


# Create your models here.
class Donor(models.Model):
    male = "Male"
    female = "Female"
    Gender_choices = {
        male:"Male",
        female:"Female"
    }
    username = models.OneToOneField(User,on_delete = models.CASCADE)
    full_name  = models.CharField(max_length = 256)
    phone_number = models.PositiveBigIntegerField()
    email = models.EmailField()
    sex = models.CharField(max_length=6,choices = Gender_choices)
    cases = models.ManyToManyField(PatientCase,
                                   through="PatientCase_Donors",
                                   related_name="donors",
                                   blank=True)
    watch_later = models.ManyToManyField(PatientCase,
                                         related_name="watched_by",
                                         blank=True)
    # pic = models.FileField()

    def __str__(self) -> str:
        return self.full_name.title()


class PatientCase_Donors(models.Model):
    patient_case = models.ForeignKey(PatientCase,on_delete = models.CASCADE)
    donor = models.ForeignKey(Donor,on_delete = models.CASCADE,)
    amount =  models.PositiveBigIntegerField()
    date = models.DateTimeField(default = timezone.now)

    def __str__(self) -> str:
        return "{}--{}".format(self.patient_case,self.donor).title()
    

class GeneralDonations(models.Model):
    donor = models.ForeignKey(Donor,on_delete = models.CASCADE)
    amount =  models.BigIntegerField()
    donation_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}".format(self.donor).title()


@receiver(post_save, sender=Donor)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Generates token whenever a donor is created
    """
    if created:
        Token.objects.create(user=instance.username)

@receiver(post_save, sender=PatientCase_Donors)
def set_case_as_approved(sender, instance=None, created=False, **kwargs):
    if created:
        total_donation = sender.objects.filter(patient_case=instance.patient_case).aggregate(total=Sum('amount'))['total'] or 0
        patientcase = instance.patient_case
        if total_donation >= patientcase.cost:
            patientcase.approve()
            users = User.objects.filter(hospitalemployee__isnull=False, hospitalemployee__hospital= 4)
            devices = FCMDevice.objects.filter(user__in=users)
            mess = Message(
                notification=Notification(
                    title="Case approved",
                    body="case has been approved initiate the treatment",
                    image='https://img.freepik.com/free-vector/hospital-building-concept-illustration_114360-8250.jpg?w=1060&t=st=1713138548~exp=1713139148~hmac=efcc95fb70d0f61ef4f10874d38994b404cee5d87e085b7c3df334ae2739d0a7'
                )
            )
            if devices.exists():
                devices.send_message(mess)