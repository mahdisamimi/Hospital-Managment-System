from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)

class hospital(models.Model):
    id = models.IntegerField()
    address = models.CharField(max_length=50)
    name = models.CharField(max_length=40)

class clerk(models.Model):
    id=models.IntegerField()
    username = models.ForeignKey(user , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    natural_code = models.IntegerField(max_length=10)
    phone = models.IntegerField(max_length=11)
    email = models.CharField(max_length=40)
    hospital_id =models.ForeignKey(hospital,on_delete=models.CASCADE)

class hospital_manager(models.Model):
    id = models.IntegerField()
    username = models.ForeignKey(user, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital,on_delete=models.CASCADE)

class doctor(models.Model):
    id = models.IntegerField()
    username = models.ForeignKey(user , on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    natural_code = models.IntegerField(max_length=10)
    msn = models.IntegerField(max_length=20)
    phone = models.IntegerField(max_length=11)
    email = models.CharField(max_length=40)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class relation_doctor_hospital(models.Model):
    id = models.IntegerField()
    doctor_id = models.ForeignKey(doctor,on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class relation_doctor_clerk(models.Model):
    id = models.IntegerField()
    doctor_id = models.ForeignKey(doctor,on_delete=models.CASCADE)
    clerk_id = models.ForeignKey(clerk, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class free_time(models.Model):
    id = models.IntegerField()
    doctor_id = models.ForeignKey(doctor, on_delete=models.CASCADE)
    free_time = models.DateTimeField()
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class reserve(models.Model):
    id = models.IntegerField()
    doctor_id = models.ForeignKey(doctor, on_delete=models.CASCADE)
    reserve_time = models.DateTimeField()
    natural_code = models.IntegerField(max_length=10)
    clerk_id = models.ForeignKey(clerk, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class comment(models.Model):
    id = models.IntegerField()
    natural_code = models.IntegerField(max_length=10)
    request_kind = models.CharField(max_length=255)
    request_txt = models.CharField(max_length=255)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)