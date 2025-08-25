from django.db import models

# Create your models here.

class login(models.Model):
    username=models.CharField(max_length=15,unique=True)
    password=models.CharField(max_length=15)
    usertype=models.CharField(max_length=15)


class patient(models.Model):
    name=models.CharField(max_length=200)
    age=models.IntegerField()
    address=models.TextField(max_length=200)
    phone=models.IntegerField()
    gender=models.CharField(max_length=200)
    bloodgroup=models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)

class medicalhistory(models.Model):
    diagnosis=models.CharField(max_length=200)
    medication=models.CharField(max_length=200)
    allergies=models.CharField(max_length=200)
    treatments=models.CharField(max_length=200)
    date=models.DateField(max_length=200)
    PATIENT=models.ForeignKey(patient, on_delete=models.CASCADE)

class billing(models.Model):
    amount=models.CharField(max_length=200)
    invoice=models.CharField(max_length=200)
    status=models.CharField(max_length=200)
    date=models.DateField(max_length=200)
    paymentdate=models.DateField(max_length=200,null=True, blank=True)
    insurance=models.CharField(max_length=200)
    service=models.CharField(max_length=200)
    PATIENT=models.ForeignKey(patient, on_delete=models.CASCADE)

class healthinfo(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)

class doctors(models.Model):
    name=models.CharField(max_length=200)
    specialization=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    phone=models.IntegerField()
    schedule=models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login, on_delete=models.CASCADE)

class booking(models.Model):
    time=models.TimeField(max_length=200)
    date=models.DateField(max_length=200)
    status=models.CharField(max_length=200)
    DOCTORS = models.ForeignKey(doctors, on_delete=models.CASCADE)
    PATIENTS = models.ForeignKey(patient, on_delete=models.CASCADE)

class facilities(models.Model):
    name=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    department=models.CharField(max_length=200)
    resources=models.CharField(max_length=200)

class prescription(models.Model):
    name=models.CharField(max_length=200)
    dosage=models.CharField(max_length=200)
    instruction=models.CharField(max_length=200)
    date=models.DateField(max_length=200)
    DOCTORS = models.ForeignKey(doctors, on_delete=models.CASCADE)
    PATIENT=models.ForeignKey(patient, on_delete=models.CASCADE)


