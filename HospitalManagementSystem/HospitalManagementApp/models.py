from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.
class base_user(User):
  USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'doctor'),
      (3, 'clerk'),
  )
  user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)

class hospital(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=50)
    name = models.CharField(max_length=40)

class clerk(models.Model):
    user = models.OneToOneField(base_user, on_delete=models.CASCADE)
    id=models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    natural_code = models.IntegerField(null=True)
    phone = models.IntegerField(null=True)
    email = models.CharField(null=True, max_length=40)
    hospital_id =models.ForeignKey(hospital,on_delete=models.CASCADE, null=True)

# class hospital_manager(models.Model):
#     id = models.IntegerField(primary_key=True)
#     username = models.ForeignKey(user, on_delete=models.CASCADE)
#     hospital_id = models.ForeignKey(hospital,on_delete=models.CASCADE)

class doctor(models.Model):
    user = models.OneToOneField(base_user, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    natural_code = models.IntegerField(null=True)
    msn = models.IntegerField(null=True)
    phone = models.IntegerField(null=True)
    email = models.CharField(max_length=40, null=True)
    email_confirmed = models.BooleanField(default=False)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE, null=True)

@receiver(post_save, sender=base_user)
def update_user(sender, instance, created, **kwargs):
    if created:
        if  instance.user_type == 2:
            doctor.objects.get_or_create(user=instance)
        elif instance.user_type == 3:
            clerk.objects.get_or_create(user=instance)
    if instance.user_type == 2:
        instance.doctor.save()
    elif instance.user_type == 3:
        instance.clerk.save()

class relation_doctor_hospital(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor_id = models.ForeignKey(doctor,on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class relation_doctor_clerk(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor_id = models.ForeignKey(doctor,on_delete=models.CASCADE)
    clerk_id = models.ForeignKey(clerk, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class free_time(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor_id = models.ForeignKey(doctor, on_delete=models.CASCADE)
    free_time = models.DateTimeField()
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class reserve(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor_id = models.ForeignKey(doctor, on_delete=models.CASCADE)
    reserve_time = models.DateTimeField()
    natural_code = models.IntegerField()
    clerk_id = models.ForeignKey(clerk, on_delete=models.CASCADE)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)

class comment(models.Model):
    id = models.IntegerField(primary_key=True)
    natural_code = models.IntegerField()
    request_kind = models.CharField(max_length=255)
    request_txt = models.CharField(max_length=255)
    hospital_id = models.ForeignKey(hospital, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)