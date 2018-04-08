from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class Patient(models.Model):
    p_id = models.OneToOneField('auth.User', related_name="patient_profile")
    name = models.CharField(max_length=50)
    birthdate =models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    emergency_contact1 = models.CharField(max_length=50)
    emergency_contact2 = models.CharField(max_length=50)
    current_GPS = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PatientSiezure(models.Model):
    p_id = models.ForeignKey('auth.User', related_name="patient_siezure")
    time_of_siezure = models.CharField(max_length=50)
    siezure_GPS = models.CharField(max_length=50)

    def __str__(self):
        return self.p_id.username
