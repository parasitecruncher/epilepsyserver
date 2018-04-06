from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    def __init__(self):
        pass

    p_id = models.OneToOneField('auth.User', related_name="patient_account",unique=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    emergency_contact1 = models.CharField(max_length=50)
    emergency_contact2 = models.CharField(max_length=50)
    current_GPS = models.CharField(max_length=50)


class PatientSiezures(models.Model):
    def __init__(self):
        pass

    p_id = models.ForeignKey('auth.User', related_name="patient_siezure")
    time_of_siezure = models.CharField(max_length=50)
    siezure_GPS = models.CharField(max_length=50)
