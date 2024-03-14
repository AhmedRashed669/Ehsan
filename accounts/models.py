from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=256)
    location = models.CharField(blank=True,max_length=256)
    phone_number = models.PositiveBigIntegerField(null = True)
    bank_account = models.PositiveBigIntegerField(null = True)

    def __str__(self) -> str:
        return str(self.hospital_name)

class HospitalEmployee(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.name)
    

class SystemEmployee(models.Model):
    employee_name = models.OneToOneField(User,on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField()
    
    def __str__(self) -> str:
        return str(self.employee_name)
    






